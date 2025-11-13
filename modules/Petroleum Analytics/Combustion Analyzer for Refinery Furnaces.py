# 📘 Module 8: Combustion Analyzer | PetroStream AI Suite
# 🔥 Calculate excess air, O₂ balance, heat loss & combustion efficiency
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

def run():
    st.set_page_config(page_title="🔥 Combustion Analyzer", layout="centered")
    st.title("🔥 Combustion Analyzer for Refinery Furnaces")
    st.markdown("Analyze combustion performance and optimize furnace operations.")

    st.sidebar.header("📥 Furnace Input Parameters")

    o2_measured = st.sidebar.slider("O₂ in Flue Gas (%)", 0.0, 20.0, 4.0)
    stack_temp = st.sidebar.slider("Stack Temperature (°C)", 100, 400, 250)
    ambient_temp = st.sidebar.slider("Ambient Air Temperature (°C)", 0, 50, 25)
    fuel_lhv = st.sidebar.number_input("Fuel Lower Heating Value (kJ/kg)", value=43000.0)
    flue_gas_cp = st.sidebar.number_input("Flue Gas Specific Heat (kJ/kg-K)", value=1.05)
    excess_air_target = st.sidebar.slider("Target Excess Air (%)", 5, 30, 15)

    # === Calculations ===
    st.subheader("🧪 Combustion Analysis Results")

    # 1. Excess Air Calculation
    excess_air = (21 / (21 - o2_measured) - 1) * 100

    # 2. Heat Loss via Stack
    delta_T = stack_temp - ambient_temp
    heat_loss = delta_T * flue_gas_cp  # per kg of flue gas

    # 3. Combustion Efficiency
    efficiency = (1 - (heat_loss / fuel_lhv)) * 100

    # 4. Efficiency Deviation
    target_eff = (1 - ((stack_temp - ambient_temp) * flue_gas_cp / fuel_lhv)) * 100
    efficiency_gap = target_eff - efficiency

    # === Display Metrics ===
    st.metric("💨 Excess Air", f"{excess_air:.2f} %", delta=f"{excess_air - excess_air_target:.2f}")
    st.metric("🔥 Heat Loss via Stack", f"{heat_loss:.2f} kJ/kg flue gas")
    st.metric("⚙️ Combustion Efficiency", f"{efficiency:.2f} %", delta=f"{efficiency_gap:.2f}")
    st.metric("🎯 Target Efficiency", f"{target_eff:.2f} %")

    # === Gauge Plot ===
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=efficiency,
        delta={'reference': target_eff},
        title={'text': "Combustion Efficiency (%)"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 70], 'color': "red"},
                {'range': [70, 85], 'color': "orange"},
                {'range': [85, 100], 'color': "lightgreen"},
            ],
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

    # === Suggestions ===
    st.subheader("🧠 Optimization Suggestions")
    if excess_air > (excess_air_target + 5):
        st.warning("🔧 Reduce excess air to improve efficiency. Consider tuning air-fuel ratio.")
    elif excess_air < (excess_air_target - 5):
        st.warning("⚠️ Low excess air — risk of incomplete combustion. Monitor CO levels.")
    else:
        st.success("✅ Excess air is within the optimal range.")
