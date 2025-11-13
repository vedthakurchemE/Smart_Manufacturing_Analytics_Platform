# ⚡ Energy Efficiency Analyzer (Streamlit + Calculations + Feedback + Report Export)
# 📦 Part of the PetroStream AI Suite
# 👨‍💻 Author: Ved Thakur

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF
import base64
import io

# ===== Efficiency Tips =====
EFFICIENCY_TIPS = {
    "low": [
        "🔄 Recover waste heat using heat exchangers.",
        "🛠️ Maintain equipment to reduce losses.",
        "⚙️ Upgrade to high-efficiency motors."
    ],
    "medium": [
        "📊 Implement energy monitoring systems.",
        "🌡️ Improve insulation in pipelines and vessels."
    ],
    "high": [
        "✅ Keep up the good work! Maintain current efficiency.",
        "📈 Perform periodic audits to stay efficient."
    ]
}

# ===== Utility Functions =====
def calculate_efficiency(input_energy, output_energy):
    efficiency = (output_energy / input_energy) * 100
    loss = 100 - efficiency
    return efficiency, loss

def generate_pdf_report(input_energy, output_energy, efficiency, loss):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="⚡ Energy Efficiency Report", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Total Energy Input: {input_energy} MJ", ln=True)
    pdf.cell(200, 10, txt=f"Useful Energy Output: {output_energy} MJ", ln=True)
    pdf.cell(200, 10, txt=f"Efficiency: {efficiency:.2f}%", ln=True)
    pdf.cell(200, 10, txt=f"Energy Loss: {loss:.2f}%", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Suggested Improvements:", ln=True)
    tips = get_efficiency_tips(efficiency)
    for tip in tips:
        pdf.cell(200, 10, txt=f"- {tip}", ln=True)

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    return pdf_output.getvalue()

def get_efficiency_tips(efficiency):
    if efficiency < 50:
        return EFFICIENCY_TIPS["low"]
    elif efficiency < 80:
        return EFFICIENCY_TIPS["medium"]
    else:
        return EFFICIENCY_TIPS["high"]

# ===== Main App =====
def energy_efficiency_analyzer():
    st.set_page_config(page_title="⚡ Energy Efficiency Analyzer", layout="centered")
    st.title("⚡ Energy Efficiency Analyzer")
    st.markdown("Analyze your energy usage and identify improvement areas.")

    with st.expander("ℹ️ About this tool"):
        st.info("""
        Input the total energy input and useful energy output to calculate energy efficiency.
        Based on your values, suggestions and visualizations will be provided.
        """)

    st.subheader("📥 Enter Energy Details")
    energy_input = st.number_input("🔌 Total Energy Input (MJ)", min_value=0.0, step=0.1)
    energy_output = st.number_input("⚙️ Useful Energy Output (MJ)", min_value=0.0, step=0.1)

    if energy_input > 0:
        if energy_output <= energy_input:
            efficiency, loss = calculate_efficiency(energy_input, energy_output)
            st.success(f"✅ System Efficiency: **{efficiency:.2f}%**")
            st.info(f"♻️ Energy Loss: **{loss:.2f}%**")

            # Pie Chart
            st.subheader("📊 Energy Distribution")
            fig, ax = plt.subplots()
            ax.pie([energy_output, energy_input - energy_output],
                   labels=["Useful Output", "Losses"],
                   colors=["#4CAF50", "#FF5722"],
                   autopct="%1.1f%%",
                   startangle=90,
                   wedgeprops={'edgecolor': 'black'})
            ax.axis('equal')
            st.pyplot(fig)

            # Tips
            st.subheader("💡 Efficiency Improvement Tips")
            for tip in get_efficiency_tips(efficiency):
                st.markdown(f"- {tip}")

            # Report Export
            if st.button("📄 Download Efficiency Report as PDF"):
                pdf_bytes = generate_pdf_report(energy_input, energy_output, efficiency, loss)
                b64 = base64.b64encode(pdf_bytes).decode()
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="efficiency_report.pdf">📥 Download Report</a>'
                st.markdown(href, unsafe_allow_html=True)
        else:
            st.error("⚠️ Output energy cannot exceed input energy.")
    elif energy_input == 0:
        st.warning("⚠️ Please enter a total energy input greater than 0.")

# Run App
def run():
    energy_efficiency_analyzer()
