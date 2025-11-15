# 🛢️ PetroStream AI Tools Launcher | app6.py
# ✅ Runs 12 intelligent tools from /tools folder
# 👨‍🔬 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import os
import sys

def run():
    # ✅ Add tools folder to path
    tools_folder = os.path.join(os.path.dirname(__file__), "tools")
    sys.path.append(tools_folder)

    # === Page Config ===
    st.set_page_config(page_title="🛢️ PetroStream AI Suite", layout="centered")

    st.title("🛢️ PetroStream AI Tool Suite")
    st.markdown("📊 A collection of advanced analytics, optimization, and monitoring tools.")
    st.markdown("🚀 Select any module from the sidebar.")

    # === Sidebar Modules ===
    st.sidebar.title("📂 Modules")

    modules = {
        "1️⃣ Emission Estimator": "emission_estimator",
        "2️⃣ Energy Efficiency Analyzer": "energy_efficiency_analyzer",
        "3️⃣ Fuel Efficiency Analyzer": "fuel_efficiency_analyzer",
        "4️⃣ Props Data Viewer": "props",
        "5️⃣ Process Optimization Dashboard": "Process_Optimization_Dashboard",
        "6️⃣ Combustion Efficiency Simulator": "combustion_efficiency_simulator",
        "7️⃣ Combustion Calculator": "combustion",
        "8️⃣ Equipment Efficiency Analyzer": "Equipment_Efficiency_Analyzer",
        "9️⃣ Energy Loss Visualizer": "energy_loss_visualizer",
        "🔟 Process Variability Analyzer": "process_variability",
        "1️⃣1️⃣ Equipment Failure Predictor": "equipment_failure_predictor",
        "1️⃣2️⃣ Yield Predictor": "yield_predictor"
    }

    selected = st.sidebar.radio("🧭 Select Module", list(modules.keys()))
    filename = modules[selected] + ".py"
    filepath = os.path.join(tools_folder, filename)

    # === Module Execution ===
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        exec(code, globals())
        run()  # ⚠️ Each module must define `def run()`
    except FileNotFoundError:
        st.error(f"❌ File not found: `{filename}`")
    except Exception as e:
        st.error(f"❌ Error loading `{filename}`:\n\n`{e}`")

st.caption("👤 Ved Thakur | Semester 1 | IPS Academy Indore | B.Tech ChemEng | 2025-2029")
