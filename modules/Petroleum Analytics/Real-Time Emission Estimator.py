# 📘 Module 3: Real-Time Emission Estimator | PetroStream AI Suite
# 🌫️ Estimate CO₂, NOx, SOx emissions from process units using live/simulated data
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import StringIO

def run():
    st.set_page_config(page_title="🌫️ Emission Estimator", layout="wide")
    st.title("🌫️ Real-Time Emission Estimator")
    st.markdown("Estimate emissions (CO₂, NOx, SOx) using fuel flow and excess air data from sensors or CSV.")

    # === Sidebar Configuration ===
    st.sidebar.header("📥 Upload or Simulate Data")

    data_option = st.sidebar.radio("Choose Input Method", ["📂 Upload CSV", "⚙️ Use Simulated Sensor Data"])

    if data_option == "📂 Upload CSV":
        uploaded_file = st.sidebar.file_uploader("Upload sensor data CSV", type=["csv"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
        else:
            st.info("📎 Please upload a CSV file.")
            return
    else:
        # Simulate Data
        time = pd.date_range(start="2025-01-01", periods=100, freq="H")
        fuel_flow = np.random.normal(200, 10, size=100)
        excess_air = np.random.normal(15, 2, size=100)
        df = pd.DataFrame({
            "Timestamp": time,
            "Fuel Flow (kg/hr)": fuel_flow,
            "Excess Air (%)": excess_air
        })

    st.subheader("📊 Input Data")
    st.dataframe(df.head(), use_container_width=True)

    # === Emission Estimation ===
    st.subheader("🧪 Estimated Emissions")
    fuel_factor_co2 = 3.14     # kg CO₂ / kg fuel
    fuel_factor_nox = 0.0008   # kg NOx / kg fuel
    fuel_factor_sox = 0.0015   # kg SOx / kg fuel

    df["CO2 (kg/hr)"] = df["Fuel Flow (kg/hr)"] * fuel_factor_co2
    df["NOx (kg/hr)"] = df["Fuel Flow (kg/hr)"] * fuel_factor_nox * (1 + df["Excess Air (%)"] / 100)
    df["SOx (kg/hr)"] = df["Fuel Flow (kg/hr)"] * fuel_factor_sox

    st.line_chart(df.set_index("Timestamp")[["CO2 (kg/hr)", "NOx (kg/hr)", "SOx (kg/hr)"]])

    st.markdown("✅ **Estimation complete based on standard emission factors.**")

    # === Summary Metrics ===
    st.subheader("📈 Summary")
    avg_emissions = df[["CO2 (kg/hr)", "NOx (kg/hr)", "SOx (kg/hr)"]].mean().round(2)
    st.metric("💨 Average CO₂ Emission", f"{avg_emissions['CO2 (kg/hr)']} kg/hr")
    st.metric("🌫️ Average NOx Emission", f"{avg_emissions['NOx (kg/hr)']} kg/hr")
    st.metric("🛢️ Average SOx Emission", f"{avg_emissions['SOx (kg/hr)']} kg/hr")

