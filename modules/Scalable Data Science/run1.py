# 📘 run.py - Scalable Data Science Module | AllProjectsSuite
# ⚙️ Simulates batch & real-time data handling
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import pandas as pd
import numpy as np
import time

def run():
    # === Page Config ===
    st.set_page_config(page_title="⚙️ Scalable Data Science App", layout="wide")

    # === App Header ===
    st.title("⚙️ Scalable Data Science App")
    st.markdown("""
    This module demonstrates **scalable data science** concepts using Python, Pandas, and simulated big data streams.

    🧪 Use-cases:
    - Batch vs Streaming simulation
    - Real-time rolling stats
    - Synthetic large dataset generation
    - Scalable dashboard with Streamlit

    📦 **Author**: Ved Thakur  
    🏫 IPS Academy Indore  
    🎯 Part of: AllProjectsSuite
    ---
    """)

    # === Generate Large Synthetic Dataset ===
    st.header("🧪 Synthetic Data Generator")
    num_rows = st.slider("Select number of rows to simulate", 1000, 1000000, step=10000)

    if st.button("Generate Dataset"):
        st.info("Generating dataset...")
        df = pd.DataFrame({
            'timestamp': pd.date_range(start='2025-01-01', periods=num_rows, freq='S'),
            'sensor_A': np.random.randn(num_rows),
            'sensor_B': np.random.randn(num_rows) * 2 + 5
        })
        st.success(f"✅ Generated {num_rows} rows!")
        st.write(df.head())

        # Show summary
        st.subheader("📊 Summary Statistics")
        st.write(df.describe())

        # Live line chart (first 1000 points)
        st.subheader("📈 Real-Time Simulation (Sensor A)")
        st.line_chart(df['sensor_A'].head(1000))

    # === Stream Simulation (Rolling Stats) ===
    st.header("📡 Simulated Streaming with Rolling Stats")

    stream_len = st.slider("Streaming Window Size", 10, 500, 100)

    if st.button("Start Simulated Stream"):
        st.info("Simulating real-time data stream...")
        placeholder = st.empty()

        data = []

        for i in range(stream_len):
            new_val = np.random.randn()
            data.append(new_val)
            if len(data) > 50:
                data.pop(0)

            df_stream = pd.DataFrame(data, columns=['Sensor A'])
            placeholder.line_chart(df_stream)
            time.sleep(0.05)

        st.success("✅ Stream Complete")

    st.markdown("---")
    st.markdown("🚀 *This module simulates scalable data workloads for real-time + batch analytics.*")
