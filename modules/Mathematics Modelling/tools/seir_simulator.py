# 📘 Module 1: SEIR Simulator | EpiModelAI Suite
# 🔬 Simulate disease spread using SEIR model (ODE-based)
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def run():
    # === Title ===
    st.title("📘 SEIR Model Simulator")
    st.markdown("Simulate disease spread using the SEIR differential equation model.")

    # === Sidebar Inputs ===
    st.sidebar.header("🧪 SEIR Model Parameters")
    N = st.sidebar.slider("Total Population (N)", 1000, 1000000, 10000, step=1000)
    beta = st.sidebar.slider("Infection Rate (β)", 0.01, 1.0, 0.3, step=0.01)
    sigma = st.sidebar.slider("Incubation Rate (σ)", 0.01, 1.0, 0.2, step=0.01)
    gamma = st.sidebar.slider("Recovery Rate (γ)", 0.01, 1.0, 0.1, step=0.01)
    days = st.sidebar.slider("Days to Simulate", 10, 365, 160)

    # Initial conditions
    I0 = st.sidebar.number_input("Initial Infected (I₀)", 1, N, 1)
    E0 = st.sidebar.number_input("Initial Exposed (E₀)", 0, N, 0)
    R0 = st.sidebar.number_input("Initial Recovered (R₀)", 0, N, 0)
    S0 = N - I0 - E0 - R0

    # === SEIR Differential Equations ===
    def seir_model(y, t, N, beta, sigma, gamma):
        S, E, I, R = y
        dSdt = -beta * S * I / N
        dEdt = beta * S * I / N - sigma * E
        dIdt = sigma * E - gamma * I
        dRdt = gamma * I
        return dSdt, dEdt, dIdt, dRdt

    # === Time Grid and Initial Conditions ===
    t = np.linspace(0, days, days)
    y0 = S0, E0, I0, R0

    # === Solve ODE ===
    result = odeint(seir_model, y0, t, args=(N, beta, sigma, gamma))
    S, E, I, R = result.T

    # === Plotting ===
    st.subheader("📈 SEIR Curve Over Time")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t, S, label='Susceptible', color='blue')
    ax.plot(t, E, label='Exposed', color='orange')
    ax.plot(t, I, label='Infected', color='red')
    ax.plot(t, R, label='Recovered', color='green')
    ax.set_xlabel("Days")
    ax.set_ylabel("Number of People")
    ax.set_title("SEIR Model Simulation")
    ax.legend()
    st.pyplot(fig)

    # === Metrics Summary ===
    st.subheader("📊 Final Day Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Susceptible", f"{int(S[-1])}")
    col2.metric("Exposed", f"{int(E[-1])}")
    col3.metric("Infected", f"{int(I[-1])}")
    col4.metric("Recovered", f"{int(R[-1])}")

    # === Behind the Model ===
    with st.expander("📘 Model Details"):
        st.markdown("""
        - **S (Susceptible)**: not yet infected  
        - **E (Exposed)**: infected but not yet infectious  
        - **I (Infectious)**: actively spreading disease  
        - **R (Recovered)**: immune or removed  
        - **Equations**:
            ```
            dS/dt = -β * S * I / N  
            dE/dt = β * S * I / N - σ * E  
            dI/dt = σ * E - γ * I  
            dR/dt = γ * I
            ```
        - Solved using SciPy’s `odeint` function.
        """)
