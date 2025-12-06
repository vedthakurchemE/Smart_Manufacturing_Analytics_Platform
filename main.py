import streamlit as st
import importlib
import traceback
import sys
import os
import pandas as pd
import sqlite3
import io
import contextlib
from PIL import Image
import matplotlib.pyplot as plt
import time
import inspect
import datetime

# Try to import reportlab, but make it optional
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter

    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False
    st.warning("⚠️ reportlab not installed. PDF export will be disabled. Install with: `pip install reportlab`")

# ===================================
# APP CONFIGURATION
# ===================================
st.set_page_config(
    page_title="📘 Portfolio Hub",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================================
# CUSTOM CSS STYLING
# ===================================
st.markdown("""
<style>
    :root {
        --primary-color: #2E86AB;
        --secondary-color: #A23B72;
        --accent-color: #F18F01;
        --bg-light: #f0f2f6;
    }

    .stButton > button {
        width: 100%;
        border-radius: 8px;
        padding: 0.75rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }

    .project-card {
        background: var(--bg-light);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid var(--primary-color);
    }

    h1 { color: var(--primary-color); font-weight: 700; }
    h2, h3 { color: var(--secondary-color); font-weight: 600; }

    .stats-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }

    .footer {
        background: var(--bg-light);
        padding: 2rem;
        border-radius: 10px;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# ===================================
# PROJECT METADATA CONFIGURATION
# ===================================
PROJECT_METADATA = {
    "🔥 Heat Transfer": {
        "tagline": "Heat transfer analysis and calculations",
        "problem": "Complex heat transfer calculations were time-consuming",
        "solution": "Automated heat transfer analysis tools",
        "tech": ["Python", "NumPy", "Matplotlib", "SciPy"],
        "outcome": "Reduced analysis time by 70%",
        "role": "Lead Developer",
        "users": "Engineering students"
    },
    "💧 Mass Transfer": {
        "tagline": "Mass transfer operations simulator",
        "problem": "Manual mass transfer calculations prone to errors",
        "solution": "Interactive mass transfer computation suite",
        "tech": ["Python", "Pandas", "NumPy", "Streamlit"],
        "outcome": "Improved calculation accuracy to 99%",
        "role": "Process Engineer",
        "users": "Chemical engineering students"
    },
    "📐 Mathematics Modelling": {
        "tagline": "Advanced mathematical modeling toolkit",
        "problem": "Complex mathematical models difficult to visualize",
        "solution": "Interactive modeling and visualization platform",
        "tech": ["Python", "SymPy", "NumPy", "Matplotlib"],
        "outcome": "Enhanced understanding of complex systems",
        "role": "Algorithm Developer",
        "users": "Engineering & Math students"
    },
    "🛢️ Petroleum Analytics": {
        "tagline": "Petroleum data analysis and insights",
        "problem": "Petroleum data analysis required specialized tools",
        "solution": "Comprehensive petroleum analytics dashboard",
        "tech": ["Python", "Pandas", "Plotly", "ML"],
        "outcome": "Streamlined petroleum data workflows",
        "role": "Data Analyst",
        "users": "Petroleum engineers"
    },
    "📊 Scalable Data Science": {
        "tagline": "Large-scale data science platform",
        "problem": "Processing large datasets was inefficient",
        "solution": "Scalable analytics with advanced visualizations",
        "tech": ["Python", "Pandas", "NumPy", "Plotly", "ML"],
        "outcome": "10x faster data processing",
        "role": "Data Scientist",
        "users": "Data science professionals"
    },
    "🌡️ Thermodynamics": {
        "tagline": "Thermodynamic analysis and simulations",
        "problem": "Thermodynamic cycle analysis was complex",
        "solution": "Interactive thermodynamic calculator suite",
        "tech": ["Python", "SciPy", "Matplotlib", "Thermodynamics"],
        "outcome": "Simplified complex calculations",
        "role": "Thermal Engineer",
        "users": "Mechanical engineering students"
    }
}

# ===================================
# PATH CONFIGURATION
# ===================================
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# ===================================
# DATABASE SETUP
# ===================================
DB_FILE = os.path.join(PROJECT_ROOT, "portfolio_data.db")


@st.cache_resource
def get_db_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)


def init_db():
    """Initialize database tables"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Results table
    c.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project TEXT,
            parameter TEXT,
            value TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Analytics table
    c.execute("""
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            session_id TEXT
        )
    """)

    # Feedback table
    c.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tool TEXT,
            feedback_text TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Uploads table
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


def save_results_to_db(project, results: dict, input_data: dict = None):
    """Save project results to database"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    for param, value in results.items():
        c.execute(
            "INSERT INTO results (project, parameter, value) VALUES (?, ?, ?)",
            (project, str(param), str(value))
        )

    if input_data:
        for param, value in input_data.items():
            c.execute(
                "INSERT INTO results (project, parameter, value) VALUES (?, ?, ?)",
                (project, f"Input: {param}", str(value))
            )

    conn.commit()
    conn.close()


def log_project_access(project_name):
    """Log project access for analytics"""
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "INSERT INTO analytics (project, session_id) VALUES (?, ?)",
        (project_name, st.session_state['session_id'])
    )
    conn.commit()
    conn.close()


def get_most_accessed_projects(limit=3):
    """Get most popular projects"""
    conn = sqlite3.connect(DB_FILE)
    query = """
        SELECT project, COUNT(*) as access_count 
        FROM analytics 
        GROUP BY project 
        ORDER BY access_count DESC 
        LIMIT ?
    """
    df = pd.read_sql_query(query, conn, params=(limit,))
    conn.close()
    return df['project'].tolist() if not df.empty else []


def load_results_from_db(project=None):
    """Load results from database"""
    conn = sqlite3.connect(DB_FILE)
    if project:
        df = pd.read_sql_query(
            "SELECT parameter, value FROM results WHERE project = ?",
            conn, params=(project,)
        )
    else:
        df = pd.read_sql_query(
            "SELECT project, parameter, value FROM results",
            conn
        )
    conn.close()
    return df


def save_upload_to_db(filename, filetype):
    """Log file uploads"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "INSERT INTO uploads (filename, filetype) VALUES (?, ?)",
        (filename, filetype)
    )
    conn.commit()
    conn.close()


def generate_pdf_report(display_name, results):
    """Generate PDF report (only if reportlab is available)"""
    if not HAS_REPORTLAB:
        return None

    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter
    y = height - 40

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, f"{display_name}")
    c.setFont("Helvetica", 10)
    c.drawString(50, y - 20, f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    y -= 50

    c.setFont("Helvetica", 11)
    for key, value in results.items():
        text = f"{key}: {value}"
        if len(text) > 80:
            text = text[:77] + "..."
        c.drawString(50, y, text)
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 40

    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer


# Initialize database
init_db()

# ===================================
# PROJECT MODULE MAPPING
# ===================================
PROJECT_SUITES = {
    "🔥 Heat Transfer": "modules.Heat Transfer.app2",
    "💧 Mass Transfer": "modules.Mass Transfer.app1",
    "📐 Mathematics Modelling": "modules.Mathematics Modelling.app3",
    "🛢️ Petroleum Analytics": "modules.Petroleum Analytics.app5",
    "📊 Scalable Data Science": "modules.Scalable Data Science.app4",
    "🌡️ Thermodynamics": "modules.Thermodynamics.app6"
}

# ===================================
# LOADING SCREEN
# ===================================
if "loaded" not in st.session_state:
    st.title("📁 Portfolio Loading...")
    st.caption("Initializing Engineering Portfolio Hub...")

    with st.spinner("🔄 Loading Dashboard..."):
        progress_bar = st.progress(0)
        loading_text = st.empty()
        for percent in range(100):
            progress_bar.progress(percent + 1)
            loading_text.text(f"Loading... {percent + 1}%")
            time.sleep(0.015)

    loading_text.empty()
    st.success("✅ Portfolio Loaded Successfully!")
    st.session_state["loaded"] = True
    time.sleep(0.5)
    st.rerun()

# ===================================
# LANDING PAGE
# ===================================
if "description_done" not in st.session_state:
    st.session_state["description_done"] = False

if not st.session_state["description_done"]:
    # Hero Section
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='font-size: 3rem; margin-bottom: 0;'>🎓 Ved Thakur</h1>
        <h2 style='color: #666; font-weight: 400;'>Chemical Engineering Portfolio Hub</h2>
        <p style='font-size: 1.2rem; color: #888;'>IPS Academy</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Stats Overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class='stats-box'>
            <h2 style='margin: 0; color: white; font-size: 2.5rem;'>6</h2>
            <p style='margin: 0; color: white; opacity: 0.95;'>Project Suites</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='stats-box' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);'>
            <h2 style='margin: 0; color: white; font-size: 2.5rem;'>200+</h2>
            <p style='margin: 0; color: white; opacity: 0.95;'>Active Users</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='stats-box' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'>
            <h2 style='margin: 0; color: white; font-size: 2.5rem;'>5000+</h2>
            <p style='margin: 0; color: white; opacity: 0.95;'>Lines of Code</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class='stats-box' style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);'>
            <h2 style='margin: 0; color: white; font-size: 2.5rem;'>75%</h2>
            <p style='margin: 0; color: white; opacity: 0.95;'>Time Saved</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # About Section
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown("""
        ## 🌟 About This Portfolio

        Welcome to my **Smart Manufacturing Analytics Platform** – a comprehensive suite of 6
        integrated engineering tools covering advanced process engineering and data science.

        ### 🎯 Key Features

        **🔥 Heat & Mass Transfer**  
        Advanced simulation tools for thermal and mass transfer operations

        **📐 Mathematical Modeling**  
        Complex system modeling with interactive visualizations

        **🛢️ Petroleum Analytics**  
        Specialized tools for petroleum data analysis

        **📊 Data Science Suite**  
        Scalable analytics for large engineering datasets

        **🌡️ Thermodynamics**  
        Comprehensive thermodynamic cycle analysis

        ### 💡 Built With
        Python • Streamlit • Pandas • NumPy • Matplotlib • SciPy • ML
        """)

    with col_right:
        st.markdown("""
        ## 👨‍💻 About Me

        **Engineering Student**  
        Process & Data Science

        **Focus Areas**
        - Heat & Mass Transfer
        - Mathematical Modeling
        - Petroleum Analytics
        - Data Science
        - Thermodynamics

        **Skills**
        - Python Development
        - Process Simulation
        - Data Analysis
        - ML Engineering
        """)

    st.markdown("---")

    # Quick Start
    with st.expander("📖 Quick Start Guide", expanded=True):
        st.markdown("""
        ### How to Use

        1. **Choose a Project** from the sidebar
        2. **Upload Data** (optional) - CSV, Excel, or images
        3. **Run Analysis** to generate results
        4. **Download Reports** in your preferred format
        5. **Provide Feedback** to help improve

        💡 **Tip:** Use "Run All" to see all projects at once
        """)

    # CTA Buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🚀 Explore Projects", use_container_width=True):
            st.session_state["description_done"] = True
            st.rerun()
    with col2:
        st.link_button("📧 Contact", "mailto:vedthakursa@gmail.com", use_container_width=True)
    with col3:
        st.link_button("💼 LinkedIn", "https://www.linkedin.com/in/ved-thakur-0b79bb36a/", use_container_width=True)

    st.stop()

