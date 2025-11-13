# props.py
"""
Thermodynamic Property Estimator Module

Features:
- Cp interpolation using NASA-like polynomials
- Enthalpy change (ΔH) estimation
- Cp vs Temperature plotting
- Fuel database and curve export

Used in: Thermodynamics simulations, optimization tools, and education.
"""

import streamlit as st
import numpy as np
import pandas as pd

# === Cp Polynomial Coefficients (simplified NASA format) ===
CP_COEFFICIENTS = {
    "Methane (CH4)": [19.89, 5.024e-2, 1.269e-5],
    "Propane (C3H8)": [14.15, 8.94e-2, -1.09e-5],
    "Octane (C8H18)": [25.48, 1.52e-1, -7.15e-5],
    "Hydrogen (H2)": [28.84, -1.01e-2, 1.47e-5],
    "Carbon Monoxide (CO)": [29.1, -0.191e-2, 0.400e-5]
}

def get_cp(fuel: str, T: float) -> float:
    """
    Calculate specific heat capacity Cp at temperature T (K) for given fuel.
    Returns Cp in J/mol·K.
    """
    if fuel not in CP_COEFFICIENTS:
        raise ValueError(f"No Cp data found for {fuel}")
    if not (200 <= T <= 1500):
        raise ValueError(f"Temperature {T}K is outside valid range (200–1500 K)")

    a, b, c = CP_COEFFICIENTS[fuel]
    Cp = a + b * T + c * (T ** 2)
    return round(Cp, 3)

def delta_H(fuel: str, T1: float, T2: float, n_mol: float = 1.0) -> float:
    """
    Estimate change in enthalpy (ΔH) for the fuel between T1 and T2 in kJ.
    """
    if T1 == T2:
        return 0.0

    T_vals = np.linspace(T1, T2, 100)
    Cp_vals = np.array([get_cp(fuel, T) for T in T_vals])
    delta_h_joule = np.trapz(Cp_vals, T_vals) * n_mol
    delta_h_kj = delta_h_joule / 1000
    return round(delta_h_kj, 3)

def get_cp_curve(fuel: str, T_range: tuple = (200, 1000), points: int = 100):
    """
    Generate Cp vs T data for plotting or analysis.
    Returns a tuple of (T_list, Cp_list).
    """
    T_vals = np.linspace(*T_range, points)
    Cp_vals = [get_cp(fuel, T) for T in T_vals]
    return T_vals, Cp_vals

def export_cp_curve_to_csv(fuel: str, filename="cp_curve.csv"):
    """
    Export Cp vs T data to CSV.
    """
    T_vals, Cp_vals = get_cp_curve(fuel)
    df = pd.DataFrame({"Temperature (K)": T_vals, "Cp (J/mol·K)": Cp_vals})
    df.to_csv(filename, index=False)

def get_available_fuels():
    """
    Returns a list of fuels with available Cp data.
    """
    return list(CP_COEFFICIENTS.keys())

def run():
    """
    Streamlit UI entry point.
    """
    st.set_page_config(page_title="🔥 Thermodynamic Properties", layout="centered")
    st.title("🔥 Thermodynamic Property Estimator")

    fuel = st.selectbox("Select Fuel", get_available_fuels())
    T1 = st.number_input("Initial Temperature (K)", min_value=200, max_value=1500, value=300)
    T2 = st.number_input("Final Temperature (K)", min_value=200, max_value=1500, value=800)
    n = st.number_input("Number of Moles", min_value=0.1, value=1.0)

    if T1 and T2 and fuel:
        try:
            delta_h = delta_H(fuel, T1, T2, n)
            st.success(f"ΔH from {T1}K to {T2}K for {n} mol of {fuel} = {delta_h} kJ")

            T_vals, Cp_vals = get_cp_curve(fuel, (T1, T2))
            st.line_chart(pd.DataFrame({"Cp (J/mol·K)": Cp_vals}, index=T_vals))
        except Exception as e:
            st.error(f"Error: {e}")
