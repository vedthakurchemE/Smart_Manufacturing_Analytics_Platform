# 🧪 Module 1: Transdermal Drug Diffusion Simulator | MassTransferAI Suite
# 📘 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng
# 💡 Real-World Case: Simulating drug diffusion through human skin

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io


def run():
    st.header("🧪 Transdermal Drug Diffusion Simulator")
    st.markdown("Simulates 1D diffusion of a drug through skin using Fick's Law and finite difference method.")

    # --- Drug Database ---
    drug_data = {
        "Custom": None,
        "Aspirin": 3.5e-10,
        "Nicotine": 1.2e-9,
        "Fentanyl": 2.4e-10,
        "Testosterone": 5.5e-10
    }

    # --- User Inputs ---
    col1, col2 = st.columns(2)
    with col1:
        drug = st.selectbox("Select Drug", list(drug_data.keys()))
        if drug != "Custom":
            D = drug_data[drug]
            st.info(f"Using Diffusion Coefficient: {D:.1e} m²/s for {drug}")
        else:
            D = st.number_input("Diffusion Coefficient (m²/s)", min_value=1e-10, max_value=1e-4, value=1e-6,
                                format="%.1e")

        L = st.number_input("Skin Thickness (m)", min_value=0.0001, max_value=0.01, value=0.002, format="%.4f")
        C0 = st.number_input("Initial Drug Concentration at Surface (mol/m³)", value=1.0)

    with col2:
        t_steps = st.slider("Time Steps", min_value=100, max_value=2000, value=500, step=100)
        total_time = st.slider("Total Simulation Time (s)", 1, 100, 10)

    # --- Grid Setup ---
    nx = 100
    dx = L / nx
    dt = total_time / t_steps

    C = np.zeros(nx)
    C[0] = C0
    initial_C = C.copy()

    # --- Finite Difference Calculation ---
    for _ in range(t_steps):
        C[1:-1] = C[1:-1] + D * dt / dx ** 2 * (C[0:-2] - 2 * C[1:-1] + C[2:])

    x = np.linspace(0, L, nx)

    # --- Plot Result ---
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x, initial_C, '--', label="Initial", color='blue')
    ax.plot(x, C, '-', label="Final", color='green', linewidth=2)
    ax.set_title("Drug Diffusion Through Skin")
    ax.set_xlabel("Depth into Skin (m)")
    ax.set_ylabel("Concentration (mol/m³)")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    # --- Download Button ---
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    st.download_button("📥 Download Graph as PNG", buf.getvalue(), file_name="drug_diffusion_plot.png", mime="image/png")

    # --- Metrics ---
    st.success(f"✅ Peak penetration depth: {L:.4f} m")
    st.metric("Final Surface Concentration", f"{C[0]:.3f} mol/m³")
    st.metric("Final Inner Concentration", f"{C[-1]:.5f} mol/m³")
# 🧪 Module 1: Transdermal Drug Diffusion Simulator | MassTransferAI Suite
# 📘 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng
# 💡 Real-World Case: Simulating drug diffusion through human skin

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io


