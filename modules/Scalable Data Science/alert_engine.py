# 📦 Module 7: Alert Engine | SensorGuardAI Suite
# 🚨 Triggers real-time alerts on anomaly detection (visual + sound)
# 📦 Author: Ved Thakur | BTech ChemEng | IPS Academy Indore

import streamlit as st

def trigger_alert(fault_df):
    """
    Triggers alerts if any faults are detected in the incoming batch.

    Args:
        fault_df (pd.DataFrame): DataFrame with 'status' and sensor readings
    """
    try:
        fault_count = len(fault_df)
        if fault_count > 0:
            st.error(f"🚨 {fault_count} Fault(s) Detected!")
            st.warning("🔊 Alert: Immediate Inspection Recommended!")

            # Display top 3 fault rows
            st.dataframe(fault_df.head(3), use_container_width=True)

            # Optional sound alert (Streamlit-native workaround)
            st.markdown("""
                <audio autoplay>
                  <source src="https://www.soundjay.com/buttons/sounds/beep-07.mp3" type="audio/mpeg">
                </audio>
            """, unsafe_allow_html=True)

        else:
            st.success("✅ No faults detected in this batch.")

    except Exception as e:
        st.error(f"❌ Alert Engine Error: {e}")


def run():
    """
    Streamlit demo runner for alert engine.
    Feeds a sample fault and shows alerts.
    """
    import pandas as pd

    st.header("🚨 Alert Engine Demo")
    st.markdown("Triggers real-time visual + sound alerts if faults are found.")

    # Sample faulty data
    df = pd.DataFrame({
        "Temperature": [145, 150],
        "Pressure": [31.5, 32.0],
        "FlowRate": [490, 505],
        "status": ["⚠️ Fault", "⚠️ Fault"]
    })

    if st.button("🚨 Trigger Sample Alert"):
        trigger_alert(df)