# ===================================
# MAIN APPLICATION
# ===================================
st.title("📘 Smart Manufacturing Analytics Platform")
st.caption("🔁 Advanced Process Engineering & Data Science Suite")

# ===================================
# SIDEBAR NAVIGATION
# ===================================
st.sidebar.title("📂 Navigation")

# View Mode
view_mode = st.sidebar.radio(
    "View Mode",
    ["🎯 Project Gallery", "⚡ Quick Access", "📊 Database Viewer"],
    index=1
)

st.sidebar.markdown("---")

# Quick Access Mode
if view_mode == "⚡ Quick Access":
    st.sidebar.subheader("Select Project")
    choice = st.sidebar.selectbox("Choose a Project", list(PROJECT_SUITES.keys()))
    run_all = st.sidebar.button("▶️ Run All Projects", use_container_width=True)

    # Popular projects
    st.sidebar.markdown("### 🔥 Most Popular")
    popular = get_most_accessed_projects(limit=3)
    if popular:
        for proj in popular:
            st.sidebar.markdown(f"- {proj}")
    else:
        st.sidebar.caption("No usage data yet")

elif view_mode == "🎯 Project Gallery":
    st.subheader("🎯 Project Gallery")
    st.caption("Explore all projects with detailed information")

    for idx, (project_name, metadata) in enumerate(PROJECT_METADATA.items()):
        with st.expander(f"{project_name}", expanded=False):
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"**{metadata['tagline']}**")
                st.markdown(f"**Problem:** {metadata['problem']}")
                st.markdown(f"**Solution:** {metadata['solution']}")
                st.markdown(f"**Outcome:** {metadata['outcome']}")
                st.markdown(f"**Tech:** {', '.join(metadata['tech'])}")

            with col2:
                st.markdown(f"**Role:** {metadata['role']}")
                st.markdown(f"**Users:** {metadata['users']}")
                if st.button(f"Run {project_name}", key=f"run_{idx}"):
                    choice = project_name
                    st.session_state['selected_project'] = project_name
                    st.rerun()

    choice = None
    run_all = False