def run():
    st.header("🧪 Transdermal Drug Diffusion Simulator")
    st.markdown("Simulates 1D diffusion of a drug through skin using Fick's Law and finite difference method.")

    # --- Drug Database ---
    drug_data = {
        "Custom": None,
        "Aspirin": 3.5e-10,
        "Nicotine": 1.2e-9,
        "Fentanyl": 2.4e-10,
        "Testosterone": 5.5e-10
    }

    # --- User Inputs ---
    col1, col2 = st.columns(2)
    with col1:
        drug = st.selectbox("Select Drug", list(drug_data.keys()))
        if drug != "Custom":
            D = drug_data[drug]
            st.info(f"Using Diffusion Coefficient: {D:.1e} m²/s for {drug}")
        else:
            D = st.number_input("Diffusion Coefficient (m²/s)", min_value=1e-10, max_value=1e-4, value=1e-6,
                                format="%.1e")

        L = st.number_input("Skin Thickness (m)", min_value=0.0001, max_value=0.01, value=0.002, format="%.4f")
        C0 = st.number_input("Initial Drug Concentration at Surface (mol/m³)", value=1.0)

    with col2:
        t_steps = st.slider("Time Steps", min_value=100, max_value=2000, value=500, step=100)
        total_time = st.slider("Total Simulation Time (s)", 1, 100, 10)

    # --- Grid Setup ---
    nx = 100
    dx = L / nx
    dt = total_time / t_steps

    C = np.zeros(nx)
    C[0] = C0
    initial_C = C.copy()

    # --- Finite Difference Calculation ---
    for _ in range(t_steps):
        C[1:-1] = C[1:-1] + D * dt / dx ** 2 * (C[0:-2] - 2 * C[1:-1] + C[2:])

    x = np.linspace(0, L, nx)

    # --- Plot Result ---
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x, initial_C, '--', label="Initial", color='blue')
    ax.plot(x, C, '-', label="Final", color='green', linewidth=2)
    ax.set_title("Drug Diffusion Through Skin")
    ax.set_xlabel("Depth into Skin (m)")
    ax.set_ylabel("Concentration (mol/m³)")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    # --- Download Button ---
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    st.download_button("📥 Download Graph as PNG", buf.getvalue(), file_name="drug_diffusion_plot.png", mime="image/png")

    # --- Metrics ---
    st.success(f"✅ Peak penetration depth: {L:.4f} m")
    st.metric("Final Surface Concentration", f"{C[0]:.3f} mol/m³")
    st.metric("Final Inner Concentration", f"{C[-1]:.5f} mol/m³")
# 🧪 Module 1: Transdermal Drug Diffusion Simulator | MassTransferAI Suite
# 📘 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng
# 💡 Real-World Case: Simulating drug diffusion through human skin

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io


def run():
    st.header("🧪 Transdermal Drug Diffusion Simulator")
    st.markdown("Simulates 1D diffusion of a drug through skin using Fick's Law and finite difference method.")

    # --- Drug Database ---
    drug_data = {
        "Custom": None,
        "Aspirin": 3.5e-10,
        "Nicotine": 1.2e-9,
        "Fentanyl": 2.4e-10,
        "Testosterone": 5.5e-10
    }

    # --- User Inputs ---
    col1, col2 = st.columns(2)
    with col1:
        drug = st.selectbox("Select Drug", list(drug_data.keys()))
        if drug != "Custom":
            D = drug_data[drug]
            st.info(f"Using Diffusion Coefficient: {D:.1e} m²/s for {drug}")
        else:
            D = st.number_input("Diffusion Coefficient (m²/s)", min_value=1e-10, max_value=1e-4, value=1e-6,
                                format="%.1e")

        L = st.number_input("Skin Thickness (m)", min_value=0.0001, max_value=0.01, value=0.002, format="%.4f")
        C0 = st.number_input("Initial Drug Concentration at Surface (mol/m³)", value=1.0)

    with col2:
        t_steps = st.slider("Time Steps", min_value=100, max_value=2000, value=500, step=100)
        total_time = st.slider("Total Simulation Time (s)", 1, 100, 10)

    # --- Grid Setup ---
    nx = 100
    dx = L / nx
    dt = total_time / t_steps

    C = np.zeros(nx)
    C[0] = C0
    initial_C = C.copy()

    # --- Finite Difference Calculation ---
    for _ in range(t_steps):
        C[1:-1] = C[1:-1] + D * dt / dx ** 2 * (C[0:-2] - 2 * C[1:-1] + C[2:])

    x = np.linspace(0, L, nx)

    # --- Plot Result ---
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x, initial_C, '--', label="Initial", color='blue')
    ax.plot(x, C, '-', label="Final", color='green', linewidth=2)
    ax.set_title("Drug Diffusion Through Skin")
    ax.set_xlabel("Depth into Skin (m)")
    ax.set_ylabel("Concentration (mol/m³)")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    # --- Download Button ---
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    st.download_button("📥 Download Graph as PNG", buf.getvalue(), file_name="drug_diffusion_plot.png", mime="image/png")

    # --- Metrics ---
    st.success(f"✅ Peak penetration depth: {L:.4f} m")
    st.metric("Final Surface Concentration", f"{C[0]:.3f} mol/m³")
    st.metric("Final Inner Concentration", f"{C[-1]:.5f} mol/m³")
