# 📘 Module 5: Catalyst Life Cycle Analyzer | PetroStream AI Suite
# ⏳ Analyze catalyst deactivation and estimate optimal replacement time
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def run():
    st.set_page_config(page_title="⏳ Catalyst Life Cycle Analyzer", layout="centered")
    st.title("⏳ Catalyst Life Cycle Analyzer")
    st.markdown("Model catalyst deactivation using real/simulated performance data and estimate optimal replacement time.")

    st.sidebar.header("📥 Input Options")
    data_mode = st.sidebar.radio("Data Source", ["📂 Upload CSV", "⚙️ Use Simulated Data"])

    if data_mode == "📂 Upload CSV":
        uploaded_file = st.sidebar.file_uploader("Upload Catalyst Performance Data", type=["csv"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
        else:
            st.info("📎 Please upload a CSV file with 'Time (days)' and 'Activity (%)'")
            return
    else:
        # Simulated Exponential Decay Data
        time = np.arange(0, 500, 10)
        activity = 100 * np.exp(-0.003 * time) + np.random.normal(0, 1, len(time))
        df = pd.DataFrame({"Time (days)": time, "Activity (%)": activity})

    st.subheader("📊 Catalyst Performance Data")
    st.dataframe(df.head(), use_container_width=True)

    # Define decay model: A(t) = A0 * exp(-k * t)
    def decay_model(t, A0, k):
        return A0 * np.exp(-k * t)

    try:
        popt, _ = curve_fit(decay_model, df["Time (days)"], df["Activity (%)"], p0=[100, 0.01])
        A0, k = popt
        df["Fitted Activity (%)"] = decay_model(df["Time (days)"], A0, k)
    except:
        st.error("❌ Curve fitting failed. Check if the data format is valid.")
        return

    # Plot actual vs fitted activity
    st.subheader("📈 Catalyst Deactivation Curve")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df["Time (days)"], df["Activity (%)"], "o", label="Actual Data")
    ax.plot(df["Time (days)"], df["Fitted Activity (%)"], "-", color="red", label="Exponential Fit")
    ax.set_xlabel("Time (days)")
    ax.set_ylabel("Activity (%)")
    ax.legend()
    st.pyplot(fig)

    st.markdown(f"**🧪 Initial Activity (A₀):** `{A0:.2f} %`")
    st.markdown(f"**🕒 Deactivation Rate Constant (k):** `{k:.5f} /day`")

    # Estimate replacement time
    threshold = st.slider("Set Activity Threshold for Replacement (%)", min_value=20, max_value=90, value=60)
    replacement_time = -np.log(threshold / A0) / k if k > 0 else np.nan

    st.metric("📆 Estimated Replacement Time", f"{replacement_time:.1f} days")

    # Download results
    st.subheader("📁 Download Fitted Data")
    csv = df.to_csv(index=False)
    st.download_button("⬇️ Download CSV", data=csv, file_name="catalyst_life_cycle.csv", mime="text/csv")
