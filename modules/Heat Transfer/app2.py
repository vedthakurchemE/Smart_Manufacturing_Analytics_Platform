# 🔥 HeatTransfer AI Suite | Main Launcher
# 🎛️ Central dashboard to run all heat transfer simulation tools
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import os
import sys

def run():
    # ✅ Add tools folder to sys.path
    tools_folder = os.path.join(os.path.dirname(__file__), "tools")
    sys.path.append(tools_folder)

    # === Streamlit Page Setup ===
    st.set_page_config(page_title="🔥 Heat Transfer Suite", layout="centered")

    # === Title ===
    st.title("🔥 Heat Transfer Suite")
    st.markdown("💡 A suite of 10 advanced tools for heat transfer analysis and simulation.")
    st.markdown("🚀 Select a module from the sidebar to begin.")

    # === Sidebar Navigation ===
    st.sidebar.title("🧭 Navigation")

    modules = {
        "1️⃣ Heat Loss Through Wall": "_heat_loss_wall",
        "2️⃣ Boiling Heat Transfer": "boiling_heat_transfer",
        "3️⃣ Condensation Estimator": "condensation_estimator",
        "4️⃣ Cooking Time Estimator": "cooking_time_estimator",
        "5️⃣ Heat Exchanger Designer": "heat_exchanger_designer",
        "6️⃣ Heat Exchanger Effectiveness": "heat_exchanger_effectiveness",
        "7️⃣ Overall Heat Transfer": "overall_heat_transfer",
        "8️⃣ Thermal Conductivity Estimator": "thermal_conductivity_estimator",
        "9️⃣ Thermal Resistance Network": "thermal_resistance_network",
        "🔟 Transient Conduction Visualizer": "transient_conduction_visualizer"
    }

    selected = st.sidebar.radio("📂 Select Module", list(modules.keys()))
    filename = modules[selected] + ".py"
    filepath = os.path.join(tools_folder, filename)

    # === Load and Run Selected Module ===
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        exec(code, globals())
        run()  # Make sure each file defines `def run():`
    except FileNotFoundError:
        st.error(f"❌ Module file not found: `{filename}`. Please check the filename.")
    except Exception as e:
        st.error(f"❌ Error while loading `{filename}`:\n\n`{e}`")

    # === Footer ===
    st.markdown("---")
    st.caption("👨‍🔬 Built by Ved Thakur | BTech ChemEng | IPS Academy Indore")
