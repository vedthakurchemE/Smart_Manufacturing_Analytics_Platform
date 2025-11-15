# 📘 Module 7: Boiling Heat Transfer Estimator | HeatTransferAI Suite
# 🔥 Estimate boiling heat transfer coefficients using Rohsenow correlation
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.set_page_config(page_title="🔥 Boiling Heat Transfer Estimator", layout="centered")
    st.title("🔥 Boiling Heat Transfer Estimator")
    st.markdown("Estimate **boiling heat transfer coefficient** using the **Rohsenow correlation** for nucleate boiling in vertical or horizontal surfaces.")
    st.caption("📘 Based on empirical relation used in boiling heat transfer analysis")

    with st.expander("ℹ️ What is Rohsenow Correlation?"):
        st.markdown("""
        The **Rohsenow correlation** estimates boiling heat transfer by relating wall superheat to surface and fluid properties.  
        It’s widely used in chemical, thermal, and mechanical systems involving phase change and nucleate boiling.
        """)

    # === Input Parameters ===
    st.subheader("🔢 Input Parameters")

    col1, col2 = st.columns(2)
    with col1:
        q_flux = st.number_input("🔸 Heat Flux (q\") [W/m²]", min_value=0.0, value=1e5, step=1000.0, help="Energy per unit area per second supplied to the surface")
        h_fg = st.number_input("🔸 Latent Heat (h_fg) [J/kg]", min_value=0.0, value=2.26e6, step=1e4, help="Heat required to convert liquid to vapor")
        c_pl = st.number_input("🔸 Specific Heat of Liquid (c_pl) [J/kg·K]", min_value=0.0, value=4180.0, step=10.0)
        mu_l = st.number_input("🔸 Viscosity (μ_l) [Pa·s]", min_value=0.0, value=0.001, step=0.0001, format="%.5f")
        sigma = st.number_input("🔸 Surface Tension (σ) [N/m]", min_value=0.0, value=0.072, step=0.001)

    with col2:
        g = st.number_input("🔹 Gravity (g) [m/s²]", min_value=0.0, value=9.81, step=0.1)
        rho_l = st.number_input("🔹 Liquid Density (ρ_l) [kg/m³]", min_value=0.0, value=997.0, step=10.0)
        rho_v = st.number_input("🔹 Vapor Density (ρ_v) [kg/m³]", min_value=0.0, value=0.6, step=0.1)
        Pr = st.number_input("🔹 Prandtl Number (Pr)", min_value=0.0, value=3.5, step=0.1)
        C_sf = st.number_input("🔹 Surface-Fluid Constant (C_sf)", min_value=0.0, value=0.013, step=0.001)
        n = st.number_input("🔹 Exponent (n)", min_value=0.0, value=1.7, step=0.1)

    # === Calculate ===
    if st.button("📊 Estimate Heat Transfer Coefficient"):
        try:
            delta_T = ((q_flux / (C_sf * (mu_l ** n) * (c_pl ** n))) *
                      ((sigma / (g * (rho_l - rho_v))) ** 0.5) * (1 / (h_fg ** (2 + n)))) ** (1 / (3 + n))
            h = q_flux / delta_T

            st.success(f"✅ Estimated Heat Transfer Coefficient: **{h:.2f} W/m²·K**")
            st.markdown(f"🌡️ Wall Superheat (ΔT): **{delta_T:.2f} K**")

            # === Plot Heat Flux vs Superheat ===
            st.subheader("📈 Heat Flux vs Superheat Plot")
            delta_T_range = np.linspace(delta_T * 0.5, delta_T * 2, 100)
            h_range = q_flux / delta_T_range

            fig, ax = plt.subplots()
            ax.plot(delta_T_range, h_range, label="h vs ΔT", color="crimson")
            ax.set_xlabel("Wall Superheat ΔT (K)")
            ax.set_ylabel("Heat Transfer Coefficient h (W/m²·K)")
            ax.set_title("Boiling Heat Transfer Coefficient vs Superheat")
            ax.grid(True)
            ax.legend()
            st.pyplot(fig)

        except Exception as e:
            st.error(f"⚠️ Calculation error: {e}")

