# ⚡ Module 2: Mass Flux Calculator | MassTransferAI Suite
# 📘 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng
# 💡 Real-World Case: Oxygen diffusion through a polymer membrane (gas separation, bioreactors)

import streamlit as st
import matplotlib.pyplot as plt
import io

def run():
    st.header("⚡ Mass Flux Calculator - Oxygen Transfer Through Membrane")
    st.markdown("Calculates mass flux based on Fick's Law for gases passing through a thin polymer membrane.")
    st.info("🔍 Real-World Context: Oxygen delivery in artificial organs or gas separation processes.")

    # --- Predefined gas scenarios ---
    gas_data = {
        "Oxygen (O₂)": {"D": 1.9e-9, "default_C1": 0.3, "default_C2": 0.08},
        "Carbon Dioxide (CO₂)": {"D": 1.4e-9, "default_C1": 0.6, "default_C2": 0.2},
        "Ammonia (NH₃)": {"D": 1.0e-9, "default_C1": 0.4, "default_C2": 0.1},
        "Custom": {"D": None, "default_C1": None, "default_C2": None}
    }

    # --- User Inputs ---
    col1, col2 = st.columns(2)
    with col1:
        gas = st.selectbox("Select Gas", list(gas_data.keys()))
        if gas != "Custom":
            D = gas_data[gas]["D"]
            C1 = st.number_input("Concentration at Membrane Inlet (mol/m³)", value=gas_data[gas]["default_C1"])
            C2 = st.number_input("Concentration at Membrane Outlet (mol/m³)", value=gas_data[gas]["default_C2"])
            st.info(f"Using D = {D:.1e} m²/s for {gas}")
        else:
            D = st.number_input("Diffusion Coefficient (m²/s)", min_value=1e-10, max_value=1e-6, value=1e-9, format="%.1e")
            C1 = st.number_input("Concentration at Membrane Inlet (mol/m³)", value=0.5)
            C2 = st.number_input("Concentration at Membrane Outlet (mol/m³)", value=0.1)

    with col2:
        dx = st.number_input("Membrane Thickness (m)", min_value=0.00001, max_value=0.01, value=0.001, format="%.5f")
        A = st.number_input("Membrane Area (m²)", min_value=0.0001, max_value=1.0, value=0.01)

    # --- Warning for reverse diffusion ---
    if C2 > C1:
        st.warning("⚠️ C₂ > C₁ detected. This may indicate reverse diffusion.")

    # --- Fick's Law Calculation ---
    J = -D * (C2 - C1) / dx     # mol/m²·s
    total_flux = J * A          # mol/s

    # --- Outputs ---
    st.subheader("📊 Results")
    st.metric("Mass Flux (J)", f"{J:.3e} mol/m²·s")
    st.metric("Total Transfer Rate", f"{total_flux:.3e} mol/s")
    st.success("✅ Calculation complete. You can adjust concentration or thickness for design optimization.")

    # --- Plot: Inlet vs Outlet Concentration ---
    st.subheader("🧪 Concentration Profile")
    fig, ax = plt.subplots()
    ax.bar(["Inlet (C₁)", "Outlet (C₂)"], [C1, C2], color=['green', 'orange'])
    ax.set_ylabel("Concentration (mol/m³)")
    ax.set_title("Membrane Side Concentrations")
    st.pyplot(fig)

    # --- Download Result Summary ---
    result_text = f"""
Mass Flux Report - {gas}
----------------------------------------
Diffusion Coefficient (D): {D:.2e} m²/s
Membrane Thickness (Δx): {dx:.5f} m
Membrane Area (A): {A:.5f} m²

C₁ (Inlet): {C1:.3f} mol/m³
C₂ (Outlet): {C2:.3f} mol/m³

Mass Flux (J): {J:.3e} mol/m²·s
Total Transfer Rate: {total_flux:.3e} mol/s
"""
    result_bytes = io.BytesIO(result_text.encode())
    st.download_button("📄 Download Report (.txt)", data=result_bytes, file_name="mass_flux_report.txt", mime="text/plain")

    # --- Equation Reference ---
    with st.expander("📘 Equation Used (Fick's First Law)"):
        st.latex(r"J = -D \cdot \frac{(C_2 - C_1)}{\Delta x}")
        st.markdown("- J: Mass flux (mol/m²·s)  \n- D: Diffusion coefficient (m²/s)  \n- C₁, C₂: Concentrations at membrane sides  \n- Δx: Membrane thickness (m)")