else:  # Database Viewer
    st.subheader("📊 Database Viewer")
    df_db = load_results_from_db()

    if not df_db.empty:
        st.dataframe(df_db, use_container_width=True)

        csv_bytes = df_db.to_csv(index=False).encode()
        st.download_button(
            "📥 Download Database",
            data=csv_bytes,
            file_name="portfolio_database.csv",
            mime="text/csv"
        )
    else:
        st.info("No data yet. Run projects to populate database!")

    choice = None
    run_all = False

# Reset button
if st.sidebar.button("🔄 Reset Session", use_container_width=True):
    st.session_state.clear()
    st.rerun()

st.sidebar.markdown("---")

# ===================================
# FILE UPLOAD
# ===================================
st.sidebar.header("📤 Upload Data")
uploaded_file = st.sidebar.file_uploader(
    "Upload CSV, Excel, or Image",
    type=["csv", "xlsx", "png", "jpg", "jpeg"]
)

uploaded_data = None
if uploaded_file:
    save_upload_to_db(uploaded_file.name, uploaded_file.type)
    file_type = uploaded_file.type

    try:
        if file_type == "text/csv":
            uploaded_data = pd.read_csv(uploaded_file)
            st.sidebar.success("✅ CSV loaded")
            with st.sidebar.expander("Preview"):
                st.write(uploaded_data.head())
        elif "excel" in file_type or ".xlsx" in uploaded_file.name:
            uploaded_data = pd.read_excel(uploaded_file)
            st.sidebar.success("✅ Excel loaded")
            with st.sidebar.expander("Preview"):
                st.write(uploaded_data.head())
        elif "image" in file_type:
            uploaded_data = Image.open(uploaded_file)
            st.sidebar.success("✅ Image loaded")
            st.sidebar.image(uploaded_data, caption="Uploaded Image")
    except Exception as e:
        st.sidebar.error(f"❌ Error: {e}")


