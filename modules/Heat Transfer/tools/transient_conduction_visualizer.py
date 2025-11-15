# 📘 Module 10: Transient Heat Conduction Simulator | MassTransferAI Suite
# 🔥 Visualize unsteady-state heat conduction in 1D slab (Explicit FDM)
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import cm
from io import BytesIO

def run_simulation(length, time_total, dx, dt, alpha, T_initial, T_left, T_right):
    Nx = int(length / dx) + 1
    Nt = int(time_total / dt) + 1

    T = np.ones(Nx) * T_initial
    T[0] = T_left
    T[-1] = T_right

    r = alpha * dt / dx**2
    T_matrix = np.zeros((Nt, Nx))
    T_matrix[0] = T

    for n in range(1, Nt):
        T_new = T.copy()
        for i in range(1, Nx - 1):
            T_new[i] = T[i] + r * (T[i+1] - 2*T[i] + T[i-1])
        T_new[0] = T_left
        T_new[-1] = T_right
        T = T_new.copy()
        T_matrix[n] = T
    return T_matrix, Nx, Nt, r

def run():
    st.set_page_config(page_title="🔥 Transient Heat Conduction Simulator", layout="wide")
    st.title("🌡️ Transient Heat Conduction Visualizer (1D Slab)")
    st.markdown("Visualize **unsteady heat flow** in a slab using explicit finite difference method.")

    with st.sidebar:
        st.header("🧾 Input Parameters")
        length = st.slider("📏 Slab Length [m]", 0.01, 1.0, 0.1)
        time_total = st.slider("⏱️ Simulation Time [s]", 1, 1000, 200)
        dx = st.slider("🔧 Spatial Step dx [m]", 0.001, 0.05, 0.01)
        dt = st.slider("🔧 Time Step dt [s]", 0.001, 1.0, 0.05)
        alpha = st.number_input("α - Thermal Diffusivity [m²/s]", 1e-6, 1e-4, 1.1e-5, format="%.1e")
        T_initial = st.number_input("🌡️ Initial Temperature [°C]", -100, 500, 25)
        T_left = st.number_input("⬅️ Left Boundary Temp [°C]", -100, 500, 100)
        T_right = st.number_input("➡️ Right Boundary Temp [°C]", -100, 500, 0)

    T_matrix, Nx, Nt, r = run_simulation(length, time_total, dx, dt, alpha, T_initial, T_left, T_right)

    st.subheader("📊 Temperature Profiles at Selected Times")
    time_list = [int(dt * i) for i in range(0, Nt, max(1, Nt // 10))]

    # ✅ Ensure default values exist in time_list
    default_steps = [0, int(time_total / 2), int(time_total)]
    valid_defaults = [t for t in default_steps if t in time_list]
    times_to_plot = st.multiselect("Pick time steps to visualize:", time_list, default=valid_defaults)

    x = np.linspace(0, length, Nx)
    fig1, ax1 = plt.subplots()
    for t_sec in times_to_plot:
        t_idx = int(t_sec / dt)
        if t_idx < Nt:
            ax1.plot(x, T_matrix[t_idx], label=f"t = {t_sec}s")
    ax1.set_xlabel("Position [m]")
    ax1.set_ylabel("Temperature [°C]")
    ax1.set_title("1D Transient Heat Conduction")
    ax1.grid(True)
    ax1.legend()
    st.pyplot(fig1)

    st.markdown("### 🧠 Stability Check")
    st.markdown(f"**r = α·dt/dx² = `{r:.4f}`**")
    if r >= 0.5:
        st.error("⚠️ Unstable Simulation: r ≥ 0.5. Decrease `dt` or increase `dx`.")
    else:
        st.success("✅ Stable Simulation: r < 0.5")

    st.subheader("🧩 3D Surface Plot of Temperature (Position vs Time)")
    fig2 = plt.figure(figsize=(8, 5))
    ax2 = fig2.add_subplot(111, projection='3d')

    X, Y = np.meshgrid(x, np.linspace(0, time_total, Nt))
    ax2.plot_surface(X, Y, T_matrix, cmap=cm.viridis)
    ax2.set_xlabel("Position [m]")
    ax2.set_ylabel("Time [s]")
    ax2.set_zlabel("Temperature [°C]")
    ax2.set_title("Temperature Surface")
    st.pyplot(fig2)

    st.subheader("📥 Download Data")
    df = pd.DataFrame(T_matrix, columns=[f"x={xi:.2f}m" for xi in x])
    df.insert(0, "Time (s)", [i * dt for i in range(Nt)])
    csv = df.to_csv(index=False).encode()
    st.download_button("⬇️ Download Full Temp Matrix as CSV", csv, "temperature_matrix.csv", "text/csv")

    with st.expander("📘 Theory: Explicit Finite Difference Method"):
        st.markdown(r"""
        The **1D transient heat conduction equation**:

        \[
        \frac{\partial T}{\partial t} = \alpha \frac{\partial^2 T}{\partial x^2}
        \]

        is discretized using the **explicit method**:

        \[
        T_i^{n+1} = T_i^n + r \cdot (T_{i+1}^n - 2T_i^n + T_{i-1}^n)
        \quad \text{where} \quad r = \frac{\alpha \cdot \Delta t}{(\Delta x)^2}
        \]

        Stability condition: `r < 0.5`
        """)

    st.markdown("---")
    st.info("💡 Tip: Try different α and boundary conditions to simulate various materials and cooling scenarios.")

