# 📘 Module 1: Crude Oil Blend Optimization | PetroStream AI Suite
# 🛢️ Optimize blend to maximize profit & minimize impurity constraints
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import numpy as np
from scipy.optimize import minimize
import pandas as pd

def run():
    st.set_page_config(page_title="🛢️ Crude Oil Blend Optimizer", layout="centered")
    st.title("🛢️ Crude Oil Blend Optimizer")
    st.markdown("Optimize crude blending to meet economic and quality targets.")

    # --- Sidebar Inputs ---
    st.sidebar.header("📥 Input Crude Details")
    num_crudes = st.sidebar.slider("Number of Crudes", 2, 5, 3)

    crude_names, prices, sulfur, viscosity = [], [], [], []

    for i in range(num_crudes):
        st.sidebar.markdown(f"### Crude {i+1}")
        crude_names.append(st.sidebar.text_input(f"Name {i+1}", value=f"Crude_{i+1}", key=f"name_{i}"))
        prices.append(st.sidebar.number_input(f"Price ($/bbl)", value=60.0+i*2, key=f"price_{i}"))
        sulfur.append(st.sidebar.number_input(f"Sulfur (%)", value=1.0+i*0.2, key=f"sulfur_{i}"))
        viscosity.append(st.sidebar.number_input(f"Viscosity (cSt)", value=2.5+i*0.3, key=f"viscosity_{i}"))

    st.sidebar.header("🎯 Blend Targets")
    max_sulfur = st.sidebar.number_input("Max Sulfur in Blend (%)", value=1.5)
    max_viscosity = st.sidebar.number_input("Max Viscosity in Blend (cSt)", value=3.5)

    st.sidebar.header("⚙️ Optimization Settings")
    obj_type = st.sidebar.selectbox("Objective Function", ["Minimize Cost", "Minimize Sulfur", "Minimize Viscosity"])

    # --- Run Optimization ---
    if st.button("🚀 Run Optimization"):
        price_arr = np.array(prices)
        sulfur_arr = np.array(sulfur)
        viscosity_arr = np.array(viscosity)

        def objective(x):
            if obj_type == "Minimize Cost":
                return np.dot(x, price_arr)
            elif obj_type == "Minimize Sulfur":
                return np.dot(x, sulfur_arr)
            else:
                return np.dot(x, viscosity_arr)

        constraints = [
            {"type": "eq", "fun": lambda x: np.sum(x) - 1},
            {"type": "ineq", "fun": lambda x: max_sulfur - np.dot(x, sulfur_arr)},
            {"type": "ineq", "fun": lambda x: max_viscosity - np.dot(x, viscosity_arr)}
        ]

        bounds = [(0, 1) for _ in range(num_crudes)]
        x0 = np.ones(num_crudes) / num_crudes

        result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

        # --- Results ---
        if result.success:
            st.success("✅ Optimization Successful!")
            st.subheader("🔍 Optimal Blend Composition")

            df = pd.DataFrame({
                "Crude": crude_names,
                "Fraction": np.round(result.x, 4),
                "Price ($/bbl)": prices,
                "Sulfur (%)": sulfur,
                "Viscosity (cSt)": viscosity
            })

            st.dataframe(df, use_container_width=True)

            st.markdown(f"**💰 Total Blend Cost:** `${np.dot(result.x, price_arr):.2f}/bbl`")
            st.markdown(f"**🧪 Blend Sulfur:** `{np.dot(result.x, sulfur_arr):.3f}%`")
            st.markdown(f"**💧 Blend Viscosity:** `{np.dot(result.x, viscosity_arr):.3f} cSt`")
        else:
            st.error("❌ Optimization Failed. Adjust constraints or inputs.")

# Uncomment below to test as a standalone app
# if __name__ == "__main__":
#     run()