# ===================================
# MODULE LOADER
# ===================================
@st.cache_resource
def load_project_module(module_path):
    """Load project module with caching"""
    return importlib.import_module(module_path)


# ===================================
# PROJECT RUNNER
# ===================================
def run_project(display_name, module_path):
    """Execute a project and display results"""
    log_project_access(display_name)

    with st.expander(f"📌 {display_name}", expanded=True):
        # Show metadata
        if display_name in PROJECT_METADATA:
            metadata = PROJECT_METADATA[display_name]
            st.info(f"**{metadata['tagline']}** | {', '.join(metadata['tech'][:3])}")

        try:
            module = load_project_module(module_path)

            if hasattr(module, "run") and callable(module.run):
                st.markdown(f"### ✅ Running {display_name}")

                with st.spinner("🔄 Processing..."):
                    output_buffer = io.StringIO()
                    with contextlib.redirect_stdout(output_buffer):
                        run_params = inspect.signature(module.run).parameters
                        if "uploaded_data" in run_params:
                            result_data = module.run(uploaded_data=uploaded_data)
                        else:
                            result_data = module.run()

                printed_output = output_buffer.getvalue().strip()
                input_data, results, graphs = {}, {}, []

                # Parse results
                if isinstance(result_data, tuple):
                    if len(result_data) == 2:
                        input_data, results = result_data
                    elif len(result_data) == 3:
                        input_data, results, graphs = result_data
                elif isinstance(result_data, dict):
                    results = result_data

                if printed_output:
                    results["Console Output"] = printed_output

                # Save and display results
                if results:
                    if "all_results" not in st.session_state:
                        st.session_state["all_results"] = {}
                    st.session_state["all_results"][display_name] = results
                    save_results_to_db(display_name, results, input_data=input_data)

                    st.markdown("#### 📋 Results")
                    for key, value in results.items():
                        st.markdown(f"- **{key}:** `{value}`")

                # Display graphs
                if graphs:
                    st.markdown("#### 📊 Visualizations")
                    for g in graphs:
                        if isinstance(g, plt.Figure):
                            st.pyplot(g)
                        elif isinstance(g, Image.Image):
                            st.image(g)

                # Download options
                if results:
                    st.markdown("---")

                    # Always show CSV option
                    if HAS_REPORTLAB:
                        col1, col2 = st.columns(2)
                    else:
                        col1 = st.container()
                        col2 = None

                    with col1:
                        df = pd.DataFrame(list(results.items()), columns=["Parameter", "Value"])
                        csv_bytes = df.to_csv(index=False).encode()
                        st.download_button(
                            "📥 Download CSV",
                            data=csv_bytes,
                            file_name=f"{display_name.replace(' ', '_')}_results.csv",
                            mime="text/csv",
                            use_container_width=True
                        )

                    # Only show PDF if reportlab is available
                    if col2 and HAS_REPORTLAB:
                        with col2:
                            pdf_buffer = generate_pdf_report(display_name, results)
                            if pdf_buffer:
                                st.download_button(
                                    "📄 Download PDF",
                                    data=pdf_buffer,
                                    file_name=f"{display_name.replace(' ', '_')}_results.pdf",
                                    mime="application/pdf",
                                    use_container_width=True
                                )
            else:
                st.warning(f"⚠️ No `run()` function in {display_name}")

        except ModuleNotFoundError:
            st.error(f"❌ Module not found: {module_path}")
            st.info("💡 Ensure the module exists in the correct directory")
        except Exception as e:
            st.error(f"❌ Error in {display_name}")
            with st.expander("🔍 Error Details"):
                st.code(traceback.format_exc(), language="python")

        st.markdown("---")


