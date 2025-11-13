# 📘 Module 1: Heat Exchanger Designer | HeatTransferAI Suite
# 🧊 Design shell-and-tube heat exchangers using LMTD or NTU methods
# 🧠 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# === Heat Capacity Database (kJ/kg.K) ===
fluid_cp = {
    "Water": 4.18,
    "Oil": 2.10,
    "Air": 1.00
}

# === LMTD Formula ===
def calculate_lmtd(Th_in, Th_out, Tc_in, Tc_out):
    dT1 = Th_in - Tc_out
    dT2 = Th_out - Tc_in
    if dT1 == dT2:
        return dT1
    elif dT1 > 0 and dT2 > 0:
        return (dT1 - dT2) / np.log(dT1 / dT2)
    else:
        return 0

# === NTU Method Formula ===
def effectiveness_NTU(Cr, NTU, flow_type="counter"):
    if flow_type == "counter":
        if Cr == 1:
            return NTU / (1 + NTU)
        else:
            return (1 - np.exp(-NTU * (1 - Cr))) / (1 - Cr * np.exp(-NTU * (1 - Cr)))
    else:
        return (1 - np.exp(-NTU * (1 + Cr))) / (1 + Cr)

# === App ===
def run():
    st.set_page_config(page_title="Heat Exchanger Designer", layout="wide")
    st.title("🌡️ Heat Exchanger Designer")
    st.markdown("Design a heat exchanger using **LMTD** or **NTU** methods, with cost estimation and fluid property presets.")

    st.sidebar.header("⚙️ Design Settings")
    method = st.sidebar.radio("Choose Design Method", ["LMTD", "NTU"])
    flow_type = st.sidebar.selectbox("Flow Type", ["counter", "parallel"])
    fluid_hot = st.sidebar.selectbox("Hot Fluid", list(fluid_cp.keys()))
    fluid_cold = st.sidebar.selectbox("Cold Fluid", list(fluid_cp.keys()))
    swap = st.sidebar.checkbox("🔄 Swap Hot and Cold Fluids", value=False)

    # === Default Inputs ===
    m_hot = st.sidebar.slider("Mass Flow Rate (Hot Fluid) [kg/s]", 0.1, 20.0, 2.0)
    m_cold = st.sidebar.slider("Mass Flow Rate (Cold Fluid) [kg/s]", 0.1, 20.0, 3.0)
    Cp_hot = fluid_cp[fluid_hot]
    Cp_cold = fluid_cp[fluid_cold]

    if swap:
        m_hot, m_cold = m_cold, m_hot
        Cp_hot, Cp_cold = Cp_cold, Cp_hot
        fluid_hot, fluid_cold = fluid_cold, fluid_hot

    # === Temperature Inputs ===
    with st.sidebar.expander("🌡️ Fluid Temperatures"):
        if method == "LMTD":
            Th_in = st.number_input("Hot Fluid Inlet Temp [°C]", 20.0, 500.0, 150.0)
            Th_out = st.number_input("Hot Fluid Outlet Temp [°C]", 10.0, 490.0, 100.0)
            Tc_in = st.number_input("Cold Fluid Inlet Temp [°C]", 0.0, 200.0, 30.0)
            Tc_out = st.number_input("Cold Fluid Outlet Temp [°C]", 10.0, 300.0, 80.0)
        else:
            Th_in = st.number_input("Hot Fluid Inlet Temp [°C]", 20.0, 300.0, 140.0)
            Tc_in = st.number_input("Cold Fluid Inlet Temp [°C]", 0.0, 200.0, 25.0)

    # === Calculations ===
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Heat Exchanger Results")
        if method == "LMTD":
            Q = m_hot * Cp_hot * (Th_in - Th_out) * 1000
            LMTD = calculate_lmtd(Th_in, Th_out, Tc_in, Tc_out)
            U = st.sidebar.slider("Overall Heat Transfer Coefficient [W/m²·K]", 10, 2000, 500)
            A = Q / (U * LMTD) if LMTD > 0 else 0
            cost = A * 1200  # Cost in ₹ (example)

            results = {
                "Method": "LMTD",
                "Q (kW)": Q / 1000,
                "LMTD (°C)": LMTD,
                "Area (m²)": A,
                "Cost Estimate (₹)": cost
            }

        else:
            C_hot = m_hot * Cp_hot
            C_cold = m_cold * Cp_cold
            C_min = min(C_hot, C_cold)
            C_max = max(C_hot, C_cold)
            Cr = C_min / C_max
            NTU = st.sidebar.slider("NTU", 0.1, 5.0, 1.0, 0.1)
            effectiveness = effectiveness_NTU(Cr, NTU, flow_type)
            Q_max = C_min * (Th_in - Tc_in) * 1000
            Q = effectiveness * Q_max
            Tc_out = Tc_in + Q / (m_cold * Cp_cold * 1000)
            Th_out = Th_in - Q / (m_hot * Cp_hot * 1000)
            cost = NTU * 5000  # Approx cost (NTU related)

            results = {
                "Method": "NTU",
                "Q (kW)": Q / 1000,
                "Effectiveness": effectiveness,
                "Hot Outlet (°C)": Th_out,
                "Cold Outlet (°C)": Tc_out,
                "Cost Estimate (₹)": cost
            }

        df = pd.DataFrame(results.items(), columns=["Parameter", "Value"])
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False)
        st.download_button("📥 Download CSV", csv, "heat_exchanger_results.csv", "text/csv")

    # === Theory ===
    with col2:
        with st.expander("📘 Method Theory", expanded=False):
            if method == "LMTD":
                st.markdown("""
                - **LMTD** = \\( \\frac{ΔT_1 - ΔT_2}{\\ln(ΔT_1 / ΔT_2)} \\)
                - Used when inlet & outlet temperatures are known.
                """)
            else:
                st.markdown("""
                - **NTU Method:**  
                  \\( ε = \\frac{Q}{Q_{max}} \\)  
                  \\( NTU = \\frac{UA}{C_{min}} \\)  
                - Used when exit temps are unknown.
                """)

        st.subheader("📈 Temperature Profile")
        fig, ax = plt.subplots()
        x = [0, 1]
        if method == "LMTD":
            ax.plot(x, [Th_in, Th_out], 'r-o', label=f'Hot: {fluid_hot}')
            ax.plot(x, [Tc_in, Tc_out], 'b-o', label=f'Cold: {fluid_cold}')
        else:
            ax.plot(x, [Th_in, Th_out], 'r-o', label=f'Hot: {fluid_hot}')
            ax.plot(x, [Tc_in, Tc_out], 'b-o', label=f'Cold: {fluid_cold}')
        ax.set_xlabel("Exchanger Length (Normalized)")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title("Fluid Temperature Profiles")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
