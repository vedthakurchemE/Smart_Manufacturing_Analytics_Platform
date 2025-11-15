# 📘 Module 8: Condensation Heat Transfer Estimator | HeatTransferAI Suite
# 💧 Estimate heat transfer coefficient during filmwise condensation on vertical surfaces
# 🚀 Version: Advanced Interactive UI + Visuals + Engineering Insights
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.set_page_config(page_title="💧 Condensation Estimator", layout="centered")
    st.title("💧 Condensation Heat Transfer Estimator")
    st.markdown("This tool estimates the **heat transfer coefficient** during filmwise condensation on vertical plates using **Nusselt’s Equation**.")
    st.markdown("---")

    with st.expander("📥 Input Parameters"):
        col1, col2 = st.columns(2)
        with col1:
            L = st.number_input("🧱 Plate Height `L (m)`", min_value=0.01, value=0.5, step=0.1)
            rho_l = st.number_input("💧 Liquid Density `ρₗ (kg/m³)`", min_value=1.0, value=1000.0)
            rho_v = st.number_input("🌫️ Vapor Density `ρᵥ (kg/m³)`", min_value=0.1, value=1.2)
            mu_l = st.number_input("🛢️ Liquid Viscosity `μₗ (Pa·s)`", min_value=1e-5, value=0.001)
        with col2:
            k_l = st.number_input("🔌 Thermal Conductivity `kₗ (W/m·K)`", min_value=0.01, value=0.6)
            h_fg = st.number_input("🔥 Latent Heat of Vaporization `h_fg (J/kg)`", min_value=1e4, value=2.25e6)
            T_s = st.number_input("🌡️ Surface Temperature `Tₛ (°C)`", value=30.0)
            T_sat = st.number_input("♨️ Saturation Temperature `T_sat (°C)`", value=100.0)

    if st.button("🚀 Estimate Condensation Coefficient"):
        delta_T = T_sat - T_s
        g = 9.81  # gravity

        if delta_T <= 0:
            st.error("Saturation temperature must be greater than surface temperature (ΔT > 0).")
            return

        # Nusselt Equation
        h = 0.943 * ((k_l**3 * rho_l**2 * g * h_fg) / (mu_l * L * delta_T))**0.25

        st.success(f"✅ Estimated heat transfer coefficient: **{h:.2f} W/m²·K**")

        # Visual Feedback
        fig, ax = plt.subplots()
        deltaTs = np.linspace(1, 70, 100)
        h_values = 0.943 * ((k_l**3 * rho_l**2 * g * h_fg) / (mu_l * L * deltaTs))**0.25
        ax.plot(deltaTs, h_values, color='blue', linewidth=2)
        ax.set_title("Heat Transfer Coefficient vs Temperature Difference")
        ax.set_xlabel("ΔT = T_sat - T_s (°C)")
        ax.set_ylabel("Heat Transfer Coefficient (W/m²·K)")
        ax.grid(True)
        st.pyplot(fig)

        st.markdown("### 🧠 Engineering Insights")
        st.markdown("- Based on **Nusselt’s theory** for laminar filmwise condensation on a vertical surface.")
        st.markdown("- Assumes constant fluid properties, laminar flow, and no vapor shear.")
        st.markdown("- Suitable for smooth surfaces with moderate temperature gradients.")
        st.markdown("- **h ∝ (ΔT)^(-0.25)** → Higher ΔT decreases film thickness, increasing h.")


