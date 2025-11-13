# tools/combustion.py

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# === CONSTANTS ===

CALORIFIC_VALUES = {
    "Methane (CH4)": 802.3,
    "Propane (C3H8)": 2043.0,
    "Octane (C8H18)": 5470.0,
    "Hydrogen (H2)": 286.0,
    "Carbon Monoxide (CO)": 283.0
}

STOICH_AFR = {
    "Methane (CH4)": 17.2,
    "Propane (C3H8)": 15.7,
    "Octane (C8H18)": 15.1,
    "Hydrogen (H2)": 34.3,
    "Carbon Monoxide (CO)": 2.4
}

MOLAR_MASS = {
    "Methane (CH4)": 16.04,
    "Propane (C3H8)": 44.1,
    "Octane (C8H18)": 114.2,
    "Hydrogen (H2)": 2.02,
    "Carbon Monoxide (CO)": 28.0
}

# === FUNCTIONS ===

def get_calorific_value(fuel_name: str) -> float:
    return CALORIFIC_VALUES.get(fuel_name, 0.0)

def get_stoich_afr(fuel_name: str) -> float:
    return STOICH_AFR.get(fuel_name, 14.7)

def get_molar_mass(fuel_name: str) -> float:
    return MOLAR_MASS.get(fuel_name, 18.0)

def combustion_efficiency(air_fuel_ratio: float, fuel_name: str) -> float:
    stoich_afr = get_stoich_afr(fuel_name)
    if air_fuel_ratio <= 0 or stoich_afr <= 0:
        return 0.0
    efficiency = np.exp(-((air_fuel_ratio - stoich_afr) ** 2) / (2 * (stoich_afr * 0.2) ** 2)) * 100
    return round(efficiency, 2)

def heat_output(fuel_flow_rate_mol: float, fuel_name: str) -> float:
    calorific_value = get_calorific_value(fuel_name)
    return round(fuel_flow_rate_mol * calorific_value, 2)

def convert_flow_rate(value: float, from_unit: str, fuel_name: str) -> float:
    molar_mass = get_molar_mass(fuel_name)
    if from_unit == "kg/h":
        return (value * 1000) / 3600 / molar_mass
    elif from_unit == "kg/s":
        return (value * 1000) / molar_mass
    else:
        return value  # assume mol/s

def simulate_combustion(fuel_name, afr, fuel_flow_rate, flow_unit):
    fuel_flow_mol_s = convert_flow_rate(fuel_flow_rate, flow_unit, fuel_name)
    heat_release = heat_output(fuel_flow_mol_s, fuel_name)
    efficiency = combustion_efficiency(afr, fuel_name)
    useful_energy = round((efficiency / 100) * heat_release, 2)
    waste_energy = round(heat_release - useful_energy, 2)

    return {
        "Fuel": fuel_name,
        "AFR": afr,
        "Stoichiometric AFR": get_stoich_afr(fuel_name),
        "Calorific Value (kJ/mol)": get_calorific_value(fuel_name),
        "Fuel Flow Rate (mol/s)": fuel_flow_mol_s,
        "Total Heat Released (kJ/s)": heat_release,
        "Combustion Efficiency (%)": efficiency,
        "Useful Energy (kJ/s)": useful_energy,
        "Heat Loss (kJ/s)": waste_energy
    }

def generate_efficiency_curve(fuel_name, afr_range=(5, 40), points=100):
    afrs = np.linspace(*afr_range, points)
    efficiencies = [combustion_efficiency(afr, fuel_name) for afr in afrs]
    return afrs, efficiencies

# === STREAMLIT UI ===

def run():
    st.title("💨 Combustion Analyzer")
    st.markdown("Analyze combustion efficiency, heat output, and energy loss.")

    fuel = st.selectbox("Select Fuel Type:", list(CALORIFIC_VALUES.keys()))
    afr = st.slider("Air-Fuel Ratio (AFR)", 5.0, 40.0, get_stoich_afr(fuel), step=0.1)
    flow_unit = st.selectbox("Fuel Flow Unit:", ["mol/s", "kg/s", "kg/h"])
    flow_value = st.number_input(f"Fuel Flow Rate ({flow_unit}):", min_value=0.0, value=1.0, step=0.1)

    if st.button("🔥 Simulate Combustion"):
        results = simulate_combustion(fuel, afr, flow_value, flow_unit)
        st.subheader("🔍 Simulation Results")
        st.dataframe(pd.DataFrame([results]))

        st.subheader("📉 Efficiency Curve")
        x, y = generate_efficiency_curve(fuel)
        fig, ax = plt.subplots()
        ax.plot(x, y, label="Efficiency (%)", color="green")
        ax.axvline(get_stoich_afr(fuel), color="red", linestyle="--", label="Stoich AFR")
        ax.set_xlabel("AFR")
        ax.set_ylabel("Efficiency (%)")
        ax.set_title(f"Efficiency Curve for {fuel}")
        ax.legend()
        st.pyplot(fig)

        st.download_button("📥 Download CSV", pd.DataFrame([results]).to_csv(index=False), "combustion_results.csv")