# ===================================
# EXECUTE PROJECTS
# ===================================
if view_mode == "⚡ Quick Access":
    if run_all:
        st.subheader("▶️ Running All Projects")
        for display_name, module_path in PROJECT_SUITES.items():
            run_project(display_name, module_path)
    elif choice:
        run_project(choice, PROJECT_SUITES[choice])

# ===================================
# FEEDBACK SECTION
# ===================================
st.markdown("---")
st.subheader("💬 Share Feedback")

feedback_col1, feedback_col2 = st.columns([3, 1])

with feedback_col1:
    feedback = st.text_area(
        "Your thoughts, suggestions, or issues:",
        placeholder="What worked well? What could be better?",
        height=100
    )

with feedback_col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📤 Submit", use_container_width=True):
        if feedback.strip():
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute(
                "INSERT INTO feedback (tool, feedback_text) VALUES (?, ?)",
                (st.session_state.get('selected_project', 'General'), feedback)
            )
            conn.commit()
            conn.close()
            st.success("✅ Thank you!")
            time.sleep(1)
            st.rerun()
        else:
            st.warning("⚠️ Please enter feedback")

# ===================================
# FOOTER
# ===================================
st.markdown("---")
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 2rem; border-radius: 15px; margin-top: 2rem;'>
    <div style='text-align: center;'>
        <h2 style='color: white; margin-bottom: 0.5rem;'>🤝 Let's Connect</h2>
        <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem;'>
            Questions or collaboration opportunities?
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem; background: #f8f9fa; 
                border-radius: 10px; margin: 1rem 0.5rem;'>
        <h4 style='color: #2E86AB;'>📧 Email</h4>
        <p><a href='mailto:vedthakursa@gmail.com' 
           style='color: #495057; text-decoration: none;'>
           vedthakursa@gmail.com</a></p>
    </div>
    """, unsafe_allow_html=True)

with footer_col2:
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem; background: #f8f9fa; 
                border-radius: 10px; margin: 1rem 0.5rem;'>
        <h4 style='color: #2E86AB;'>💼 LinkedIn</h4>
        <p><a href='https://www.linkedin.com/in/ved-thakur-0b79bb36a/' target='_blank' 
           style='color: #495057; text-decoration: none;'>
           Connect →</a></p>
    </div>
    """, unsafe_allow_html=True)

with footer_col3:
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem; background: #f8f9fa; 
                border-radius: 10px; margin: 1rem 0.5rem;'>
        <h4 style='color: #2E86AB;'>🔗 GitHub</h4>
        <p><a href='https://github.com/vedthakurchemE' target='_blank' 
           style='color: #495057; text-decoration: none;'>
           View Projects →</a></p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style='margin-top: 3rem; padding: 2rem; background: #f8f9fa; 
            border-radius: 10px; text-align: center;'>
    <p style='color: #6c757d; font-size: 14px; font-weight: 500;'>
        Developed by <strong style='color: #2E86AB;'>Ved Thakur</strong>
    </p>
    <p style='color: #adb5bd; font-size: 12px; margin-top: 0.5rem;'>
        Built with Python, Streamlit & Modern Web Technologies
    </p>
</div>
""", unsafe_allow_html=True)