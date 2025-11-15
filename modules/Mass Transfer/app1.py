# 🧪 MassTransferAI Suite | Main Launcher
# 🎛️ Central dashboard to run all mass transfer simulation tools
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import os
import sys

def run():
    # ✅ Add tools folder to sys.path
    tools_folder = os.path.join(os.path.dirname(__file__), "tools")
    sys.path.append(tools_folder)

    # === Streamlit Page Config ===
    st.set_page_config(page_title="🧪 MassTransferAI Suite", layout="centered")

    # === App Title ===
    st.title("🧪 MassTransferAI Suite")
    st.markdown("💡 A professional simulation toolkit for core Mass Transfer operations.")
    st.markdown("🚀 Select a module from the sidebar to begin.")

    # === Sidebar Navigation ===
    st.sidebar.title("🧭 Navigation")

    modules = {
        "1️⃣ Diffusion Simulation": "diffusion_simulator",
        "2️⃣ Diffusivity Estimator": "diffusivity_estimator",
        "3️⃣ Drying Time Estimator": "drying_time_estimator",
        "4️⃣ Fick’s Law Visualizer": "ficks_law_visualizer",
        "5️⃣ Gas Absorber Design": "gas_absorber_design",
        "6️⃣ Gas Diffusion Loss": "gas_diffusion_loss",
        "7️⃣ Liquid-Liquid Extraction": "liquid_liquid_extraction",
        "8️⃣ Mass Flux Calculator": "mass_flux_calculator",
        "9️⃣ Mass Transfer Coefficient Estimator": "mass_transfer_coeff",
        "🔟 Packed Column Simulator": "packed_column_simulator"
    }

    selected = st.sidebar.radio("📂 Select Module", list(modules.keys()))
    filename = modules[selected] + ".py"
    filepath = os.path.join(tools_folder, filename)

    # === Run Selected Module Dynamically ===
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        exec(code, globals())
        run()  # 🔁 Each module must define `def run():`
    except FileNotFoundError:
        st.error(f"❌ Module file not found: `{filename}`. Please check the filename.")
    except Exception as e:
        st.error(f"❌ Error while loading `{filename}`:\n\n`{e}`")


