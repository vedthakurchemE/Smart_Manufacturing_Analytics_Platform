# 📘 Module 4: Energy Loss Visualizer in Heat Exchangers | PetroStream AI Suite
# 🔥 Visualize thermal energy loss across exchangers (basic pinch + Sankey)
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt


def run():
    st.set_page_config(page_title="🔥 Energy Loss Visualizer", layout="centered")
    st.title("🔥 Energy Loss Visualizer in Heat Exchangers")
    st.markdown("Simulate and visualize energy loss in crude preheat trains or heat recovery networks.")

    st.sidebar.header("📥 Input Stream Data")
    uploaded_file = st.sidebar.file_uploader("Upload Stream Data CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        # Simulated data if no upload
        df = pd.DataFrame({
            "Stream": ["Crude A", "Crude B", "Product A", "Cooling Water"],
            "Type": ["Hot", "Hot", "Cold", "Cold"],
            "m_dot (kg/s)": [5.0, 3.0, 4.5, 6.0],
            "Cp (kJ/kg-K)": [2.1, 2.0, 2.2, 4.2],
            "T_in (°C)": [300, 280, 100, 30],
            "T_out (°C)": [200, 190, 250, 70]
        })

    st.subheader("📊 Stream Data")
    st.dataframe(df)

    # Heat duty calculation: Q = m * Cp * (T_in - T_out)
    df["Q (kW)"] = df["m_dot (kg/s)"] * df["Cp (kJ/kg-K)"] * abs(df["T_in (°C)"] - df["T_out (°C)"]) / 1000

    st.subheader("📈 Heat Duties (Q)")
    st.dataframe(df[["Stream", "Type", "Q (kW)"]])

    # === Sankey Diagram ===
    st.subheader("🔁 Sankey Diagram of Energy Flow")

    sources = []
    targets = []
    values = []
    labels = df["Stream"].tolist()

    hot_streams = df[df["Type"] == "Hot"]
    cold_streams = df[df["Type"] == "Cold"]

    for i, hot_row in hot_streams.iterrows():
        for j, cold_row in cold_streams.iterrows():
            q_transfer = min(hot_row["Q (kW)"], cold_row["Q (kW)"])
            sources.append(i)
            targets.append(j)
            values.append(round(q_transfer, 2))

    sankey_fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values
        ))])

    st.plotly_chart(sankey_fig, use_container_width=True)

    # === Energy Efficiency ===
    st.subheader("📉 Energy Summary")
    total_hot = hot_streams["Q (kW)"].sum()
    total_cold = cold_streams["Q (kW)"].sum()
    total_transferred = sum(values)

    recovery_efficiency = total_transferred / total_hot * 100 if total_hot > 0 else 0

    st.metric("🔥 Total Hot Stream Energy", f"{total_hot:.2f} kW")
    st.metric("❄️ Total Cold Stream Demand", f"{total_cold:.2f} kW")
    st.metric("🔁 Energy Recovered", f"{total_transferred:.2f} kW")
    st.metric("⚙️ Recovery Efficiency", f"{recovery_efficiency:.2f} %")

    # === Pinch Alert ===
    if recovery_efficiency < 50:
        st.warning("⚠️ Low energy recovery. Pinch analysis recommended.")
    elif recovery_efficiency < 80:
        st.info("ℹ️ Moderate energy recovery. Potential for improvement.")
    else:
        st.success("✅ Excellent energy recovery!")
