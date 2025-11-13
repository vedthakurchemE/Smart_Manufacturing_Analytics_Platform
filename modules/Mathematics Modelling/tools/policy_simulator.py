# 📘 Module 7: Containment Policy Simulator | EpiModelAI Suite
# 🚫 Compare disease spread with and without interventions like lockdowns or masks
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def run():
    # === Title ===
    st.title("📘 Containment Policy Simulator")
    st.markdown("Simulate the effect of policies like lockdowns, masks, or social distancing using SEIR model variations.")

    # === Sidebar Inputs ===
    st.sidebar.header("🛑 Policy Settings")
    N = st.sidebar.slider("Total Population (N)", 1000, 1000000, 10000, step=1000)
    I0 = st.sidebar.slider("Initial Infected", 1, 1000, 10)
    E0 = st.sidebar.slider("Initial Exposed", 0, 500, 5)
    R0 = 0
    S0 = N - I0 - E0 - R0

    base_beta = st.sidebar.slider("Base Infection Rate (β)", 0.1, 1.0, 0.4, 0.01)
    sigma = st.sidebar.slider("Incubation Rate (σ)", 0.01, 1.0, 0.2, 0.01)
    gamma = st.sidebar.slider("Recovery Rate (γ)", 0.01, 1.0, 0.1, 0.01)
    days = st.sidebar.slider("Simulation Days", 30, 365, 160)

    # === Policy Slider ===
    policy = st.radio("Select Policy Type", [
        "🔓 No Intervention",
        "🔒 Full Lockdown (50% Reduction)",
        "😷 Masks + Distancing (30% Reduction)",
        "🌀 Late Lockdown (Starts at Day 50)"
    ])

    # === Define Beta(t) for Policy ===
    def get_beta_t(t):
        if policy == "🔓 No Intervention":
            return base_beta
        elif policy == "🔒 Full Lockdown (50% Reduction)":
            return base_beta * 0.5
        elif policy == "😷 Masks + Distancing (30% Reduction)":
            return base_beta * 0.7
        elif policy == "🌀 Late Lockdown (Starts at Day 50)":
            return base_beta if t < 50 else base_beta * 0.4

    # === SEIR with Policy ===
    def seir_policy(y, t, N, sigma, gamma):
        S, E, I, R = y
        beta_t = get_beta_t(t)
        dSdt = -beta_t * S * I / N
        dEdt = beta_t * S * I / N - sigma * E
        dIdt = sigma * E - gamma * I
        dRdt = gamma * I
        return dSdt, dEdt, dIdt, dRdt

    # === Solve ODE ===
    t = np.linspace(0, days, days)
    y0 = S0, E0, I0, R0
    ret = odeint(seir_policy, y0, t, args=(N, sigma, gamma))
    S, E, I, R = ret.T

    # === Plot ===
    st.subheader("📈 SEIR with Policy Effect")
    fig, ax = plt.subplots()
    ax.plot(t, S, label='Susceptible', color='blue')
    ax.plot(t, E, label='Exposed', color='orange')
    ax.plot(t, I, label='Infected', color='red')
    ax.plot(t, R, label='Recovered', color='green')
    ax.set_xlabel("Days")
    ax.set_ylabel("Population")
    ax.set_title(f"Policy: {policy}")
    ax.legend()
    st.pyplot(fig)

    # === Summary Metrics ===
    st.subheader("📊 Final Day Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Susceptible", f"{int(S[-1])}")
    col2.metric("Exposed", f"{int(E[-1])}")
    col3.metric("Infected", f"{int(I[-1])}")
    col4.metric("Recovered", f"{int(R[-1])}")

    with st.expander("📘 About This Simulation"):
        st.markdown(f"""
        This simulation modifies the **transmission rate (β)** depending on the selected containment strategy.  
        - **Full Lockdown**: 50% β  
        - **Masks & Distancing**: 70% β  
        - **Late Lockdown**: Switches β at day 50  
        - Model equations follow the standard SEIR system using SciPy’s `odeint`.
        """)
