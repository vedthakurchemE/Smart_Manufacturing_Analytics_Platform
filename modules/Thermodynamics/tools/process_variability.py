# 📊 Process Variability Analyzer (Streamlit + SPC Charts)
# 🔧 Part of PetroStream AI Suite
# 👨‍💻 Author: Ved Thakur

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import numpy as np
import threading

# For thread-safe plotting
_lock = threading.Lock()

def run():
    st.set_page_config(page_title="📊 Process Variability Analyzer", layout="wide")
    st.title("📊 Process Variability Analyzer")
    st.markdown(
        """
        Analyze and visualize process variation using **Statistical Process Control (SPC)**.
        Upload a CSV with at least one time/date column and one numeric process variable.
        """
    )

    # === Upload Section ===
    uploaded_file = st.file_uploader("📁 Upload Time-Series Process Data (.csv)", type=["csv"])

    if not uploaded_file:
        st.info("📤 Please upload a `.csv` file to get started.")
        return

    try:
        # === Data Read & Preview ===
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")
        st.dataframe(df.head(), use_container_width=True)

        # === Column Detection ===
        numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
        time_col = next((col for col in df.columns if 'time' in col.lower() or 'date' in col.lower()), None)

        if not time_col or not numeric_cols:
            st.warning("⚠️ CSV must contain at least one time/date column and one numeric column.")
            return

        # === Time Preprocessing ===
        df[time_col] = pd.to_datetime(df[time_col], errors='coerce')
        df = df.dropna(subset=[time_col])
        df = df.sort_values(by=time_col)

        # === User Inputs ===
        metric = st.selectbox("📈 Select Variable to Analyze", numeric_cols)
        rolling_window = st.slider("🌀 Rolling Window Size", 2, 50, value=5)
        sigma_level = st.slider("🔧 Sigma Control Limits", 1.0, 4.0, value=3.0, step=0.5)

        # === SPC Calculation ===
        df['Mean'] = df[metric].rolling(window=rolling_window).mean()
        df['StdDev'] = df[metric].rolling(window=rolling_window).std()
        df['UCL'] = df['Mean'] + sigma_level * df['StdDev']
        df['LCL'] = df['Mean'] - sigma_level * df['StdDev']
        df['Out of Control'] = (df[metric] > df['UCL']) | (df[metric] < df['LCL'])

        out_of_control = df[df['Out of Control']]
        percent_ooc = (len(out_of_control) / len(df)) * 100 if len(df) > 0 else 0
        max_dev = np.abs(df[metric] - df['Mean']).max()

        # === Metrics Display ===
        col1, col2, col3 = st.columns(3)
        col1.metric("🚨 Out of Control Points", f"{len(out_of_control)}")
        col2.metric("📉 Max Deviation", f"{max_dev:.2f}")
        col3.metric("📊 % Out of Control", f"{percent_ooc:.2f} %")

        # === SPC Chart ===
        st.subheader("📊 SPC Control Chart")

        with _lock:
            fig, ax = plt.subplots(figsize=(14, 6))
            sns.lineplot(x=df[time_col], y=df[metric], label="Process Value", marker="o", ax=ax)
            ax.plot(df[time_col], df["Mean"], color="green", label="Mean")
            ax.plot(df[time_col], df["UCL"], color="red", linestyle="--", label=f"UCL (+{sigma_level}σ)")
            ax.plot(df[time_col], df["LCL"], color="orange", linestyle="--", label=f"LCL (-{sigma_level}σ)")
            ax.fill_between(df[time_col], df["LCL"], df["UCL"], color="gray", alpha=0.1)

            # Highlight out-of-control points
            ax.scatter(out_of_control[time_col], out_of_control[metric],
                       color='red', s=60, zorder=5, label='Out of Control')

            ax.set_title("SPC Control Chart")
            ax.set_xlabel("Time")
            ax.set_ylabel(metric)
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

        # === Export Options ===
        st.subheader("📤 Export Results")

        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        st.download_button(
            "⬇️ Download CSV Report",
            data=csv_buffer.getvalue(),
            file_name="spc_analysis_report.csv",
            mime="text/csv"
        )

        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format="png")
        st.download_button(
            "🖼️ Download Chart Image",
            data=img_buffer.getvalue(),
            file_name="spc_chart.png",
            mime="image/png"
        )

    except Exception as e:
        st.error(f"❌ An unexpected error occurred:\n\n{e}")
