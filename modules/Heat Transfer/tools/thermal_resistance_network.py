# 📘 Module 10: Thermal Resistance Network Visualizer | HeatTransferAI Suite
# 🌡️ Visualize and calculate total resistance in series/parallel heat conduction paths
# ✨ Enhanced Version: Sankey-like diagram, annotations, real-world notes
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


def draw_series(ax, resistances):
    x = 0
    for i, R in enumerate(resistances):
        ax.add_patch(patches.FancyArrowPatch((x, 0), (x + 1, 0), arrowstyle='->', linewidth=3))
        ax.text(x + 0.5, 0.1, f"R{i + 1}={R}K/W", ha='center', fontsize=10)
        x += 1
    ax.set_xlim(-0.5, x + 0.5)
    ax.set_ylim(-1, 1)
    ax.axis('off')


def draw_parallel(ax, resistances):
    for i, R in enumerate(resistances):
        ax.add_patch(patches.FancyArrowPatch((0, -i), (1, -i), arrowstyle='->', linewidth=3))
        ax.text(0.5, -i + 0.1, f"R{i + 1}={R}K/W", ha='center', fontsize=10)
    ax.set_xlim(-0.2, 1.2)
    ax.set_ylim(-len(resistances) + 0.5, 0.5)
    ax.axis('off')


def run():
    st.set_page_config(page_title="🌡️ Thermal Resistance Network", layout="wide")
    st.title("🌡️ Thermal Resistance Network Visualizer")
    st.markdown(
        "Visualize and compute total **thermal resistance** in series or parallel conduction paths. Ideal for **walls, fins, PCBs, HVAC** and more.")

    network_type = st.selectbox("🔢 Select Resistance Network Type:", ["Series", "Parallel"])
    n = st.number_input("🧱 Number of Thermal Elements", min_value=2, value=3, step=1)

    resistances = []
    for i in range(n):
        R = st.number_input(f"R{i + 1} (K/W)", min_value=0.0001, value=0.5, key=f"R_{i}")
        resistances.append(R)

    if st.button("🧮 Calculate & Visualize"):
        try:
            if network_type == "Series":
                R_total = sum(resistances)
            else:
                R_total = 1 / sum(1 / r for r in resistances)

            st.success(f"✅ Total Thermal Resistance = **{R_total:.4f} K/W** ({network_type})")

            st.markdown("### 🧠 Resistance Network Diagram")
            fig, ax = plt.subplots(figsize=(8, 2 if network_type == "Series" else 2 + n * 0.5))
            if network_type == "Series":
                draw_series(ax, resistances)
            else:
                draw_parallel(ax, resistances)
            plt.text(0.5, -1.2 if network_type == "Series" else -n - 0.3,
                     f"Total Resistance = {R_total:.4f} K/W", fontsize=11, ha='center', color='green')
            st.pyplot(fig)

        except ZeroDivisionError:
            st.error("⚠️ One of the resistance values might be zero, which is not allowed for parallel networks.")

    st.markdown("### 🔍 Real-World Applications")
    st.markdown("- 🧱 Composite wall analysis with layers (foam + brick + insulation)")
    st.markdown("- 💻 Thermal resistance in CPUs, GPUs, microelectronics")
    st.markdown("- ❄️ Fin arrays and extended surfaces in HVAC and radiators")
    st.markdown("- 🔬 Semiconductor cooling and PCB substrate design")

    st.markdown("### 📘 Notes")
    st.info("""
- **K/W** (Kelvin per Watt) indicates resistance to heat flow.
- Use this tool to optimize multilayer systems, electronic cooling, or thermal packaging.

💡 Tip: For complex structures, combine series and parallel concepts.
""")

    st.markdown("---")
    st.caption("Module 10 | HeatTransferAI Suite © Ved Thakur")
