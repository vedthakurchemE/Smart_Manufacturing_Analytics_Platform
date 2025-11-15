import streamlit as st
import os
import importlib.util
import sqlite3
import pandas as pd
import time

st.set_page_config(
    page_title="📘 Semester 1 – Engineering Project Suite",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ——— Loading Screen Section ———
# This block runs before your main dashboard

if "loaded" not in st.session_state:
    st.title("📁 Project is loading...")
    st.caption("Loading main project, please wait...")

    with st.spinner("🔄 Initializing Dashboard..."):
        progress_bar = st.progress(0)
        loading_text = st.empty()
        for percent_complete in range(100):
            progress_bar.progress(percent_complete + 1)
            loading_text.text(f"Loading... {percent_complete + 1}%")
            time.sleep(0.02)  # Simulate loading time

    loading_text.empty()
    st.success("✅ Project Loaded!")
    st.session_state["loaded"] = True
    st.rerun()      # reload and show actual dashboard
    # 🧑‍🔬 Advanced Process & Data Science Suite

# ==== DESCRIPTION SCREEN ====
if "description_done" not in st.session_state:
    st.session_state["description_done"] = False

if not st.session_state["description_done"]:
    st.markdown("""
    # 🧑‍🔬 Advanced Process & Data Science Suite

    Welcome to the **Process Engineering and Petroleum Analytics Platform** – a state-of-the-art dashboard uniting key domains of modern engineering and data science.

    Built for deep exploration and innovation, this suite empowers users with interactive tools for:

    - 🌡️ **Mass & Heat Transfer** – Simulate and analyze real process systems, from heat exchangers to chemical reactors
    - 🔢 **Mathematical Modeling** – Develop, visualize and solve mathematical models for dynamic and steady-state engineering problems
    - 🛢️ **Petroleum Analysis** – Unlock critical insights from composition, thermodynamic properties, and process optimization in energy systems
    - 🧮 **Thermodynamics Simulations** – Visualize cycles and processes, calculate efficiencies, track energy balances across diverse scenarios
    - ⚖️ **Scalable Data Science** – Apply advanced analytic techniques to large-scale engineering data, automate reporting, and uncover trends for research and industry

    ---

    ### 🌟 Key Features

    - **Interactive Visualization:** Seamless plotting and analysis of process variables, system responses, and engineering datasets.
    - **Modular Toolkits:** Each module is designed for specialized computations—mass balances, energy analysis, predictive modeling, and more.
    - **Data-Driven Process Engineering:** Integrate real and simulated plant/lab data, perform multivariate analysis, optimize workflows, and validate models.
    - **Professional & Educational Utility:** Suitable for students mastering chemical engineering concepts and professionals pushing boundaries in R&D, production, and analytics.
    - **Scalable and Extensible:** Future-ready architecture enables integration of new models, workflows, and IoT/plant data for smart manufacturing.

    ---

    ### 🚀 Why This Platform?

    By merging deep engineering principles with powerful analytics, this platform helps you master fundamental concepts and drive practical innovations in process and energy industries.

    Empower your workflow. **Analyze, discover, and innovate — from thermodynamics to data science.**
    """)
    if st.button("Next"):
        st.session_state["description_done"] = True
        st.rerun()
    st.stop()

# ——— Main Dashboard Section ———
# Existing code for navigation, modules, DB viewer, etc. comes after this.
st.title("📘 Semester 1 – Engineering Project Suite")
st.caption("🔁 Centralized Dashboard for All 12 Labs & Project Suites")

# === Database Setup ===
def init_db():
    conn = sqlite3.connect("project_data.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT,
            parameter TEXT,
            value TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            filetype TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_results_to_db(project_name, results: dict):
    conn = sqlite3.connect("project_data.db")
    c = conn.cursor()
    for param, value in results.items():
        c.execute("INSERT INTO results (project_name, parameter, value) VALUES (?, ?, ?)",
                  (project_name, str(param), str(value)))
    conn.commit()
    conn.close()

def save_upload_to_db(filename, filetype):
    conn = sqlite3.connect("project_data.db")
    c = conn.cursor()
    c.execute("INSERT INTO uploads (filename, filetype) VALUES (?, ?)", (filename, filetype))
    conn.commit()
    conn.close()

init_db()

# === Function to Dynamically Import run() from Any File ===
def import_run_function(path_to_file):
    try:
        if not os.path.isfile(path_to_file):
            st.error(f"❌ File not found:\n`{path_to_file}`")
            return lambda: {}

        spec = importlib.util.spec_from_file_location("module.name", path_to_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "run"):
            return module.run
        else:
            return lambda: {}
    except:
        return lambda: {}

# === Base Directory ===
base_dir = os.path.dirname(os.path.abspath(__file__))

# === Full Project Mapping ===
projects = {
    "💧 Mass Transfer Suite": os.path.join(base_dir, "modules", "Mass Transfer", "app1.py"),
    "🔥 Heat Transfer Suite": os.path.join(base_dir, "modules", "Heat Transfer", "app2.py"),
    "📕 Mathematics Modelling Suite": os.path.join(base_dir, "modules", "Mathematics Modelling", "app3.py"),
    "📊 Scalable Data Science Suite": os.path.join(base_dir, "modules", "Scalable Data Science", "app4.py"),
    "🛢️ Petroleum Analytics Suite": os.path.join(base_dir, "modules", "Petroleum Analytics", "app5.py"),
    "🌡️ Thermodynamics Suite": os.path.join(base_dir, "modules", "Thermodynamics", "app6.py")
}

# === Sidebar for Project Selection ===
st.sidebar.title("📚 Semester 1 Project Suite")
choice = st.sidebar.radio("🔍 Select a Major Project", list(projects.keys()))

# ✅ Reset Button
if st.sidebar.button("🔄 Reset App"):
    st.session_state.clear()
    st.rerun()

# === Run Selected Project ===
selected_path = projects.get(choice)
run_func = import_run_function(selected_path)
results = run_func()

# === File Upload Section (Sidebar) ===
st.sidebar.markdown("---")
st.sidebar.header("📤 Upload Your Files")
uploaded_file = st.sidebar.file_uploader("Upload CSV, Excel, or PDF", type=["csv", "xlsx", "xls", "pdf"])

if uploaded_file:
    save_upload_to_db(uploaded_file.name, uploaded_file.type)
    st.success(f"✅ Uploaded {uploaded_file.name} successfully!")

    if uploaded_file.type in ["text/csv", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.dataframe(df)

            # Append uploaded data into DB results
            for col in df.columns:
                for val in df[col]:
                    save_results_to_db("Uploaded File", {col: val})

        except Exception as e:
            st.error(f"❌ Error reading file: {e}")

# === Display Results Only If Present ===
if isinstance(results, dict) and results:
    st.subheader("📌 Module Results")
    save_results_to_db(choice, results)
    for key, value in results.items():
        st.markdown(f"- **{key}:** {value}")

# ---- Feedback Section ----
import datetime

st.markdown("---")
st.subheader("💬 Feedback")
feedback = st.text_area("Your feedback, suggestions, or improvement ideas:", key="feedback_text")
if st.button("Submit Feedback"):
    if "feedback_list" not in st.session_state:
        st.session_state["feedback_list"] = []
    st.session_state["feedback_list"].append({
        "text": feedback,
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    st.success("Thank you for your feedback!")

# Display feedback history (optional, only current session)
if "feedback_list" in st.session_state and st.session_state["feedback_list"]:
    st.markdown("#### Recent Feedback (this session):")
    for item in st.session_state["feedback_list"][-5:][::-1]:
        st.write(f"🕒 {item['time']} \n- {item['text']}")

