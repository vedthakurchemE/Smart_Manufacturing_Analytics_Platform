# 📦 Module 9: IoT Webhook Sync | SensorGuardAI Suite
# 🌐 Sends real-time sensor data or anomalies to a webhook (e.g. Firebase, Node-RED, Webhook.site)
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import requests
import streamlit as st

# === Replace with your actual webhook ===
# Get one free from https://webhook.site
WEBHOOK_URL = "https://webhook.site/25eb76c2-41c1-4964-b55a-db2fb9657e95"  # 🔁 Replace with your own live URL

def sync_to_webhook(data_dict):
    """
    Send one row (as dictionary) to an external webhook or IoT cloud endpoint.

    Args:
        data_dict (dict): A single sensor reading + status row.
    """
    try:
        headers = {"Content-Type": "application/json"}

        st.code(f"Sending to: {WEBHOOK_URL}")
        st.json(data_dict)  # Show the actual payload in Streamlit

        response = requests.post(WEBHOOK_URL, json=data_dict, headers=headers, timeout=10)

        if response.status_code == 200:
            st.success("🌐 Synced to Webhook Successfully!")
        else:
            st.warning(f"⚠️ Webhook Error: {response.status_code} - {response.text}")

    except Exception as e:
        st.error(f"❌ Webhook Sync Error: {e}")


def run():
    """
    Streamlit demo runner to test webhook sync with sample data.
    """
    st.header("🌐 IoT Webhook Sync Tester")
    st.markdown("Send sample sensor data to an external webhook endpoint like Firebase, Node-RED, or webhook.site.")

    sample_dict = {
        "unit_id": "Reactor-2",
        "Temperature": 145.0,
        "Pressure": 31.7,
        "FlowRate": 489.5,
        "status": "⚠️ Fault",
        "log_time": "2025-07-24 11:10:00"
    }

    if st.button("🔁 Send Sample Data"):
        sync_to_webhook(sample_dict)
