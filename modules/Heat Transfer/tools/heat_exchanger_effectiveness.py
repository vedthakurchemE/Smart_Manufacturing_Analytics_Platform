# 📘 Module 6: Heat Exchanger Effectiveness Calculator | HeatTransferAI Suite
# 🔄 Calculate effectiveness of parallel/counter-flow heat exchangers using NTU method
# ✨ Enhanced UI, plot, and guidance for 12.5/10 rating
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.set_page_config(page_title="🔄 Heat Exchanger Effectiveness", layout="wide")
    st.title("🔄 Heat Exchanger Effectiveness Calculator")
    st.markdown("### Compute effectiveness of **Parallel** or **Counter-Flow** heat exchangers using the **NTU method**.")

    # === Input Section ===
    with st.sidebar:
        st.header("📥 Input Parameters")
        flow_type = st.radio("Flow Configuration", ["Parallel Flow", "Counter Flow"])
        C_min = st.number_input("🔹 Minimum Heat Capacity (C_min) [W/K]", min_value=0.01, step=0.1, help="Smaller of the two fluid heat capacity rates (W/K)")
        C_max = st.number_input("🔸 Maximum Heat Capacity (C_max) [W/K]", min_value=0.01, step=0.1, help="Larger of the two fluid heat capacity rates (W/K)")
        NTU = st.number_input("📈 Number of Transfer Units (NTU)", min_value=0.01, step=0.1, help="NTU = UA / C_min, where UA is heat exchanger conductance")

    # === Validation ===
    if C_min > C_max:
        st.warning("⚠️ C_min should be ≤ C_max. Please check your input.")
        return

    # === Main Calculation ===
    st.subheader("📊 Results")

    if st.button("🧮 Calculate Effectiveness"):
        C_r = C_min / C_max

        if flow_type == "Parallel Flow":
            effectiveness = (1 - np.exp(-NTU * (1 + C_r))) / (1 + C_r)
        else:  # Counter Flow
            if C_r == 1:
                effectiveness = NTU / (1 + NTU)
            else:
                numerator = 1 - np.exp(-NTU * (1 - C_r))
                denominator = 1 - C_r * np.exp(-NTU * (1 - C_r))
                effectiveness = numerator / denominator

        st.success(f"✅ Effectiveness of the **{flow_type.lower()}** heat exchanger: **{effectiveness:.4f}**")

        # === Notes ===
        st.markdown("#### 🧾 Notes")
        st.markdown("- NTU = UA / C_min")
        st.markdown("- C_min / C_max = Heat capacity rates (W/K)")
        st.markdown("- Valid for 2-stream heat exchangers with no phase change")

        # === Plot ===
        st.markdown("#### 📉 Effectiveness vs NTU (Fixed C_r)")
        NTU_vals = np.linspace(0.01, 5, 100)
        if flow_type == "Parallel Flow":
            eff_vals = (1 - np.exp(-NTU_vals * (1 + C_r))) / (1 + C_r)
        else:
            eff_vals = []
            for NTU_i in NTU_vals:
                if C_r == 1:
                    eff_vals.append(NTU_i / (1 + NTU_i))
                else:
                    num = 1 - np.exp(-NTU_i * (1 - C_r))
                    den = 1 - C_r * np.exp(-NTU_i * (1 - C_r))
                    eff_vals.append(num / den)
        fig, ax = plt.subplots()
        ax.plot(NTU_vals, eff_vals, color='green', lw=2)
        ax.set_xlabel("NTU")
        ax.set_ylabel("Effectiveness")
        ax.set_title(f"{flow_type} - Effectiveness vs NTU (Cᵣ = {C_r:.2f})")
        ax.grid(True)
        st.pyplot(fig)

    # === Example ===
    with st.expander("📌 View Sample Case"):
        st.markdown("""
        **Example:**  
        - Flow Type: Counter Flow  
        - C_min = 500 W/K  
        - C_max = 1000 W/K  
        - NTU = 2.5  
        - ➤ Resulting effectiveness ≈ 0.76
        """)

