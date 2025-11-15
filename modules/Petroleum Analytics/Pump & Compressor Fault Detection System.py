# 📘 Module 7: Pump & Compressor Fault Detection | PetroStream AI Suite
# ⚙️ Detect abnormal behavior in rotating equipment using ML models
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import plotly.express as px

def run():
    st.set_page_config(page_title="⚙️ Fault Detection System", layout="wide")
    st.title("⚙️ Pump & Compressor Fault Detection")
    st.markdown("Real-time anomaly detection using pressure, temperature, and vibration sensor data.")

    st.sidebar.header("📥 Upload Sensor Dataset")
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        st.sidebar.info("No file uploaded. Simulating real-time sensor data...")
        np.random.seed(42)
        time = pd.date_range("2024-01-01", periods=100, freq="H")
        pressure = np.random.normal(5, 0.5, size=100)
        vibration = np.random.normal(0.2, 0.05, size=100)
        temperature = np.random.normal(65, 3, size=100)
        pressure[25] = 8    # Inject anomaly
        vibration[70] = 0.5
        temperature[80] = 80
        df = pd.DataFrame({
            "Timestamp": time,
            "Pressure (bar)": pressure,
            "Vibration (mm/s)": vibration,
            "Temperature (°C)": temperature
        })

    st.subheader("📊 Sensor Data Preview")
    st.dataframe(df.head(), use_container_width=True)

    # Drop timestamp for model
    data = df.drop(columns=["Timestamp"], errors="ignore")

    # Anomaly Detection with Isolation Forest
    model = IsolationForest(contamination=0.05, random_state=42)
    df["Anomaly"] = model.fit_predict(data)
    df["Anomaly"] = df["Anomaly"].map({1: "Normal", -1: "Anomaly"})

    st.subheader("🛠️ Anomaly Detection Result")
    fig = px.scatter(df, x=df.index, y="Pressure (bar)", color="Anomaly",
                     title="📉 Pressure Anomaly Detection", color_discrete_map={"Normal": "green", "Anomaly": "red"})
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.scatter(df, x=df.index, y="Vibration (mm/s)", color="Anomaly",
                      title="💥 Vibration Anomaly Detection", color_discrete_map={"Normal": "blue", "Anomaly": "red"})
    st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.scatter(df, x=df.index, y="Temperature (°C)", color="Anomaly",
                      title="🌡️ Temperature Anomaly Detection", color_discrete_map={"Normal": "orange", "Anomaly": "red"})
    st.plotly_chart(fig3, use_container_width=True)

