import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="🍲 Cooking Time Estimator", layout="centered")

def lumped_capacitance_time(m, Cp, h, A, T_initial, T_env, T_target):
    Bi = h * (m / (A * Cp))**(1/3)
    if Bi > 0.1:
        return None, Bi  # Not valid for lumped method
    tau = (m * Cp) / (h * A)
    time_required = -tau * np.log((T_target - T_env) / (T_initial - T_env))
    return time_required, Bi

def shape_area_calculator(shape, d, L=None):
    if shape == "Sphere":
        A = 4 * np.pi * (d/2)**2
    elif shape == "Cylinder" and L is not None:
        A = 2 * np.pi * (d/2)**2 + 2 * np.pi * (d/2) * L
    else:
        A = None
    return A

def run():
    st.title("🍲 Cooking Time Estimator using Lumped Capacitance Method")
    st.markdown("Estimate **heating/cooling time** using an analytical approach for small Biot number systems.")

    with st.sidebar:
        st.header("📦 Object Properties")
        shape = st.selectbox("Select Shape", ["Custom", "Sphere", "Cylinder"])
        if shape != "Custom":
            d = st.number_input("Diameter [m]", 0.01, 1.0, 0.1)
            L = st.number_input("Length [m] (only for Cylinder)", 0.01, 2.0, 0.2) if shape == "Cylinder" else None
            A = shape_area_calculator(shape, d, L)
        else:
            A = st.number_input("Surface Area A [m²]", 0.001, 5.0, 0.03)

        m = st.number_input("Mass [kg]", 0.01, 10.0, 0.5)
        Cp = st.number_input("Specific Heat Cp [kJ/kg·K]", 0.1, 10.0, 3.7)
        h = st.number_input("Convective Coefficient h [W/m²·K]", 5.0, 1000.0, 100.0)

        st.header("🌡️ Temperature Conditions")
        T_initial = st.number_input("Initial Temp [°C]", -50, 300, 25)
        T_env = st.number_input("Environment Temp [°C]", 0, 300, 100)
        T_target = st.number_input("Target Temp [°C]", 0, 300, 70)

    # Run model
    time_required, Bi = lumped_capacitance_time(m, Cp * 1000, h, A, T_initial, T_env, T_target)

    st.subheader("📊 Results")
    st.markdown(f"**Biot Number (Bi):** `{Bi:.4f}`")

    if Bi > 0.1:
        st.error("❌ Lumped method **not valid**: Bi > 0.1. Try transient simulation instead.")
    else:
        st.success("✅ Lumped method **valid**: Bi < 0.1")
        st.markdown(f"**Estimated Time Required:** `{time_required:.2f}` seconds (~ `{time_required/60:.2f}` minutes)")

        # Plot temperature curve
        st.subheader("📈 Temperature vs. Time")
        tau = (m * Cp * 1000) / (h * A)
        t_vals = np.linspace(0, time_required * 1.3, 120)
        T_vals = T_env + (T_initial - T_env) * np.exp(-t_vals / tau)

        fig, ax = plt.subplots()
        ax.plot(t_vals, T_vals, color="orange", label="Temperature Curve")
        ax.axhline(T_target, color='red', linestyle='--', label="Target Temperature")
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Temperature [°C]")
        ax.set_title("Lumped Model: Temperature vs Time")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

        # Export CSV
        df = pd.DataFrame({"Time (s)": t_vals, "Temperature (°C)": T_vals})
        st.download_button("⬇️ Download Temperature Profile (CSV)", df.to_csv(index=False), file_name="cooking_profile.csv")

    with st.expander("📘 Theory: Lumped Capacitance Method"):
        st.markdown(r"""
        **Applicable when Biot Number (Bi) < 0.1**

        \[
        \text{Bi} = \frac{h L_c}{k} \approx h \left( \frac{m}{A C_p} \right)^{1/3}
        \]

        \[
        T(t) = T_{\infty} + (T_0 - T_{\infty}) \cdot e^{-t / \tau}, \quad \tau = \frac{m C_p}{h A}
        \]

        This model assumes **uniform internal temperature** due to high conductivity or small size.
        """)

    st.markdown("---")
    st.info("💡 Tip: Best for small foods, metals, or objects with high internal conductivity and low Biot number.")
    st.caption("🧠 Created by Ved Thakur | IPS Academy Indore | ChemEng")
