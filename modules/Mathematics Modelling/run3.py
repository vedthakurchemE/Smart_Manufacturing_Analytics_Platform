# 📘 run.py - Mathematical Modeling Module | AllProjectsSuite
# 📐 Solve, visualize, and simulate real-world engineering models
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import minimize

def run():
    # === Page Config ===
    st.set_page_config(page_title="📐 Mathematical Modeling App", layout="wide")

    # === App Header ===
    st.title("📐 Mathematical Modeling Suite")
    st.markdown("""
    Explore the power of **math-based simulations** for Chemical Engineering, using tools like:
    - ODE/PDE solvers
    - Optimization models
    - Reaction kinetics & process systems

    📦 **Author**: Ved Thakur  
    🏫 IPS Academy Indore | BTech Chemical Engineering  
    🔗 Part of: **AllProjectsSuite**
    ---
    """)

    # === Navigation Tabs ===
    tab = st.selectbox("🔍 Select Tool", [
        "ODE Reactor Simulator",
        "Parameter Optimization",
        "Logistic Growth Model"
    ])

    # === Tool 1: ODE Reactor Simulation ===
    if tab == "ODE Reactor Simulator":
        st.header("🧪 CSTR First-Order Reaction Simulator")

        # ODE: dC/dt = -kC
        def model(C, t, k):
            return -k * C

        k = st.slider("Reaction Rate Constant (k)", 0.1, 2.0, 0.5)
        C0 = st.number_input("Initial Concentration (mol/L)", value=1.0)
        t = np.linspace(0, 10, 100)
        C = odeint(model, C0, t, args=(k,))

        fig, ax = plt.subplots()
        ax.plot(t, C, 'b-', linewidth=2)
        ax.set_xlabel('Time (min)')
        ax.set_ylabel('Concentration (mol/L)')
        ax.set_title('Concentration vs Time in CSTR')
        st.pyplot(fig)

    # === Tool 2: Parameter Optimization ===
    elif tab == "Parameter Optimization":
        st.header("📈 Minimize Cost Function")

        # Example cost function: f(x) = (x-3)^2 + 10
        def cost_function(x):
            return (x[0] - 3)**2 + 10

        x0 = [0.0]
        result = minimize(cost_function, x0)

        st.write(f"Initial Guess: x = {x0[0]}")
        st.write(f"Optimal x = {result.x[0]:.4f}")
        st.success(f"Minimum Cost = {result.fun:.4f}")

        # Plot cost function
        X = np.linspace(-5, 10, 100)
        Y = (X - 3)**2 + 10
        fig, ax = plt.subplots()
        ax.plot(X, Y, label='Cost Function')
        ax.plot(result.x, result.fun, 'ro', label='Minimum')
        ax.set_title("Cost Function Optimization")
        ax.legend()
        st.pyplot(fig)

    # === Tool 3: Logistic Growth Model ===
    elif tab == "Logistic Growth Model":
        st.header("📊 Logistic Population Growth Model")

        def logistic_model(P, t, r, K):
            return r * P * (1 - P / K)

        r = st.slider("Growth Rate (r)", 0.1, 1.0, 0.3)
        K = st.slider("Carrying Capacity (K)", 100, 1000, 500)
        P0 = st.number_input("Initial Population", value=10)
        t = np.linspace(0, 50, 200)
        P = odeint(logistic_model, P0, t, args=(r, K))

        fig, ax = plt.subplots()
        ax.plot(t, P, 'g-', linewidth=2)
        ax.set_xlabel('Time')
        ax.set_ylabel('Population')
        ax.set_title('Logistic Growth Curve')
        st.pyplot(fig)

    # === Footer ===
    st.markdown("---")
    st.markdown("📐 *This mathematical modeling module is part of the AllProjectsSuite by Ved Thakur.*")
