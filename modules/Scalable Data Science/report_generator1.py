# 📦 Module 5: Report Generator | SensorGuardAI Suite
# 📤 Export sensor fault results to Excel for offline reporting
# 📦 Author: Ved Thakur | BTech ChemEng | IPS Academy Indore

import pandas as pd
import streamlit as st
from io import BytesIO

def export_report(df, filename="sensor_fault_report.xlsx"):
    """
    Exports DataFrame to Excel file and returns downloadable buffer.

    Args:
        df (pd.DataFrame): Final DataFrame with sensor data and anomaly labels.
        filename (str): Desired name of the Excel file.

    Returns:
        BytesIO: In-memory Excel file buffer for Streamlit download.
    """
    try:
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="FaultReport")
            writer.close()
        st.success(f"✅ Report prepared: `{filename}`")
        return buffer

    except Exception as e:
        st.error(f"❌ Report Generation Error: {e}")
        return None


def run():
    """
    Streamlit test runner for the report generator module.
    Creates sample output and offers download.
    """
    st.header("📤 Report Generator Demo")
    st.markdown("Download a full Excel report of processed + labeled sensor data.")

    # Sample Data
    sample_df = pd.DataFrame({
        "Temperature": [75, 140, 73, 76],
        "Pressure": [10.2, 30.1, 10.0, 10.5],
        "FlowRate": [300, 500, 302, 295],
        "Temp_scaled": [-0.36, 1.91, -0.48, -0.22],
        "Press_scaled": [-0.45, 2.0, -0.51, -0.41],
        "Flow_scaled": [-0.29, 1.99, -0.16, -0.54],
        "anomaly": [1, -1, 1, 1],
        "status": ["✅ Normal", "⚠️ Fault", "✅ Normal", "✅ Normal"]
    })

    if st.button("📥 Generate Report"):
        excel_file = export_report(sample_df)
        if excel_file:
            st.download_button(
                label="📄 Download Excel Report",
                data=excel_file,
                file_name="SensorFaultReport.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
