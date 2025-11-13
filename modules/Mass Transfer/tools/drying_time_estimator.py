# 🌬️ Drying Time Estimator (Mass Transfer Suite)
# 📘 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng
# 📊 Models: Constant + Falling Rate, Page Model | Exports Report | Moisture Curve

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io


def run():
    st.title("🌬️ Drying Time Estimator")
    st.markdown("Estimate drying time using **Constant + Falling Rate** or **Page Model**.")

    col1, col2 = st.columns(2)

    with col1:
        M0 = st.number_input("Initial Moisture Content (kg water/kg dry solid)", 0.01, 5.0, 1.0, 0.01)
        X = st.number_input("Final Moisture Content (kg water/kg dry solid)", 0.001, 4.9, 0.1, 0.01)
        A = st.number_input("Drying Surface Area (m²)", 0.01, 10.0, 1.0, 0.01)

    with col2:
        Mc = st.number_input("Critical Moisture Content (kg water/kg dry solid)", 0.001, 5.0, 0.3, 0.01)
        Rc = st.number_input("Constant Drying Rate (kg/m²·hr)", 0.01, 10.0, 0.5, 0.01)
        model = st.selectbox("Drying Model", ["Constant + Falling Rate", "Page Model"])

    # Input validation
    if X >= M0:
        st.error("❌ Final moisture must be less than initial moisture.")
        return
    if Mc >= M0:
        st.warning("⚠️ Critical moisture should be less than initial moisture.")

    t1 = t2 = t = 0
    report = ""

    if model == "Constant + Falling Rate":
        # Handle critical moisture logic
        if Mc >= M0:
            Mc = M0  # No constant rate drying
        if Mc <= X:
            Mc = X  # Fully in constant rate

        ΔM1 = M0 - Mc
        ΔM2 = Mc - X

        t1 = ΔM1 / Rc  # Constant rate time

        # Falling rate zone (assume linear decline)
        if ΔM2 > 0:
            Rf_avg = Rc / 2
            t2 = ΔM2 / Rf_avg
        else:
            t2 = 0

        t = t1 + t2

        report = f"""📄 **Drying Report**:
------------------------
🔹 Model: Constant + Falling Rate
🔹 Initial Moisture (M₀): {M0} kg/kg
🔹 Final Moisture (X): {X} kg/kg
🔹 Critical Moisture (M꜀): {Mc} kg/kg
🔹 Drying Area (A): {A} m²
🔹 Constant Rate (R꜀): {Rc} kg/m²·hr

⏱️ Constant Rate Time: {t1:.2f} hr
⏱️ Falling Rate Time: {t2:.2f} hr
⏱️ **Total Drying Time**: {t:.2f} hr
"""

    elif model == "Page Model":
        k = st.number_input("Page Model Constant (k)", 0.01, 5.0, 0.5, 0.01)
        n = st.number_input("Page Model Exponent (n)", 0.01, 5.0, 1.0, 0.01)
        MR0 = 1.0
        MRf = (X - 0) / (M0 - 0)
        if MRf <= 0 or MRf >= 1:
            st.error("Invalid moisture ratio for Page model.")
            return

        t = ((-np.log(MRf)) / k) ** (1 / n)
        t1 = t
        total_time = t

        report = f"""📄 **Drying Report**:
------------------------
🔹 Model: Page Model
🔹 Initial Moisture (M₀): {M0} kg/kg
🔹 Final Moisture (X): {X} kg/kg
🔹 Drying Area (A): {A} m²
🔹 Constants: k = {k}, n = {n}

⏱️ **Estimated Drying Time**: {t:.2f} hr
"""

    # Energy estimate (optional)
    drying_load = A * (M0 - X)  # kg water removed
    energy_kJ = drying_load * 2260  # Approx. latent heat of water
    report += f"🔋 Estimated Energy: {energy_kJ:.1f} kJ (based on latent heat of vaporization)"

    st.success(f"✅ Estimated Drying Time: {t:.2f} hr")

    # Moisture vs Time Plot
    plot_time = t if model == "Page Model" else t1 + t2
    time_vals = np.linspace(0, plot_time, 100)

    if model == "Constant + Falling Rate":
        moisture_vals = []
        for time in time_vals:
            if time <= t1:
                moisture = M0 - Rc * time
            else:
                slope = (X - Mc) / (t2 if t2 != 0 else 1e-5)
                moisture = Mc + slope * (time - t1)
            moisture_vals.append(max(X, moisture))
    else:
        moisture_vals = M0 * np.exp(-k * time_vals ** n)

    fig, ax = plt.subplots()
    ax.plot(time_vals, moisture_vals, label="Moisture Content", color='teal', linewidth=2)

    if model == "Constant + Falling Rate":
        ax.axvline(t1, linestyle='--', color='gray', label="End of Constant Rate")
        ax.axhline(Mc, linestyle=':', color='red', label="Critical Moisture")

    ax.set_xlabel("Time (hr)")
    ax.set_ylabel("Moisture Content (kg/kg dry solid)")
    ax.set_title("🧪 Moisture Content vs Time")
    ax.legend()
    st.pyplot(fig)

    # Report download
    st.download_button("⬇️ Download Report", report, file_name="drying_time_report.txt")
