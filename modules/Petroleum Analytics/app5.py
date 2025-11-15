# 🛢️ PetroStream AI Suite | Main Launcher
# 🎛️ Central dashboard to run all petroleum analytics tools
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import os
import sys

def run():
    # ✅ Ensure this directory is in the path for dynamic imports
    sys.path.append(os.path.dirname(__file__))

    # === Streamlit Page Config ===
    st.set_page_config(page_title="🛢️ PetroStream AI Suite", layout="centered")

    # === Main Title ===
    st.title("🛢️ PetroStream AI Suite")
    st.markdown("💡 A Streamlit-powered suite of 10 professional-grade petroleum analytics tools.")
    st.markdown("🚀 Select a module from the sidebar to begin.")

    # === Sidebar Navigation ===
    st.sidebar.title("🧭 Navigation")

    modules = {
        "1️⃣ Crude Oil Blend Optimization": "Crude Oil Blend Optimizer",
        "2️⃣ Refinery Product Yield Predictor": "Refinery Product Yield Predictor",
        "3️⃣ Real-Time Emission Estimator": "Real-Time Emission Estimator",
        "4️⃣ Energy Loss Visualizer in Heat Exchangers": "Energy Loss Visualizer in Heat Exchangers",
        "5️⃣ Catalyst Life Cycle Analyzer": "Catalyst Life Cycle Analyzer",
        "6️⃣ Petroleum Inventory Forecasting": "Petroleum Inventory Forecasting",
        "7️⃣ Pump & Compressor Fault Detection System": "Pump & Compressor Fault Detection System",
        "8️⃣ Combustion Analyzer for Refinery Furnaces": "Combustion Analyzer for Refinery Furnaces",
        "9️⃣ Petroleum Supply Chain Optimizer": "Petroleum Supply Chain Optimizer",
        "🔟 Petroleum Lab Data Auto-Analyzer": "Petroleum Lab Data Auto-Analyzer"
    }

    selection = st.sidebar.radio("📂 Select Module", list(modules.keys()))
    module_filename = modules[selection] + ".py"
    module_path = os.path.join(os.path.dirname(__file__), module_filename)

    # === Module Execution ===
    try:
        with open(module_path, 'r', encoding='utf-8') as f:
            code = f.read()
        # Execute code inside the global scope
        exec(code, globals())
        run()  # Each module must have a `run()` function defined
    except FileNotFoundError:
        st.error(f"❌ Module file not found: `{module_filename}`. Please check the filename.")
    except Exception as e:
        st.error(f"❌ Error while loading `{module_filename}`:\n\n`{e}`")


