# 📘 Module 4: Mass Transfer Coefficient Estimator | MassTransferAI Suite
# 📈 Estimate kL or kG using real-world correlations
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("🔁 Mass Transfer Coefficient Estimator")
    st.markdown(r"""
    Estimate mass transfer coefficient ($k_L$ or $k_G$) using empirical correlations.  
    Useful in packed beds, gas-liquid absorbers, tubes, etc.
    """)

    # --- Sidebar: Inputs ---
    st.sidebar.header("🔧 Input Parameters")
    phase = st.sidebar.radio("Phase", ["Liquid Phase (kL)", "Gas Phase (kG)"])
    D = st.sidebar.number_input("Diffusivity D (m²/s)", value=1e-9, format="%.1e", help="Binary diffusivity of species in fluid")
    d = st.sidebar.number_input("Characteristic Length d (m)", value=0.01)
    v = st.sidebar.number_input("Velocity v (m/s)", value=0.2)
    rho = st.sidebar.number_input("Density ρ (kg/m³)", value=1000.0)
    mu = st.sidebar.number_input("Viscosity μ (Pa·s)", value=0.001)
    correlation = st.sidebar.selectbox("Select Correlation", [
        "Dittus-Boelter (Turbulent Flow)",
        "Sieder-Tate (Viscous Flow)",
        "Whitman Penetration Theory"
    ])

    # --- Calculations ---
    Re = rho * v * d / mu
    Sc = mu / (rho * D)

    if correlation == "Dittus-Boelter (Turbulent Flow)":
        Sh = 0.023 * (Re ** 0.83) * (Sc ** 0.44)
        formula = r"Sh = 0.023 \cdot Re^{0.83} \cdot Sc^{0.44}"
    elif correlation == "Sieder-Tate (Viscous Flow)":
        Sh = 0.027 * (Re ** 0.8) * (Sc ** 0.33)
        formula = r"Sh = 0.027 \cdot Re^{0.8} \cdot Sc^{0.33}"
    else:  # Whitman
        Sh = 2  # approximate constant
        formula = r"Sh \approx 2 \text{ (Whitman Penetration Theory)}"

    k = Sh * D / d
    flow_regime = "Laminar" if Re < 2300 else "Turbulent"

    # --- Results ---
    st.subheader("📊 Results")
    col1, col2 = st.columns(2)
    col1.metric("Reynolds Number (Re)", f"{Re:.2f}")
    col2.metric("Schmidt Number (Sc)", f"{Sc:.2f}")
    st.metric("Sherwood Number (Sh)", f"{Sh:.2f}")
    st.metric("Flow Regime", flow_regime)

    if phase == "Liquid Phase (kL)":
        st.success(f"✅ Estimated Liquid Mass Transfer Coefficient kL = {k:.4e} m/s")
    else:
        st.success(f"✅ Estimated Gas Mass Transfer Coefficient kG = {k:.4e} m/s")

    # --- Theory ---
    with st.expander("📘 Theory & Correlation Used"):
        st.latex(formula)
        st.markdown("""
        - **Sh**: Sherwood Number  
        - **Re**: Reynolds Number  
        - **Sc**: Schmidt Number  
        - **k**: Mass Transfer Coefficient (m/s)  
        - Each correlation is used based on regime and conditions.
        """)

    # --- Plotting Sherwood vs Reynolds ---
    with st.expander("📉 Sherwood Number Trend"):
        Re_vals = np.linspace(100, 10000, 200)
        if correlation == "Dittus-Boelter (Turbulent Flow)":
            Sh_vals = 0.023 * Re_vals**0.83 * Sc**0.44
        elif correlation == "Sieder-Tate (Viscous Flow)":
            Sh_vals = 0.027 * Re_vals**0.8 * Sc**0.33
        else:
            Sh_vals = np.full_like(Re_vals, 2)
        fig, ax = plt.subplots()
        ax.plot(Re_vals, Sh_vals, label="Sherwood vs Reynolds", color="green")
        ax.set_xlabel("Reynolds Number (Re)")
        ax.set_ylabel("Sherwood Number (Sh)")
        ax.grid(True)
        st.pyplot(fig)

    # --- Report Generator ---
    report = f"""
Mass Transfer Coefficient Estimation Report
-----------------------------------------------
Phase: {phase}
Correlation Used: {correlation}
Flow Regime: {flow_regime}

Inputs:
Diffusivity (D): {D:.2e} m²/s
Length (d): {d:.4f} m
Velocity (v): {v:.3f} m/s
Density (ρ): {rho:.1f} kg/m³
Viscosity (μ): {mu:.4f} Pa·s

Results:
Re = {Re:.2f}
Sc = {Sc:.2f}
Sh = {Sh:.2f}
Estimated {'kL' if 'Liquid' in phase else 'kG'} = {k:.4e} m/s
"""
    st.download_button("📄 Download .txt Report", report, file_name="mass_transfer_coefficient.txt")
