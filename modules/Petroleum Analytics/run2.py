# 📘 run.py - Petroleum Analytics AI Suite | AllProjectsSuite
# 🛢️ Unified dashboard for 11 petroleum tools
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st

# === Import your tools ===
from Catalyst_Life_Cycle_Analyzer import run as run_catalyst
from Combustion_Analyzer_for_Refinery_Furnaces import run as run_combustion
from Crude_Oil_Blend_Optimizer import run as run_blend
from Energy_Loss_Visualizer_in_Heat_Exchangers import run as run_loss
from Petroleum_Inventory_Forecasting import run as run_inventory
from Petroleum_Lab_Data_Auto_Analyzer import run as run_lab
from Petroleum_Supply_Chain_Optimizer import run as run_supply
from Pump_and_Compressor_Fault_Detection_System import run as run_faults
from Real_Time_Emission_Estimator import run as run_emission
from Refinery_Product_Yield_Predictor import run as run_yield
from app5 import run as run_dashboard  # assuming this is a common dashboard

def run():
    st.set_page_config(page_title="🛢️ Petroleum Analytics Suite", layout="wide")
    st.title("🛢️ Petroleum Analytics AI Suite")
    st.markdown("""
    A comprehensive suite of **11 petroleum tools** built with Python + Streamlit to analyze, predict, and optimize real-world refinery operations.

    🧪 Built by: **Ved Thakur**  
    🏫 IPS Academy Indore | BTech Chemical Engineering  
    📦 Part of: **AllProjectsSuite**
    ---
    """)

    # === Module Selector ===
    tool = st.selectbox("🧰 Select a Petroleum Tool", [
        "1️⃣ Catalyst Life Cycle Analyzer",
        "2️⃣ Combustion Analyzer for Refinery Furnaces",
        "3️⃣ Crude Oil Blend Optimizer",
        "4️⃣ Energy Loss Visualizer in Heat Exchangers",
        "5️⃣ Petroleum Inventory Forecasting",
        "6️⃣ Petroleum Lab Data Auto-Analyzer",
        "7️⃣ Petroleum Supply Chain Optimizer",
        "8️⃣ Pump & Compressor Fault Detection System",
        "9️⃣ Real-Time Emission Estimator",
        "🔟 Refinery Product Yield Predictor",
        "🧠 Summary Dashboard (app5)"
    ])

    # === Routing Logic ===
    if tool.startswith("1"):
        run_catalyst()
    elif tool.startswith("2"):
        run_combustion()
    elif tool.startswith("3"):
        run_blend()
    elif tool.startswith("4"):
        run_loss()
    elif tool.startswith("5"):
        run_inventory()
    elif tool.startswith("6"):
        run_lab()
    elif tool.startswith("7"):
        run_supply()
    elif tool.startswith("8"):
        run_faults()
    elif tool.startswith("9"):
        run_emission()
    elif tool.startswith("🔟") or tool.startswith("10"):
        run_yield()
    elif "Dashboard" in tool:
        run_dashboard()

    # === Footer ===
    st.markdown("---")
    st.markdown("🛢️ *This unified petroleum analytics app is part of the AllProjectsSuite by Ved Thakur.*")
