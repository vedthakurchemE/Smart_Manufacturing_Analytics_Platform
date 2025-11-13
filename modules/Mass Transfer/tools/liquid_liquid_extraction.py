# 📘 Module 9: Liquid-Liquid Extraction Designer | MassTransferAI Suite
# 💧 Simulates counter-current LLE using McCabe-Thiele method
# 👨‍💻 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def run():
    st.title("💧 Liquid-Liquid Extraction Designer")

    st.markdown("""
    Simulate **counter-current liquid-liquid extraction** and estimate the  
    **number of ideal stages** using the **McCabe-Thiele method**.

    ✅ Used for solvent extraction design in systems with two immiscible liquids.
    """)

    # --- User Inputs ---
    st.sidebar.header("🔧 Extraction Settings")
    feed_conc = st.sidebar.slider("Feed Solute Concentration (xF)", 0.1, 0.9, 0.5, 0.01)
    raff_conc = st.sidebar.slider("Raffinate Exit Concentration (xR)", 0.01, feed_conc, 0.1, 0.01)
    extract_conc = st.sidebar.slider("Solvent Entry Concentration (yS)", 0.0, 0.5, 0.0, 0.01)
    SbyF = st.sidebar.slider("Solvent to Feed Ratio (S/F)", 0.5, 5.0, 1.0, 0.1)
    KD = st.sidebar.slider("Equilibrium Slope (K_D)", 0.3, 3.0, 1.0, 0.1)

    st.markdown("---")
    st.subheader("📈 McCabe-Thiele Diagram")

    # --- Equilibrium and Operating Lines ---
    x_vals = np.linspace(raff_conc, feed_conc, 200)
    y_eq = KD * x_vals
    y_op = extract_conc + SbyF * (feed_conc - x_vals)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(x_vals, y_eq, label="Equilibrium Line", color="blue", linewidth=2)
    ax.plot(x_vals, y_op, label="Operating Line", color="green", linestyle="--", linewidth=2)

    # --- Stepping Procedure ---
    stages = 0
    x, y = feed_conc, extract_conc
    stage_points = [(x, y)]
    max_stages = 50
    valid = True

    while x > raff_conc and stages < max_stages:
        y = KD * x
        stage_points.append((x, y))
        x_new = x - (y - extract_conc) / SbyF
        stage_points.append((x_new, y))
        if x_new >= x:  # Infinite loop guard
            valid = False
            break
        x = x_new
        stages += 1

    if x <= raff_conc and valid:
        st.success(f"✅ Estimated Number of Ideal Stages: `{stages}`")
    else:
        st.warning("⚠️ More than 50 stages needed or invalid design (check slope/S/F).")

    # --- Draw stepping lines ---
    for i in range(0, len(stage_points) - 1, 2):
        ax.plot([stage_points[i][0], stage_points[i+1][0]],
                [stage_points[i][1], stage_points[i+1][1]], 'k')
        if i+2 < len(stage_points):
            ax.plot([stage_points[i+1][0], stage_points[i+2][0]],
                    [stage_points[i+1][1], stage_points[i+2][1]], 'k')

    ax.set_xlabel("x (Raffinate Phase)")
    ax.set_ylabel("y (Extract Phase)")
    ax.set_title("LLE: McCabe-Thiele Method")
    ax.grid(True)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, max(1.0, max(y_eq)))
    ax.legend()
    st.pyplot(fig)

    # --- Downloadable Report ---
    report = f"""
Liquid-Liquid Extraction Design Report
--------------------------------------
Feed Solute Concentration (xF):     {feed_conc:.3f}
Raffinate Exit Concentration (xR):  {raff_conc:.3f}
Solvent Entry Concentration (yS):   {extract_conc:.3f}
Solvent/Feed Ratio (S/F):           {SbyF:.2f}
Distribution Coefficient (K_D):     {KD:.2f}
Estimated Ideal Stages:             {stages if valid else 'Invalid or >50'}
"""
    st.download_button("⬇️ Download Report", report, file_name="LLE_design_report.txt")

    # --- Engineering Notes ---
    with st.expander("📘 Engineering Notes"):
        st.markdown("""
        - **Ideal Stages** assume perfect contact between phases in each stage.
        - Try increasing `S/F` or choosing a better solvent (higher `K_D`) to reduce stage count.
        - For non-linear systems, replace linear `K_D·x` with interpolated lab data.
        - Always ensure `yS < y_eq(xF)` for physical feasibility.

        🧪 Common Applications:
        - Acetic acid extraction using isopropyl ether  
        - Penicillin recovery from fermentation broth  
        - Aromatic/aliphatic separation using furfural  
        """)
