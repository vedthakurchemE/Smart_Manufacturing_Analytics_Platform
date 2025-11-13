# 📘 Module 9: Healthcare Capacity Forecaster | EpiModelAI Suite
# 🏥 Forecast hospital and ICU capacity demand using SEIR model projections
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def run():
    # === Title ===
    st.title("📘 Healthcare Capacity Forecaster")
    st.markdown("Forecast hospital and ICU bed demand during an epidemic using SEIR projections.")

    # === Sidebar Inputs ===
    st.sidebar.header("🏥 Capacity & Parameters")
    N = st.sidebar.slider("Population Size", 1000, 1000000, 10000, step=1000)
    I0 = st.sidebar.slider("Initial Infected", 1, 500, 50)
    E0 = st.sidebar.slider("Initial Exposed", 0, 500, 25)
    R0 = 0
    S0 = N - I0 - E0 - R0

    beta = st.sidebar.slider("Infection Rate (β)", 0.1, 1.0, 0.3, 0.01)
    sigma = st.sidebar.slider("Incubation Rate (σ)", 0.05, 1.0, 0.2, 0.01)
    gamma = st.sidebar.slider("Recovery Rate (γ)", 0.01, 1.0, 0.1, 0.01)

    days = st.sidebar.slider("Simulation Days", 30, 365, 180)

    hospital_rate = st.sidebar.slider("Hospitalization Rate (%)", 1, 100, 10) / 100
    icu_rate = st.sidebar.slider("ICU Rate (%)", 1, 100, 3) / 100

    total_beds = st.sidebar.number_input("🛏️ Total Hospital Beds", value=1000)
    total_icu = st.sidebar.number_input("💉 Total ICU Beds", value=200)

    # === SEIR Equations ===
    def seir(y, t, N, beta, sigma, gamma):
        S, E, I, R = y
        dSdt = -beta * S * I / N
        dEdt = beta * S * I / N - sigma * E
        dIdt = sigma * E - gamma * I
        dRdt = gamma * I
        return dSdt, dEdt, dIdt, dRdt

    t = np.linspace(0, days, days)
    y0 = S0, E0, I0, R0
    ret = odeint(seir, y0, t, args=(N, beta, sigma, gamma))
    S, E, I, R = ret.T

    # === Forecasted Hospitalization & ICU Demand ===
    hospitalized = I * hospital_rate
    icu = I * icu_rate

    # === Plotting ===
    st.subheader("📈 SEIR + Hospital Load Forecast")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t, hospitalized, label="Hospital Beds Needed", color="orange")
    ax.axhline(total_beds, linestyle="--", color="brown", label="Total Hospital Beds")

    ax.plot(t, icu, label="ICU Beds Needed", color="red")
    ax.axhline(total_icu, linestyle="--", color="black", label="Total ICU Beds")

    ax.set_xlabel("Days")
    ax.set_ylabel("People")
    ax.set_title("🏥 Forecasted Bed Demand vs Capacity")
    ax.legend()
    st.pyplot(fig)

    # === Summary Metrics ===
    st.subheader("📊 Key Forecast Stats")
    col1, col2 = st.columns(2)
    col1.metric("🔺 Max Hospital Beds Needed", f"{int(max(hospitalized))}")
    col2.metric("🔺 Max ICU Beds Needed", f"{int(max(icu))}")

    st.subheader("📉 Overload Risk")
    overload_hosp = int(max(0, max(hospitalized) - total_beds))
    overload_icu = int(max(0, max(icu) - total_icu))
    col3, col4 = st.columns(2)
    col3.metric("🛏️ Hospital Overload", overload_hosp)
    col4.metric("💉 ICU Overload", overload_icu)

    with st.expander("📘 Model Notes"):
        st.markdown(f"""
        - Forecast uses **SEIR model** to simulate infection spread.
        - Hospitalization is estimated as: `Hospital = I × hospitalization rate`
        - ICU need is estimated as: `ICU = I × ICU rate`
        - Capacity lines represent your available healthcare infrastructure.
        """)
