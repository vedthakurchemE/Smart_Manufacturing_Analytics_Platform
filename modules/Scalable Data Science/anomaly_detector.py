# 📦 Module 3: Anomaly Detector | SensorGuardAI Suite
# 🚨 Detects sensor anomalies using Isolation Forest (unsupervised)
# 📦 Author: Ved Thakur | BTech ChemEng | IPS Academy Indore

import pandas as pd
from sklearn.ensemble import IsolationForest
import streamlit as st

# Create Isolation Forest model globally (can be reused)
model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)

def detect_anomalies(df):
    """
    Detect anomalies in scaled sensor data using Isolation Forest.

    Args:
        df (pd.DataFrame): DataFrame with 'Temp_scaled', 'Press_scaled', 'Flow_scaled'

    Returns:
        pd.DataFrame: Original DataFrame + 'anomaly' and 'status' columns
    """
    try:
        # Ensure required scaled columns exist
        required = ["Temp_scaled", "Press_scaled", "Flow_scaled"]
        if not all(col in df.columns for col in required):
            raise ValueError("❌ Required scaled columns not found for anomaly detection.")

        features = df[required]
        df["anomaly"] = model.fit_predict(features)  # -1 = anomaly, 1 = normal

        df["status"] = df["anomaly"].apply(lambda x: "⚠️ Fault" if x == -1 else "✅ Normal")

        return df

    except Exception as e:
        st.error(f"❌ Anomaly Detection Error: {e}")
        return df


def run():
    """
    Streamlit demo runner for anomaly detection module.
    Uses sample processed data and visualizes anomaly labels.
    """
    st.header("🚨 Anomaly Detector Demo")
    st.markdown("Detects faults in scaled sensor data using Isolation Forest.")

    # Sample pre-processed scaled data
    sample_df = pd.DataFrame({
        "Temperature": [75, 140, 73, 76],
        "Pressure": [10.2, 30.1, 10.0, 10.5],
        "FlowRate": [300, 500, 302, 295],
        "Temp_scaled": [-0.36, 1.91, -0.48, -0.22],
        "Press_scaled": [-0.45, 2.0, -0.51, -0.41],
        "Flow_scaled": [-0.29, 1.99, -0.16, -0.54]
    })

    if st.button("🚨 Detect Anomalies"):
        result_df = detect_anomalies(sample_df)
        st.subheader("🔍 Labeled Data")
        st.dataframe(result_df, use_container_width=True)
