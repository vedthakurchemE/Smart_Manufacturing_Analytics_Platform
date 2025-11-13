# 📦 Module 1: Stream Simulator | SensorGuardAI Suite
# 🌀 Simulates Kafka-style streaming of sensor data from a CSV file
# 📦 Author: Ved Thakur | BTech ChemEng | IPS Academy Indore

import pandas as pd
import time
import io
import streamlit as st

def stream_data(csv_input, delay=1.0):
    """
    Generator function to stream sensor data row by row with delay.

    Args:
        csv_input (str or file-like): Path or uploaded file-like object
        delay (float): Delay between data points (in seconds)

    Yields:
        dict: A single row of sensor data as a dictionary
    """
    try:
        if isinstance(csv_input, str):
            df = pd.read_csv(csv_input)
        elif hasattr(csv_input, 'read'):
            content = csv_input.read()
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            df = pd.read_csv(io.StringIO(content))
        else:
            raise ValueError("❌ Invalid input. Provide file path or file-like object.")

        required_cols = {"Temperature", "Pressure", "FlowRate"}
        if not required_cols.issubset(df.columns):
            raise ValueError(f"❌ CSV must contain columns: {required_cols}")

        for _, row in df.iterrows():
            yield row.to_dict()
            time.sleep(delay)

    except Exception as e:
        st.error(f"❌ Stream Simulator Error: {e}")
        yield None


def run():
    """
    Streamlit-compatible demo runner for stream simulator module.
    Uploads CSV and streams 10 rows to console with delay.
    """
    st.header("🌀 Stream Simulator Demo")
    st.markdown("Simulates real-time streaming of chemical plant sensor data.")

    uploaded_file = st.file_uploader("📁 Upload Sensor CSV", type=["csv"])
    delay = st.slider("⏱️ Delay between rows (seconds)", 0.1, 3.0, 1.0)

    if uploaded_file and st.button("▶️ Start Simulation"):
        st.success("✅ Streaming started...")
        data_gen = stream_data(uploaded_file, delay=delay)

        for i in range(10):
            data = next(data_gen, None)
            if data:
                st.write(f"📡 Data Point {i+1}:", data)
            else:
                st.warning("⚠️ No more data or error in stream.")
                break
