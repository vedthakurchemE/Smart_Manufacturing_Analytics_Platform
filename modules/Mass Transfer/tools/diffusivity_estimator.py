# 📘 Module 5: Binary Diffusion Coefficient Estimator | MassTransferAI Suite
# 🧪 Estimate binary diffusivity using Wilke–Chang (liquids) or Fuller (gases)
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("🌡️ Binary Diffusion Coefficient Estimator")
    st.markdown("""
    Estimate **binary diffusion coefficients (D<sub>AB</sub>)** in gases or liquids.  
    - Wilke–Chang for **liquids**  
    - Fuller’s method for **gases**  
    """)

    phase = st.sidebar.radio("Choose Phase", ["Liquid", "Gas"])

    st.sidebar.markdown("ℹ️ Accurate within ~10–20% for common engineering use.")

    if phase == "Liquid":
        st.subheader("💧 Wilke–Chang Equation for Liquids")

        M_B = st.number_input("Molar Mass of Solvent M_B (g/mol)", value=18.0, min_value=0.1)
        phi = st.number_input("Association Factor φ (e.g. 2.6 for water)", value=2.6)
        V_A = st.number_input("Solute Molar Volume at BP V_A (cm³/mol)", value=90.0, min_value=0.1)
        mu = st.number_input("Viscosity μ (cP)", value=1.0, min_value=0.001)
        T = st.number_input("Temperature T (K)", value=298.0, min_value=100.0)

        try:
            D_AB = 7.4e-8 * (phi * M_B)**0.5 * T / (mu * V_A**0.6)
            D_AB_m2s = D_AB * 1e-4
            st.success(f"✅ Estimated D_AB = {D_AB_m2s:.4e} m²/s")
        except Exception:
            st.error("Check your inputs — cannot compute diffusivity.")

        st.markdown(r"""
        **Equation:**  
        $$
        D_{AB} = \frac{7.4 \times 10^{-8} \cdot \sqrt{\phi \cdot M_B} \cdot T}{\mu \cdot V_A^{0.6}}
        $$
        - φ: Association factor (e.g. 2.6 for water)  
        - M<sub>B</sub>: Solvent molar mass (g/mol)  
        - μ: Viscosity (cP)  
        - V<sub>A</sub>: Solute molar volume (cm³/mol)  
        """)

    else:
        st.subheader("🌀 Fuller’s Equation for Gases")

        T = st.number_input("Temperature T (K)", value=298.0, min_value=100.0)
        P = st.number_input("Pressure P (atm)", value=1.0, min_value=0.01)
        M_A = st.number_input("Molar Mass of Gas A (g/mol)", value=28.0, min_value=0.1)
        M_B = st.number_input("Molar Mass of Gas B (g/mol)", value=32.0, min_value=0.1)
        sigma_A = st.number_input("Diffusion Volume A (σₐ)", value=18.0, min_value=1.0)
        sigma_B = st.number_input("Diffusion Volume B (σᵦ)", value=20.0, min_value=1.0)

        try:
            D_AB = 0.00143 * T**1.75 * np.sqrt(1/M_A + 1/M_B) / (P * ( (sigma_A**(1/3) + sigma_B**(1/3))**2 ))
            D_AB_m2s = D_AB * 1e-4
            st.success(f"✅ Estimated D_AB = {D_AB_m2s:.4e} m²/s")
        except Exception:
            st.error("Check your inputs — could not compute diffusivity.")

        st.markdown(r"""
        **Equation:**  
        $$
        D_{AB} = \frac{0.00143 \cdot T^{1.75} \cdot \sqrt{\frac{1}{M_A} + \frac{1}{M_B}}}{P \cdot (\sigma_A^{1/3} + \sigma_B^{1/3})^2}
        $$
        - T in K, P in atm  
        - σ: Diffusion volumes  
        """)

    # 🔍 Model Notes
    with st.expander("📘 When to Use Which Model?"):
        st.markdown("""
        - **Wilke–Chang**: For **liquid–liquid or solid–liquid** systems  
        - **Fuller**: For **gas–gas** or gas in air systems  
        - Both methods are semi-empirical and offer reasonable estimates.  
        """)

    # 📉 Optional: D_AB vs Temperature
    with st.expander("📊 Diffusivity vs Temperature"):
        T_vals = np.linspace(273, 373, 100)
        if phase == "Liquid":
            D_vals = [7.4e-8 * (phi * M_B)**0.5 * T_i / (mu * V_A**0.6) * 1e-4 for T_i in T_vals]
        else:
            D_vals = [0.00143 * T_i**1.75 * np.sqrt(1/M_A + 1/M_B) /
                      (P * ( (sigma_A**(1/3) + sigma_B**(1/3))**2 )) * 1e-4 for T_i in T_vals]
        fig, ax = plt.subplots()
        ax.plot(T_vals, D_vals, color='blue')
        ax.set_xlabel("Temperature (K)")
        ax.set_ylabel("D_AB (m²/s)")
        ax.set_title("Effect of Temperature on D_AB")
        ax.grid(True)
        st.pyplot(fig)

    # 📥 Download Report
    report = f"""
Binary Diffusion Coefficient Estimator Report
---------------------------------------------
Phase: {phase}
Model Used: {'Wilke–Chang' if phase == 'Liquid' else 'Fuller'}
Temperature: {T:.1f} K

Estimated D_AB: {D_AB_m2s:.4e} m²/s
"""
    st.download_button("📄 Download Report", report, file_name="diffusivity_estimation.txt")
