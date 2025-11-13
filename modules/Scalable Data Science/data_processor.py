# 📦 Module 2: Data Processor | SensorGuardAI Suite
# 🔧 Scales sensor data (Temp, Pressure, FlowRate) for ML pipeline
# 📦 Author: Ved Thakur | BTech ChemEng | IPS Academy Indore

import pandas as pd
from sklearn.preprocessing import StandardScaler
import streamlit as st

# Create a global StandardScaler instance
scaler = StandardScaler()

def process_batch(data_batch):
    """
    Process a list of sensor data dicts into a scaled DataFrame.

    Args:
        data_batch (list of dict): List of sensor data rows.

    Returns:
        pd.DataFrame: Original + scaled features + ready for ML
    """
    try:
        # Convert to DataFrame
        df = pd.DataFrame(data_batch)

        # Validate required columns
        required = ["Temperature", "Pressure", "FlowRate"]
        if not all(col in df.columns for col in required):
            raise ValueError("Missing required columns in input data.")

        # Scale data
        scaled = scaler.fit_transform(df[required])
        df_scaled = pd.DataFrame(scaled, columns=["Temp_scaled", "Press_scaled", "Flow_scaled"])

        # Merge and return
        final_df = pd.concat([df.reset_index(drop=True), df_scaled], axis=1)
        return final_df

    except Exception as e:
        st.error(f"❌ Data Processor Error: {e}")
        return pd.DataFrame()


def run():
    """
    Demo runner for Module 2 using Streamlit.
    Takes user input of sensor data and shows scaled output.
    """
    st.header("🔧 Sensor Data Processor Demo")
    st.markdown("This module scales sensor input for ML using StandardScaler.")

    sample_data = [
        {"Temperature": 75, "Pressure": 10.2, "FlowRate": 300},
        {"Temperature": 140, "Pressure": 30.1, "FlowRate": 500},
        {"Temperature": 73, "Pressure": 10.0, "FlowRate": 302},
        {"Temperature": 76, "Pressure": 10.5, "FlowRate": 295},
    ]

    if st.button("⚙️ Run Processing on Sample Data"):
        processed = process_batch(sample_data)
        st.subheader("📈 Processed & Scaled Data")
        st.dataframe(processed, use_container_width=True)
