# 📘 Module 10: Petroleum Lab Data Auto-Analyzer | PetroStream AI Suite
# 🧪 Analyze lab parameters: distillation, flash point, viscosity, pour point
# 📦 Author: Ved Thakur | Semester 1 | IPS Academy Indore | ChemE (2025-2029)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run():
    st.set_page_config(page_title="🧪 Lab Data Auto-Analyzer", layout="centered")
    st.title("🧪 Petroleum Lab Data Auto-Analyzer")
    st.markdown("Auto-analyze lab data like distillation curve, flash point, viscosity, pour point.")

    # --- Simulated sample data only ---
    df = pd.DataFrame({
        "Temp (°C)": [100, 150, 200, 250, 300, 350],
        "Vol (%)": [10, 30, 50, 70, 90, 100],
        "Viscosity (cSt)": [2.5, 2.7, 3.0, 3.3, 3.5, 3.7],
        "Flash Point (°C)": [45, 48, 52, 56, 60, 64],
        "Pour Point (°C)": [-10, -8, -7, -6, -5, -4]
    })

    st.subheader("📊 Raw Lab Data")
    st.dataframe(df)

    # === Distillation Curve ===
    st.subheader("🌡️ Distillation Curve")
    fig1, ax1 = plt.subplots()
    ax1.plot(df["Temp (°C)"], df["Vol (%)"], marker='o', color='darkblue')
    ax1.set_xlabel("Temperature (°C)")
    ax1.set_ylabel("Volume Recovered (%)")
    ax1.set_title("Distillation Curve")
    ax1.grid(True)
    st.pyplot(fig1)

    # === Flash Point Trend ===
    st.subheader("🔥 Flash Point Trend")
    fig2, ax2 = plt.subplots()
    ax2.plot(df["Temp (°C)"], df["Flash Point (°C)"], marker='o', color='crimson')
    ax2.set_title("Flash Point vs Temperature")
    ax2.set_xlabel("Temperature (°C)")
    ax2.set_ylabel("Flash Point (°C)")
    ax2.grid(True)
    st.pyplot(fig2)

    # === Viscosity Plot ===
    st.subheader("🛢️ Viscosity vs Temp")
    fig3, ax3 = plt.subplots()
    sns.lineplot(x="Temp (°C)", y="Viscosity (cSt)", data=df, marker="o", ax=ax3, color="purple")
    ax3.set_title("Viscosity vs Temperature")
    ax3.grid(True)
    st.pyplot(fig3)

    # === Pour Point Trend ===
    st.subheader("❄️ Pour Point vs Temp")
    fig4, ax4 = plt.subplots()
    ax4.plot(df["Temp (°C)"], df["Pour Point (°C)"], marker='o', linestyle='--', color='teal')
    ax4.set_title("Pour Point vs Temperature")
    ax4.set_xlabel("Temperature (°C)")
    ax4.set_ylabel("Pour Point (°C)")
    ax4.grid(True)
    st.pyplot(fig4)

    # === QC Checks ===
    st.subheader("✅ Quality Control Rules")
    violations = []
    if df["Flash Point (°C)"].min() < 35:
        violations.append("⚠️ Flash point too low — potential safety hazard.")
    if df["Pour Point (°C)"].max() > 0:
        violations.append("❄️ High pour point — may cause flow issues in cold weather.")
    if df["Viscosity (cSt)"].max() > 5:
        violations.append("🛢️ Viscosity too high — pumping issues likely.")

    if violations:
        for v in violations:
            st.error(v)
    else:
        st.success("✅ All parameters within acceptable QC range.")
