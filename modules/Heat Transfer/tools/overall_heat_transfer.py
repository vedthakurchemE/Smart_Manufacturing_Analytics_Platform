# 📘 Module 9: Overall Heat Transfer Coefficient Calculator | HeatTransferAI Suite
# 🧱 Estimate U value for composite walls, heat exchangers, or layered systems
# ✨ Enhanced by: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.set_page_config(page_title="Overall Heat Transfer Coefficient", layout="centered")

    # === Title and Description ===
    st.title("🧱 Overall Heat Transfer Coefficient (U) Calculator")
    st.markdown("""
    Estimate the **Overall Heat Transfer Coefficient (U)** for systems with multiple layers or resistances, 
    such as **composite walls, pipe systems, and heat exchangers**.
    """)

    st.markdown("### 🔢 Step 1: Enter Thermal Resistances")

    # === User Inputs ===
    n = st.number_input("🔹 Number of Layers (n)", min_value=1, value=3, help="Each layer contributes a thermal resistance.")
    resistances = []

    cols = st.columns(n)
    for i in range(n):
        with cols[i]:
            R = st.number_input(f"R{i+1} (m²·K/W)", min_value=0.0001, value=0.1, key=f"R_{i}",
                                help=f"Thermal resistance of layer {i+1}")
            resistances.append(R)

    A = st.number_input("📐 Heat Transfer Area A (m²)", min_value=0.01, value=1.0, help="Surface area over which heat is transferred.")

    # === Calculation ===
    if st.button("🚀 Calculate Overall U"):
        R_total = sum(resistances)
        U = 1 / R_total
        Q_per_K = U * A

        st.success(f"✅ Overall Heat Transfer Coefficient (U): **{U:.2f} W/m²·K**")
        st.markdown(f"🧮 **Total Thermal Resistance (R_total):** `{R_total:.4f} m²·K/W`")
        st.markdown(f"⚡ **UA Value (U × A):** `{Q_per_K:.2f} W/K` → Heat flow per unit ΔT")

        # === Formula Box ===
        st.markdown("### 📘 Formula Used")
        st.latex(r"U = \frac{1}{R_1 + R_2 + ... + R_n}")
        st.latex(r"Q = U \cdot A \cdot \Delta T")

        # === Plot ===
        fig, ax = plt.subplots(figsize=(8, 1.5))
        ax.barh([""], [r for r in resistances], left=np.cumsum([0] + resistances[:-1]), color="skyblue", edgecolor="black")
        ax.set_xlabel("Thermal Resistance (m²·K/W)")
        ax.set_title("🧱 Layer-wise Resistance Profile")
        ax.get_yaxis().set_visible(False)
        st.pyplot(fig)

        # === Application Section ===
        st.markdown("### 🌍 Real-World Applications")
        st.markdown("""
        - 🏭 **Heat exchanger** shell and tube analysis  
        - 🧊 **Insulated walls** in cold storage or housing  
        - 🚰 **Pipes** with internal/external insulation  
        - 🌡️ HVAC thermal loss analysis  
        """)


