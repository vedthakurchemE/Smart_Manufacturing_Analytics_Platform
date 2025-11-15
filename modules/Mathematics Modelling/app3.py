# 📐 MathModelAI Suite | app3.py
import streamlit as st
import os
import sys
import importlib.util

def run():
    folder = os.path.dirname(__file__)
    tools_folder = os.path.join(folder, "tools")
    sys.path.append(tools_folder)

    st.set_page_config(page_title="📐 MathModelAI Suite", layout="centered")
    st.title("📐 MathModelAI Suite")
    st.markdown("🧠 A professional suite of mathematical modeling tools.")
    st.markdown("🚀 Use the sidebar to launch any module.")

    st.sidebar.title("📊 Select a Modeling Tool")
    modules = {
        "1️⃣ Agent-Based Model": "agent_based",
        "2️⃣ Contact Network Simulation": "contact_network",
        "3️⃣ Data Visualizer": "data_visualizer",
        "4️⃣ Healthcare Forecaster": "healthcare_forecaster",
        "5️⃣ Policy Simulator": "policy_simulator",
        "6️⃣ R₀ Calculator": "r0_calculator",
        "7️⃣ Report Generator": "report_generator",
        "8️⃣ SEIR Simulator": "seir_simulator",
        "9️⃣ Sensitivity Analysis": "sensitivity",
        "🔟 Vaccine Strategy Planner": "vaccine_strategy"
    }

    selected = st.sidebar.radio("📂 Module List", list(modules.keys()))
    filename = modules[selected] + ".py"
    filepath = os.path.join(tools_folder, filename)

    try:
        spec = importlib.util.spec_from_file_location("module.name", filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.run()  # ✅ Call run() from the imported module
    except FileNotFoundError:
        st.error(f"❌ File not found: `{filename}`.")
    except Exception as e:
        st.error(f"❌ Error loading `{filename}`:\n\n`{e}`")


