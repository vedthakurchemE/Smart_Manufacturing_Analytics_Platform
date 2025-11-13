# 📘 run.py - Mass Transfer AI Suite | AllProjectsSuite
# 💧 10 real-world tools for diffusion, drying, extraction & absorption
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st

# Import all 10 modules (each with a run() function)
from module1_diffusion_sim import run as run_diffusion
from module2_diffusivity_estimator import run as run_diffusivity
from module3_drying_time import run as run_drying
from module4_ficks_law import run as run_fick
from module5_gas_absorber import run as run_absorber
from module6_gas_diffusion_loss import run as run_gas_loss
from module7_liquid_extraction import run as run_extraction
from module8_mass_flux import run as run_flux
from module9_mass_transfer_coeff import run as run_coeff
from module10_packed_column import run as run_packed

def run():
    # === Page Config ===
    st.set_page_config(page_title="💧 Mass Transfer AI Suite", layout="wide")

    # === App Title ===
    st.title("💧 Mass Transfer AI Suite")
    st.markdown("""
    Explore 10 high-impact tools for real-world **mass transfer problems** in Chemical Engineering.

    🔧 Developed with: **Python + Streamlit**  
    📦 Author: **Ved Thakur**  
    🎯 Portfolio App | Part of: **AllProjectsSuite**
    ---
    """)

    # === Navigation Menu ===
    tool = st.selectbox("📚 Select a Module", [
        "1️⃣ Diffusion Simulator",
        "2️⃣ Diffusivity Estimator",
        "3️⃣ Drying Time Estimator",
        "4️⃣ Fick’s Law Visualizer",
        "5️⃣ Gas Absorber Design",
        "6️⃣ Gas Diffusion Loss",
        "7️⃣ Liquid-Liquid Extraction",
        "8️⃣ Mass Flux Calculator",
        "9️⃣ Mass Transfer Coefficient Estimator",
        "🔟 Packed Column Simulator"
    ])

    # === Routing to Modules ===
    if tool.startswith("1"):
        run_diffusion()
    elif tool.startswith("2"):
        run_diffusivity()
    elif tool.startswith("3"):
        run_drying()
    elif tool.startswith("4"):
        run_fick()
    elif tool.startswith("5"):
        run_absorber()
    elif tool.startswith("6"):
        run_gas_loss()
    elif tool.startswith("7"):
        run_extraction()
    elif tool.startswith("8"):
        run_flux()
    elif tool.startswith("9"):
        run_coeff()
    elif tool.startswith("🔟") or tool.startswith("10"):
        run_packed()

    # === Footer ===
    st.markdown("---")
    st.markdown("🧪 *This suite is part of the AllProjectsSuite by Ved Thakur (BTech ChemEng).*")

