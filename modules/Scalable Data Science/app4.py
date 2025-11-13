# ⚙️ Scalable Data Science Suite | app4.py
# 🚀 Dynamic Launcher for Scalable Python Modules
# 👨‍🔬 Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import os
import sys

def run():
    # ✅ Add current folder to Python path
    folder = os.path.dirname(__file__)
    sys.path.append(folder)

    # === Streamlit Page Config ===
    st.set_page_config(page_title="⚙️ Scalable Data Science Suite", layout="centered")

    st.title("⚙️ Scalable Data Science Suite")
    st.markdown("🧠 Real-Time | Stream | IoT | Anomaly Detection | Automation Tools.")
    st.markdown("🚀 Select any module below to begin.")

    # === Sidebar Module List ===
    st.sidebar.title("📂 Modules")

    modules = {
        "1️⃣ Alert Engine": "alert_engine",
        "2️⃣ Anomaly Detector": "anomaly_detector",
        "3️⃣ Dashboard View": "dashboard_view",
        "4️⃣ Data Processor": "data_processor",
        "5️⃣ IoT Webhook Sync": "iot_webhook_sync",
        "6️⃣ Logger Module": "logger_module",
        "7️⃣ Notification Bot": "notification_bot",
        "8️⃣ Report Generator": "report_generator1",
        "9️⃣ Stream Simulator": "stream_simulator"
    }

    selected = st.sidebar.radio("🧭 Select Tool", list(modules.keys()))
    filename = modules[selected] + ".py"
    filepath = os.path.join(folder, filename)

    # === Dynamic Load + Execute ===
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        exec(code, globals())
        run()  # ⚠️ Each module file must have def run()
    except FileNotFoundError:
        st.error(f"❌ File not found: `{filename}`")
    except Exception as e:
        st.error(f"❌ Error in `{filename}`:\n\n`{e}`")

    # === Footer ===
    st.markdown("---")
    st.caption("👨‍💻 Built by Ved Thakur | BTech ChemEng | IPS Academy Indore")
