# 🔥 Combustion Efficiency Simulator
# Part of the Real-World Thermodynamics Project
# Author: Ved Thakur | Semester 1 | IPS Academy Indore | ChemE (2025-2029)

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ===== Constants =====
FUEL_OPTIONS = ["Methane (CH4)", "Propane (C3H8)", "Octane (C8H18)", "Hydrogen (H2)", "Carbon Monoxide (CO)"]

STOICH_AFR = {
    "Methane (CH4)": 17.2,
    "Propane (C3H8)": 15.7,
    "Octane (C8H18)": 15.1,
    "Hydrogen (H2)": 34.3,
    "Carbon Monoxide (CO)": 2.4
}

# ===== Core Thermodynamic Simulation =====
def compute_efficiency(fuel: str, afr: float) -> float:
    afr_opt = STOICH_AFR.get(fuel, 15.0)
    efficiency = np.exp(-((afr - afr_opt) ** 2) / (2 * (afr_opt * 0.2) ** 2)) * 100
    return round(efficiency, 2)

# ===== Streamlit App =====
def combustion_efficiency_simulator():
    st.set_page_config(page_title="Combustion Efficiency Simulator", layout="centered")
    st.title("🛢️ Combustion Efficiency Simulator")
    st.markdown("Simulate combustion efficiency of different fuels based on air-fuel ratio and thermodynamic principles.")

    # Sidebar: Inputs
    st.sidebar.header("🔧 Input Parameters")
    fuel = st.sidebar.selectbox("Select Fuel Type", FUEL_OPTIONS)
    afr = st.sidebar.slider("Air-Fuel Ratio (AFR)", min_value=5.0, max_value=50.0, value=15.0, step=0.1)

    # Output: Thermodynamics Simulation
    eff = compute_efficiency(fuel, afr)
    st.subheader("📊 Thermodynamic Simulation Result")
    st.success(f"Estimated Combustion Efficiency: **{eff}%**")

    # Efficiency Curve Plot
    afr_range = np.linspace(5, 50, 300)
    efficiency_curve = [compute_efficiency(fuel, x) for x in afr_range]
    fig, ax = plt.subplots()
    ax.plot(afr_range, efficiency_curve, color='blue', label="Efficiency Curve")
    ax.axvline(x=afr, color='red', linestyle='--', label="Your AFR")
    ax.set_xlabel("Air-Fuel Ratio (AFR)")
    ax.set_ylabel("Efficiency (%)")
    ax.set_title(f"Efficiency vs AFR for {fuel}")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

def run():
    combustion_efficiency_simulator()
