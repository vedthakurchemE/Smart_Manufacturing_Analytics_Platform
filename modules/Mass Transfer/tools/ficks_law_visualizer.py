# 📘 Module 3: Fick’s Law 1D Visualizer | MassTransferAI Suite
# 📊 Visualize and simulate 1D mass transfer using Fick's First Law
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io

def run():
    st.title("📈 Fick’s Law 1D Visualizer")
    st.markdown(r"""
    Visualize 1D steady-state diffusion using Fick’s First Law:  
    \n$J = -D \cdot \frac{dC}{dx}$  
    Useful for studying membranes, slabs, or barrier materials.
    """)

    # --- Sidebar ---
    st.sidebar.header("🔧 Simulation Parameters")
    L = st.sidebar.slider("Length of Domain (m)", 0.01, 1.0, 0.1, step=0.01)
    C1 = st.sidebar.slider("Concentration at x=0 (mol/m³)", 0.0, 10.0, 5.0)
    C2 = st.sidebar.slider("Concentration at x=L (mol/m³)", 0.0, 10.0, 0.0)
    D = st.sidebar.slider("Diffusivity D (m²/s)", 1e-12, 1e-6, 1e-9, format="%.1e")

    # --- Core Calculations ---
    x = np.linspace(0, L, 100)
    Cx = C1 + (C2 - C1) * (x / L)
    J = -D * (C2 - C1) / L

    # --- Plotting ---
    st.subheader("📉 Concentration Profile (1D Slab)")
    fig, ax = plt.subplots()
    ax.plot(x, Cx, color='darkgreen', linewidth=2)
    ax.set_xlabel("Distance x (m)")
    ax.set_ylabel("Concentration C(x) (mol/m³)")
    ax.set_title("Steady-State Concentration Profile")
    ax.grid(True)

    # --- Add flux arrow ---
    arrow_x = L / 2
    arrow_y = C1 + (C2 - C1) / 2
    ax.annotate('', xy=(arrow_x + 0.02 * L, arrow_y), xytext=(arrow_x - 0.02 * L, arrow_y),
                arrowprops=dict(facecolor='red', shrink=0.05), annotation_clip=False)
    ax.text(arrow_x, arrow_y + 0.3, 'Flux →', color='red', ha='center', fontsize=10)

    st.pyplot(fig)

    # --- PNG Download ---
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    st.download_button("📸 Download Plot as PNG", buf.getvalue(), file_name="ficks_1d_plot.png", mime="image/png")

    # --- Result Metric ---
    st.success(f"Calculated Steady-State Diffusion Flux J = {J:.2e} mol/m²·s")

    # --- Downloadable Report ---
    report = f"""
Fick’s Law 1D Simulation Report
---------------------------------------
Length of Slab: {L:.4f} m
Concentration at x=0: {C1:.3f} mol/m³
Concentration at x=L: {C2:.3f} mol/m³
Diffusivity: {D:.1e} m²/s

→ Flux J = {J:.2e} mol/m²·s
"""
    st.download_button("📄 Download .txt Report", report, file_name="ficks_law_1d_report.txt")

    # --- Units Explanation ---
    with st.expander("📘 Units & Theory"):
        st.latex(r"J = -D \cdot \frac{dC}{dx}")
        st.markdown("""
        - **D**: Diffusivity in m²/s  
        - **C(x)**: Concentration profile in mol/m³  
        - **x**: Distance in meters  
        - **J**: Diffusion Flux in mol/m²·s  
        - Profile assumes **steady-state** linear diffusion with constant D.
        """)
