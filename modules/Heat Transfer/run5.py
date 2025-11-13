# 📘 run.py - Heat Transfer AI Suite | AllProjectsSuite
# 🔥 Simulate conduction, convection, radiation, and transient heat flow
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st

# Import all modules (each has a run() function)
from module1_conduction import run as run_conduction
from module2_convection import run as run_convection
from module3_radiation import run as run_radiation
from module4_transient_conduction import run as run_transient
from module5_overall_htc import run as run_overall
from module6_heat_exchanger import run as run_exchanger
from module7_finned_surface import run as run_fins
from module8_insulation_optimizer import run as run_insulation
from module9_htc_estimator import run as run_htc
from module10_heat_loss_analyzer import run as run_loss

def run():
    # === Page Config ===
    st.set_page_config(page_title="🔥 Heat Transfer AI Suite", layout="wide")

    # === App Title ===
    st.title("🔥 Heat Transfer AI Suite")
    st.markdown("""
    A powerful suite of **10 heat transfer tools** to solve and visualize real-world engineering problems.

    💻 Built using Python + Streamlit  
    📦 Module of: **AllProjectsSuite**  
    👨‍💻 Author: **Ved Thakur**  
    🏫 IPS Academy Indore | BTech Chemical Engineering  
    ---
    """)

    # === Module Selection Menu ===
    tool = st.selectbox("📚 Select a Module", [
        "1️⃣ Steady-State Conduction",
        "2️⃣ Convective Heat Transfer",
        "3️⃣ Radiative Heat Transfer",
        "4️⃣ Transient Conduction (1D)",
        "5️⃣ Overall Heat Transfer Coefficient",
        "6️⃣ Heat Exchanger Design (LMTD/NTU)",
        "7️⃣ Finned Surface Efficiency",
        "8️⃣ Insulation Thickness Optimizer",
        "9️⃣ Heat Transfer Coefficient Estimator",
        "🔟 Heat Loss Analyzer"
    ])

    # === Routing Logic ===
    if tool.startswith("1"):
        run_conduction()
    elif tool.startswith("2"):
        run_convection()
    elif tool.startswith("3"):
        run_radiation()
    elif tool.startswith("4"):
        run_transient()
    elif tool.startswith("5"):
        run_overall()
    elif tool.startswith("6"):
        run_exchanger()
    elif tool.startswith("7"):
        run_fins()
    elif tool.startswith("8"):
        run_insulation()
    elif tool.startswith("9"):
        run_htc()
    elif tool.startswith("🔟") or tool.startswith("10"):
        run_loss()

    # === Footer ===
    st.markdown("---")
    st.markdown("🔥 *This heat transfer suite is part of the AllProjectsSuite by Ved Thakur.*")
