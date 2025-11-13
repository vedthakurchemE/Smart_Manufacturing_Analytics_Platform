# 📦 Module 4: Dashboard View | SensorGuardAI Suite
# 📊 Real-time visualization of sensor trends and fault alerts
# 📦 Author: Ved Thakur | BTech ChemEng | IPS Academy Indore

import streamlit as st
import matplotlib.pyplot as plt

def show_dashboard(df):
    """
    Displays real-time sensor data, plots, and fault alerts.

    Args:
        df (pd.DataFrame): DataFrame with original and anomaly columns
    """
    st.subheader("📡 Live Sensor Data Stream")
    st.dataframe(df.tail(10), use_container_width=True)

    st.subheader("📈 Sensor Trends Over Time")

    sensor_cols = ["Temperature", "Pressure", "FlowRate"]

    for sensor in sensor_cols:
        fig, ax = plt.subplots()
        ax.plot(df[sensor], marker='o', linestyle='-', label=sensor, color='teal')
        ax.set_xlabel("Sample Index")
        ax.set_ylabel(sensor)
        ax.set_title(f"{sensor} Trend")
        ax.grid(True)
        st.pyplot(fig)

    st.subheader("🚨 Detected Faults")
    fault_df = df[df["status"] == "⚠️ Fault"]
    if not fault_df.empty:
        st.error(f"⚠️ {len(fault_df)} fault(s) detected")
        st.dataframe(fault_df, use_container_width=True)
    else:
        st.success("✅ No faults detected in recent data.")


def run():
    """
    Streamlit demo runner for the dashboard module using sample labeled data.
    """
    import pandas as pd

    st.header("📊 Dashboard Viewer Demo")
    st.markdown("Visualizes sensor data and highlights anomaly status.")

    # Sample labeled data
    sample_df = pd.DataFrame({
        "Temperature": [75, 140, 73, 76],
        "Pressure": [10.2, 30.1, 10.0, 10.5],
        "FlowRate": [300, 500, 302, 295],
        "Temp_scaled": [-0.36, 1.91, -0.48, -0.22],
        "Press_scaled": [-0.45, 2.0, -0.51, -0.41],
        "Flow_scaled": [-0.29, 1.99, -0.16, -0.54],
        "anomaly": [1, -1, 1, 1],
        "status": ["✅ Normal", "⚠️ Fault", "✅ Normal", "✅ Normal"]
    })

    if st.button("📊 Show Sample Dashboard"):
        show_dashboard(sample_df)
