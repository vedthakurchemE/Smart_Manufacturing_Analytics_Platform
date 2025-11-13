# 📘 Module 10: Report Generator & Dashboard | EpiModelAI Suite
# 🧾 Export results as PDF or HTML dashboard
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
from io import BytesIO
import base64
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

def run():
    # === Title ===
    st.title("📘 Report Generator & Dashboard")
    st.markdown("Export summary metrics, plots, and analysis as **PDF** or **HTML** dashboards.")

    # === Dashboard Inputs ===
    st.subheader("📊 Summary Inputs")
    title = st.text_input("Report Title", "EpiModelAI Pandemic Report")
    analyst = st.text_input("Prepared By", "Ved Thakur")
    organization = st.text_input("College", "IPS Academy Indore")
    date = datetime.today().strftime('%Y-%m-%d')

    total_cases = st.number_input("Total Cases", value=10450)
    peak_infected = st.number_input("Peak Infected", value=870)
    total_recovered = st.number_input("Total Recovered", value=9000)
    vaccinated = st.number_input("Total Vaccinated", value=2000)

    # === Sample Chart ===
    st.subheader("📈 Chart Preview")
    days = list(range(10))
    cases = [100, 250, 500, 700, 870, 800, 650, 400, 200, 100]
    fig, ax = plt.subplots()
    ax.plot(days, cases, marker='o', color='crimson')
    ax.set_title("📉 Sample Infections Over Time")
    ax.set_xlabel("Day")
    ax.set_ylabel("Infected Count")
    st.pyplot(fig)

    # === Report Template ===
    html = f"""
    <html>
    <head><style>
    body {{ font-family: Arial; padding: 20px; }}
    h1 {{ color: #C0392B; }}
    .metrics {{ margin-top: 20px; }}
    .metrics table {{ border-collapse: collapse; width: 100%; }}
    .metrics th, .metrics td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
    </style></head>
    <body>
    <h1>{title}</h1>
    <p><b>Date:</b> {date}<br>
    <b>Prepared by:</b> {analyst}<br>
    <b>Organization:</b> {organization}</p>

    <div class="metrics">
    <h2>📊 Summary Metrics</h2>
    <table>
        <tr><th>Total Cases</th><th>Peak Infected</th><th>Total Recovered</th><th>Vaccinated</th></tr>
        <tr><td>{total_cases}</td><td>{peak_infected}</td><td>{total_recovered}</td><td>{vaccinated}</td></tr>
    </table>
    </div>
    <p><i>Generated using EpiModelAI Suite | Developed by Ved Thakur</i></p>
    </body></html>
    """

    # === Download as HTML ===
    st.subheader("💾 Export Report")
    b64 = base64.b64encode(html.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="epimodelai_report.html">📥 Download Report (HTML)</a>'
    st.markdown(href, unsafe_allow_html=True)

    st.markdown("---")
    with st.expander("📘 Notes"):
        st.markdown("""
        - This module builds a full HTML dashboard.
        - It exports metrics + charts into a report.
        - You can extend this to PDF using libraries like `pdfkit` or `weasyprint`.
        """)
