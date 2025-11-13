# 📦 Module 6: Logger | SensorGuardAI Suite
# 📝 Logs real-time sensor readings + anomalies to a CSV or in-memory DataFrame
# 📦 Author: Ved Thakur | BTech ChemEng | IPS Academy Indore

import pandas as pd
import os
import streamlit as st
from datetime import datetime

LOG_FILE = "logs/sensor_log.csv"

def log_data(df, log_path=LOG_FILE):
    """
    Appends sensor data (with anomaly status) to a persistent CSV log file.

    Args:
        df (pd.DataFrame): Final processed DataFrame with status column.
        log_path (str): Path to save the log file (default: logs/sensor_log.csv)

    Returns:
        bool: True if saved successfully.
    """
    try:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        # Add timestamp
        df["log_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Append to CSV
        if os.path.exists(log_path):
            df.to_csv(log_path, mode='a', header=False, index=False)
        else:
            df.to_csv(log_path, mode='w', header=True, index=False)

        st.success(f"📁 Logged {len(df)} rows to `{log_path}`")
        return True

    except Exception as e:
        st.error(f"❌ Logging Error: {e}")
        return False


def run():
    """
    Streamlit demo runner for Logger module.
    Creates a small sensor log and appends to CSV file.
    """
    st.header("📝 Logger Demo")
    st.markdown("Log your sensor data + fault labels to CSV file.")

    # Sample data
    df = pd.DataFrame({
        "Temperature": [72, 150],
        "Pressure": [10.3, 32.0],
        "FlowRate": [310, 490],
        "Temp_scaled": [-0.4, 2.0],
        "Press_scaled": [-0.5, 2.1],
        "Flow_scaled": [-0.2, 1.8],
        "anomaly": [1, -1],
        "status": ["✅ Normal", "⚠️ Fault"]
    })

    if st.button("📝 Log Sample Data"):
        logged = log_data(df)
        if logged:
            st.info("✅ Sample logged! Check `logs/sensor_log.csv`.")
