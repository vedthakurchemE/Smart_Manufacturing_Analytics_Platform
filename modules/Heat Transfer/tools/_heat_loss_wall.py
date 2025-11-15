# 📘 Heat Loss Through Composite Wall | MassTransferAI Suite - Heat Transfer Module
# 🧱 Estimate total thermal resistance and heat loss through multi-layer walls
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st

def run():
    st.title("🧱 Heat Loss Through Composite Wall")
    st.markdown("Estimate total thermal resistance and heat loss through a wall made of multiple layers.")

    st.sidebar.header("Wall Parameters")
    num_layers = st.sidebar.slider("Number of Layers", min_value=1, max_value=5, value=2)

    # Input: Temperatures & Area
    T_inside = st.number_input("🌡️ Inside Temperature (°C)", value=100.0)
    T_outside = st.number_input("❄️ Outside Temperature (°C)", value=30.0)
    area = st.number_input("📐 Wall Area (m²)", min_value=0.1, max_value=100.0, value=10.0, step=0.1)

    st.subheader("🔍 Layer-by-Layer Properties")

    total_resistance = 0.0

    # Thermal conductivity reference (W/m·K)
    material_library = {
        "Brick": 0.72,
        "Concrete": 1.4,
        "Insulation Foam": 0.03,
        "Glass": 1.0,
        "Custom": None
    }

    for i in range(num_layers):
        st.markdown(f"### 🧱 Layer {i+1}")
        thickness = st.number_input(
            f"🧱 Thickness of Layer {i+1} (m)",
            min_value=0.001, max_value=1.0, value=0.1, step=0.001,
            key=f"thickness_{i}"
        )

        selected = st.selectbox(
            f"🔎 Material of Layer {i+1}",
            list(material_library.keys()),
            key=f"material_{i}"
        )

        default_k = 0.04 if material_library[selected] is None else float(material_library[selected])

        conductivity = st.number_input(
            f"💡 Thermal Conductivity k (W/m·K) - Layer {i+1}",
            min_value=0.01, max_value=500.0, value=default_k,
            step=0.01, key=f"k_{i}"
        )

        resistance = thickness / conductivity
        total_resistance += resistance

        st.write(f"🧮 Thermal Resistance (R) of Layer {i+1}: `{resistance:.4f} °C/W`")

    st.markdown("---")
    st.subheader("🧠 Final Calculated Results")

    st.success(f"🔁 Total Thermal Resistance: `{total_resistance:.4f} °C/W`")

    try:
        heat_loss = (T_inside - T_outside) / total_resistance
        heat_loss_total = heat_loss * area
        st.info(f"🔥 Heat Loss per unit area: `{heat_loss:.2f} W/m²`")
        st.info(f"📦 Total Heat Loss: `{heat_loss_total:.2f} W`")
    except ZeroDivisionError:
        st.error("❌ Error: Total resistance is zero. Please check your inputs.")


