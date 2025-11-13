# 📘 Module 10: Gas Diffusion Loss Estimator | MassTransferAI Suite
# 🔍 Predict diffusion-based gas loss in tanks/pipes using Fick’s Law
# 👨‍💻 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import io

# 🌐 GAS DATABASE
GAS_DATA = {
    "Hydrogen (H2)": 2.016,
    "Methane (CH4)": 16.04,
    "Ammonia (NH3)": 17.03,
    "Oxygen (O2)": 32.00,
    "Carbon Dioxide (CO2)": 44.01
}

def run():
    st.title("🌬️ Gas Diffusion Loss Estimator")

    st.markdown("""
    Estimate **gas loss** due to molecular diffusion from **storage tanks** or **pipeline leaks** using **Fick’s Law**.

    📈 Powered by: `Real Gas Data`, `Time Simulation`, and `PDF Reporting`
    """)

    st.sidebar.header("📊 Input Parameters")

    gas_type = st.sidebar.selectbox("Select Gas", list(GAS_DATA.keys()))
    molar_mass = GAS_DATA[gas_type]

    A_cm2 = st.sidebar.number_input("Leak Area (cm²)", 0.1, 100.0, 10.0, 0.1)
    C1 = st.sidebar.number_input("Initial Gas Concentration (mol/m³)", 1.0, 200.0, 50.0, 1.0)
    D_cm2_s = st.sidebar.number_input("Diffusivity (cm²/s)", 0.01, 1.0, 0.24, 0.01)
    t_min = st.sidebar.slider("Time Duration (minutes)", 1, 300, 60, 1)
    length_cm = st.sidebar.slider("Distance of Leak Path (cm)", 1.0, 100.0, 10.0, 1.0)

    # 🔁 Unit Conversions
    A = A_cm2 / 1e4              # cm² to m²
    D = D_cm2_s / 1e4            # cm²/s to m²/s
    length = length_cm / 100.0   # cm to m
    t_sec = t_min * 60           # min to sec

    # 📐 Fick's First Law Calculation
    J = D * (C1 / length)        # mol/m²/s
    n_loss = J * A * t_sec       # mol
    mass_loss = n_loss * molar_mass  # g

    # 🔍 Output Summary
    st.subheader("📉 Diffusion Loss Results")
    col1, col2 = st.columns(2)
    col1.metric("Moles Lost", f"{n_loss:.2f} mol")
    col2.metric("Mass Lost", f"{mass_loss:.2f} g")

    # 📈 Time-series Plot
    time_array = np.linspace(0, t_sec, 100)
    loss_array = J * A * time_array
    fig, ax = plt.subplots()
    ax.plot(time_array / 60, loss_array, label="Moles Lost", color="crimson")
    ax.set_xlabel("Time (minutes)")
    ax.set_ylabel("Gas Lost (mol)")
    ax.set_title(f"{gas_type} Loss vs Time")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    # 📄 PDF Report Generator
    if st.button("📤 Generate PDF Report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, "Gas Diffusion Loss Report", ln=True, align='C')
        pdf.ln(10)
        pdf.multi_cell(0, 10, f"""
Gas Type: {gas_type}
Molar Mass: {molar_mass} g/mol

Leak Area: {A_cm2} cm²
Initial Concentration: {C1} mol/m³
Diffusivity: {D_cm2_s} cm²/s
Distance of Leak: {length_cm} cm
Time Duration: {t_min} minutes

Moles Lost: {n_loss:.2f} mol
Mass Lost: {mass_loss:.2f} g

Use: Estimating inventory loss from diffusion-based microleaks.
        """)
        pdf_output = io.BytesIO()
        pdf.output(pdf_output)
        st.download_button("📥 Download PDF", data=pdf_output.getvalue(), file_name="Gas_Diffusion_Report.pdf")

    # 🧠 Notes & Assumptions
    with st.expander("📘 Engineering Notes"):
        st.markdown(f"""
        - Based on **Fick’s First Law**: `J = -D * dC/dx`
        - Assumes **constant diffusivity** and **steady-state loss**
        - 📌 Adapt molar mass for different gases: Currently using **{gas_type}**
        - Use to:
            - Estimate **micro-leakage losses**
            - Build **inventory loss models**
            - Assist in **safety margin designs**
        """)
