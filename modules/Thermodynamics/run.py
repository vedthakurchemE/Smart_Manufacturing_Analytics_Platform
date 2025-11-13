# 📘 run.py - Thermodynamics Module | AllProjectsSuite
# 🌡️ Thermodynamic Visualizer & Calculator
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def run():
    # === Page Config ===
    st.set_page_config(page_title="🌡️ Thermodynamics App", layout="centered")

    # === App Header ===
    st.title("🌡️ Thermodynamics Analyzer")
    st.markdown("""
    Welcome to the **Thermodynamics App** – an educational + analytical tool for visualizing core thermodynamic concepts.

    🔹 Developed by: **Ved Thakur**  
    🔹 Institute: **IPS Academy Indore**  
    🔹 Part of: **AllProjectsSuite** (Chemical + Data Projects)

    ---  
    """)

    # === User Input Section ===
    st.header("📊 Ideal Gas Law Calculator (PV=nRT)")

    col1, col2 = st.columns(2)
    with col1:
        P = st.number_input("🔵 Pressure (P) [atm]", value=1.0)
        V = st.number_input("🟢 Volume (V) [L]", value=22.4)
    with col2:
        n = st.number_input("🟡 Moles of Gas (n)", value=1.0)
        R = 0.0821  # Ideal gas constant
        T = st.number_input("🔴 Temperature (T) [K]", value=273.15)

    # === Calculate ===
    st.subheader("🧮 Calculation Result")
    calculated_PV = round(n * R * T, 3)
    if st.button("Calculate PV using nRT"):
        st.success(f"Calculated PV = {calculated_PV} L·atm")

    # === Plotting Section ===
    st.header("📈 PV vs T Graph (Constant n, R, V)")

    T_vals = np.linspace(200, 600, 100)
    PV_vals = n * R * T_vals

    fig, ax = plt.subplots()
    ax.plot(T_vals, PV_vals, color='red')
    ax.set_title("Ideal Gas Law: PV vs Temperature")
    ax.set_xlabel("Temperature (K)")
    ax.set_ylabel("PV (L·atm)")
    st.pyplot(fig)

    # === Footer ===
    st.markdown("---")
    st.markdown("🧪 *This is part of the AllProjectsSuite by Ved Thakur.*")
