# 📘 Module 6: Packed Column Simulator | MassTransferAI Suite
# 🏭 Simulate absorption/stripping in packed beds using NTU-HTU method
# 👨‍💻 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO


def run():
    st.title("🏭 Packed Column Simulator (Absorber/Stripper)")

    st.markdown("""
    Simulate a **packed mass transfer column** using the NTU-HTU method.  
    📌 Predict required **column height**, visualize operating/equilibrium lines, and download full simulation report.

    🌐 Ideal for **gas-liquid absorption**, **stripping**, and **solvent extraction** processes.
    """)

    st.sidebar.header("🔧 Column & Process Settings")
    process_type = st.sidebar.radio("Select Process Type", ["Absorption", "Stripping"])

    st.subheader("🔢 Input Parameters")

    col1, col2 = st.columns(2)
    with col1:
        G = st.number_input("Gas Flow Rate (mol/m²·s)", value=2.5, format="%.3f")
        y_in = st.number_input("Inlet Gas Mole Fraction (yₐ,in)", value=0.15, min_value=0.0, max_value=1.0)
        m = st.number_input("Equilibrium Line Slope (m)", value=1.1)
    with col2:
        L = st.number_input("Liquid Flow Rate (mol/m²·s)", value=1.2, format="%.3f")
        y_out = st.number_input("Outlet Gas Mole Fraction (yₐ,out)", value=0.02, min_value=0.0, max_value=1.0)
        HTU = st.number_input("HTU (Height of Transfer Unit) [m]", value=0.5, min_value=0.01)

    st.markdown("---")

    # === NTU and Height Calculation
    try:
        A = m * L / G
        NTU = (1 / (A - 1)) * np.log(
            ((y_in - m * y_out) * (1 - y_out)) /
            ((y_out - m * y_in) * (1 - y_in))
        )
        Z = HTU * NTU
        st.success(f"✅ **Required Packed Bed Height**: `{Z:.2f} meters`")
        st.info(f"🔁 **Number of Transfer Units (NTU)**: `{NTU:.2f}`")
    except:
        st.error("❌ Invalid input or math error! Please check the flow rates and mole fractions.")
        return

    # === Plot Operating and Equilibrium Lines
    st.subheader("📈 Operating vs. Equilibrium Line")

    y_vals = np.linspace(y_out, y_in, 100)
    x_vals_eq = y_vals / m  # Equilibrium Line
    x_vals_op = (L / G) * y_vals + (0 - (L / G) * y_in)  # Operating Line

    fig, ax = plt.subplots()
    ax.plot(x_vals_eq, y_vals, label="Equilibrium Line", color="blue", linewidth=2)
    ax.plot(x_vals_op, y_vals, label="Operating Line", color="green", linestyle="--", linewidth=2)
    ax.set_xlabel("x (Liquid Phase Mole Fraction)")
    ax.set_ylabel("y (Gas Phase Mole Fraction)")
    ax.set_title("Equilibrium vs. Operating Line")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    # === Engineering Notes
    with st.expander("📘 Engineering Note"):
        st.markdown("""
        - The **HTU** depends on packing type, fluid properties, and system temperature.
        - A **lower NTU** implies higher efficiency; consider optimizing gas-liquid ratios.
        - For design, keep a **safety factor of 10-20%** over the calculated height.
        - Ensure **column flooding & loading checks** during final mechanical design.

        🔗 *Refer to Treybal’s or Geankoplis' Mass Transfer books for theoretical background.*
        """)

    # === Downloadable Report
    st.subheader("📄 Simulation Report")
    report = f"""
Packed Column Simulation Report
-------------------------------
Process Type       : {process_type}
Gas Flow Rate (G)  : {G} mol/m²·s
Liquid Flow Rate (L): {L} mol/m²·s
Inlet yₐ (Gas)     : {y_in}
Outlet yₐ (Gas)    : {y_out}
Equilibrium Slope (m): {m}
HTU                : {HTU} m
NTU                : {NTU:.2f}
Packed Height (Z)  : {Z:.2f} m
"""
    st.download_button("⬇️ Download Report as TXT", report, file_name="packed_column_report.txt")
