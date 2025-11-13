# 📘 Module 10: Thermal Conductivity Estimator | HeatTransferAI Suite
# 📦 Estimate thermal conductivity using empirical models for various materials
# 📌 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("🔥 Thermal Conductivity Estimator")
    st.markdown("Estimate thermal conductivity based on material, temperature, and empirical models.")

    material = st.selectbox("Select Material:", [
        "Copper", "Aluminum", "Stainless Steel", "Water", "Air", "Glass", "Iron"
    ])

    temperature = st.slider("Temperature (°C):", min_value=0, max_value=500, value=25)

    # === Thermal Conductivity Models ===
    def k_copper(T): return 401 - 0.1 * T
    def k_aluminum(T): return 237 - 0.05 * T
    def k_stainless_steel(T): return 16.2 + 0.01 * T
    def k_water(T): return 0.6065 - 0.00122 * T
    def k_air(T): return 0.024 + 7.2e-5 * T
    def k_glass(T): return 1.1 - 0.0005 * T
    def k_iron(T): return 80 - 0.02 * T

    material_funcs = {
        "Copper": k_copper,
        "Aluminum": k_aluminum,
        "Stainless Steel": k_stainless_steel,
        "Water": k_water,
        "Air": k_air,
        "Glass": k_glass,
        "Iron": k_iron,
    }

    if material in material_funcs:
        k = material_funcs[material](temperature)
        st.success(f"Estimated Thermal Conductivity of {material} at {temperature}°C: **{k:.4f} W/m·K**")
    else:
        st.warning("Model not available for selected material.")

    st.markdown("---")

    # === Heat Transfer through a Slab (Optional Visualization) ===
    st.subheader("🧊 Heat Transfer Through a Slab")
    with st.expander("➕ Show Heat Transfer Calculator"):
        A = st.number_input("Area (m²):", value=1.0)
        d = st.number_input("Thickness (m):", value=0.01)
        T_hot = st.number_input("Hot Side Temperature (°C):", value=100.0)
        T_cold = st.number_input("Cold Side Temperature (°C):", value=25.0)

        if st.button("Estimate Heat Transfer Rate"):
            q = (k * A * (T_hot - T_cold)) / d
            st.success(f"Estimated Heat Transfer Rate: **{q:.2f} W**")

            # Plotting
            fig, ax = plt.subplots()
            ax.bar(["T_hot", "T_cold"], [T_hot, T_cold], color=["red", "blue"])
            ax.set_ylabel("Temperature (°C)")
            st.pyplot(fig)

    st.markdown("---")

    # === Plot Conductivity vs Temperature ===
    st.subheader("📈 Thermal Conductivity vs. Temperature")

    T_vals = np.linspace(0, 500, 100)
    if material in material_funcs:
        k_vals = [material_funcs[material](T) for T in T_vals]
        fig, ax = plt.subplots()
        ax.plot(T_vals, k_vals, color="green")
        ax.set_xlabel("Temperature (°C)")
        ax.set_ylabel("Thermal Conductivity (W/m·K)")
        ax.set_title(f"{material} Thermal Conductivity")
        ax.grid(True)
        st.pyplot(fig)

    # === Sample Heat Exchanger Visualizer (Edge Use) ===
    st.subheader("🧮 Heat Exchanger Output Visualizer (Optional)")

    method = st.radio("Calculation Method:", ["Effectiveness-NTU", "LMTD"], horizontal=True)

    if method == "LMTD":
        delta_T1 = st.number_input("ΔT1 (Hot In - Cold Out) °C", value=50.0)
        delta_T2 = st.number_input("ΔT2 (Hot Out - Cold In) °C", value=30.0)
        if delta_T1 != delta_T2:
            LMTD = (delta_T1 - delta_T2) / np.log(delta_T1 / delta_T2)
        else:
            LMTD = delta_T1
        st.info(f"Estimated LMTD: **{LMTD:.2f}°C**")
        delta_T = (delta_T1 + delta_T2) / 2
    else:
        st.info("Effectiveness-NTU method visualization not implemented here.")
        delta_T = None  # fallback

    # === Plot ===
    st.subheader("📉 Temperature Profile")

    # Fallback for delta_T if None
    delta_T_plot = delta_T if delta_T is not None else 20

    T_hot_in = T_hot
    T_cold_in = T_cold
    T_hot_out = T_hot_in - delta_T_plot
    T_cold_out = T_cold_in + delta_T_plot

    temps = [T_hot_in, T_hot_out]
    cold = [T_cold_in, T_cold_out]

    fig, ax = plt.subplots()
    ax.plot(["Inlet", "Outlet"], temps, label="Hot Stream", color="red", marker="o")
    ax.plot(["Inlet", "Outlet"], cold, label="Cold Stream", color="blue", marker="o")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Temperature Profile")
    ax.legend()
    st.pyplot(fig)
