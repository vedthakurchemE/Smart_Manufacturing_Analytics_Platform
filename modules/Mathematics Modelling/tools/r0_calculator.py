# 📘 Module 2: R₀ Calculator | EpiModelAI Suite
# 🔢 Calculate basic reproduction number from infection data
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def run():
    # === Title ===
    st.title("📘 R₀ Calculator (Basic Reproduction Number)")
    st.markdown("Estimate **R₀** from your infection time-series data or manually using parameters.")

    # === Mode Selection ===
    mode = st.radio("Select Calculation Mode", ["📁 Upload Infection Data (CSV)", "✍️ Manual Estimation"])

    if mode == "📁 Upload Infection Data (CSV)":
        st.markdown("""
        **Instructions**:  
        Upload a `.csv` file with a column of daily infection counts named `"infected"`.  
        """)
        file = st.file_uploader("Upload CSV File", type=["csv"])

        if file:
            df = pd.read_csv(file)
            if 'infected' not in df.columns:
                st.error("CSV must contain an 'infected' column.")
                return

            df['day'] = np.arange(len(df))
            df['log_infected'] = np.log(df['infected'].replace(0, 1))

            # Linear regression to estimate exponential growth
            slope, intercept = np.polyfit(df['day'], df['log_infected'], 1)
            growth_rate = slope

            st.success(f"Estimated Growth Rate: {growth_rate:.3f} per day")

            # Assume recovery rate gamma
            gamma = st.slider("Assumed Recovery Rate γ (1/days)", 0.01, 1.0, 0.1, 0.01)
            r0 = 1 + (growth_rate / gamma)

            st.metric("Estimated R₀", f"{r0:.2f}")

            # Plot
            st.subheader("📈 Infection Growth Fit")
            fig, ax = plt.subplots()
            ax.plot(df['day'], df['log_infected'], label="Log(Infected)", marker='o')
            ax.plot(df['day'], slope * df['day'] + intercept, label="Linear Fit", color='red')
            ax.set_xlabel("Day")
            ax.set_ylabel("log(Infected)")
            ax.legend()
            st.pyplot(fig)

    elif mode == "✍️ Manual Estimation":
        st.sidebar.header("🔢 Manual Parameters")
        beta = st.sidebar.slider("Infection Rate β", 0.01, 1.0, 0.3, step=0.01)
        gamma = st.sidebar.slider("Recovery Rate γ", 0.01, 1.0, 0.1, step=0.01)

        r0 = beta / gamma
        st.metric("Estimated R₀", f"{r0:.2f}")

        st.markdown(f"""
        **Formula Used:**  
        `R₀ = β / γ`  
        Where:  
        - **β** = rate of infection per contact  
        - **γ** = rate of recovery  
        """)
