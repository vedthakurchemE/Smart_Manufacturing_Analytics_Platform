# 📘 Module 8: Sensitivity Analyzer | EpiModelAI Suite
# 🔍 Explore impact of β, γ, σ on epidemic outcome using parameter sweep
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def run():
    # === Title ===
    st.title("📘 Sensitivity Analyzer")
    st.markdown("Run multiple simulations to observe how small changes in parameters affect the epidemic outcome.")

    # === Sidebar Parameters ===
    st.sidebar.header("🎛️ Parameter Sweep Settings")
    N = st.sidebar.number_input("Total Population (N)", value=10000)
    I0 = st.sidebar.slider("Initial Infected", 1, 100, 10)
    E0 = st.sidebar.slider("Initial Exposed", 0, 100, 5)
    R0 = 0
    S0 = N - I0 - E0 - R0
    days = st.sidebar.slider("Simulation Days", 30, 365, 160)

    beta_range = st.sidebar.slider("β Range (Infection Rate)", 0.1, 1.0, (0.2, 0.5), step=0.01)
    gamma_range = st.sidebar.slider("γ Range (Recovery Rate)", 0.01, 1.0, (0.05, 0.2), step=0.01)
    sigma_range = st.sidebar.slider("σ Range (Incubation Rate)", 0.01, 1.0, (0.1, 0.3), step=0.01)

    num_samples = st.sidebar.slider("Number of Monte Carlo Samples", 5, 50, 10)

    # === SEIR Model ===
    def seir_model(y, t, N, beta, sigma, gamma):
        S, E, I, R = y
        dSdt = -beta * S * I / N
        dEdt = beta * S * I / N - sigma * E
        dIdt = sigma * E - gamma * I
        dRdt = gamma * I
        return dSdt, dEdt, dIdt, dRdt

    # === Run Simulations ===
    peak_infections = []
    final_recovered = []
    beta_vals = np.linspace(beta_range[0], beta_range[1], num_samples)
    gamma_vals = np.linspace(gamma_range[0], gamma_range[1], num_samples)
    sigma_vals = np.linspace(sigma_range[0], sigma_range[1], num_samples)

    for b, g, s in zip(beta_vals, gamma_vals, sigma_vals):
        y0 = S0, E0, I0, R0
        t = np.linspace(0, days, days)
        ret = odeint(seir_model, y0, t, args=(N, b, s, g))
        S, E, I, R = ret.T
        peak_infections.append(np.max(I))
        final_recovered.append(R[-1])

    # === Plot Results ===
    st.subheader("📈 Sensitivity of Peak Infection")
    fig1, ax1 = plt.subplots()
    ax1.plot(beta_vals, peak_infections, 'r-o')
    ax1.set_xlabel("Infection Rate (β)")
    ax1.set_ylabel("Peak Infected")
    ax1.set_title("📉 Peak Infections vs β")
    st.pyplot(fig1)

    st.subheader("📈 Sensitivity of Final Recovered")
    fig2, ax2 = plt.subplots()
    ax2.plot(gamma_vals, final_recovered, 'g-o')
    ax2.set_xlabel("Recovery Rate (γ)")
    ax2.set_ylabel("Total Recovered")
    ax2.set_title("📉 Final Recovery vs γ")
    st.pyplot(fig2)

    # === Summary ===
    st.subheader("📊 Sample Statistics")
    col1, col2 = st.columns(2)
    col1.metric("Max Peak Infection", f"{max(peak_infections):.0f}")
    col2.metric("Max Final Recovered", f"{max(final_recovered):.0f}")

    with st.expander("📘 What This Shows"):
        st.markdown("""
        - This module runs **multiple SEIR simulations** with different β, γ, and σ values.
        - It helps assess how **sensitive** the model is to small parameter changes.
        - Useful for tuning public health interventions and understanding uncertainty.
        """)
