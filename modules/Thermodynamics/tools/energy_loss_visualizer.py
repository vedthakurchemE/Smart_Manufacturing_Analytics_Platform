# 🔥 Energy Loss Visualizer (Streamlit + Plotly + Matplotlib)
# 📦 Part of the PetroStream AI Suite
# 👨‍💻 Author: Ved Thakur (Improved by ChatGPT)

import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from io import BytesIO
from datetime import datetime

# ===== Constants =====
DEFAULT_UNITS = {
    "Heater": 18,
    "Reactor": 25,
    "Distillation Column": 30,
    "Pump": 10,
    "Compressor": 12,
    "Piping and Friction Losses": 5
}

EFFICIENCY_TIPS = {
    "Heater": "🔧 Insulate and use heat recovery systems.",
    "Reactor": "⚙️ Optimize reaction time and temperature.",
    "Distillation Column": "💡 Use multiple-effect or dividing wall columns.",
    "Pump": "🔄 Use VFDs, proper sizing, and regular maintenance.",
    "Compressor": "⚙️ Check for leaks and optimize staging.",
    "Piping and Friction Losses": "🛠️ Improve layout and reduce flow resistance."
}

# ===== Utility Functions =====
def get_download_button(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    st.download_button(
        label="📥 Download Pie Chart (PNG)",
        data=buf.getvalue(),
        file_name=f"energy_loss_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
        mime="image/png"
    )

def reset_sliders():
    st.session_state.clear()
    st.rerun()

# ===== Main App =====
def energy_loss_visualizer():
    st.set_page_config(page_title="Energy Loss Visualizer", layout="centered")
    st.title("♻️ Energy Loss Visualizer")
    st.markdown("Analyze and visualize energy losses in petroleum processing units.\n\nAdjust loss values and get efficiency tips.")

    with st.expander("🔧 Reset All Values", expanded=False):
        if st.button("🔄 Reset to Default", use_container_width=True):
            reset_sliders()

    st.divider()
    st.subheader("⚙️ Customize Energy Loss (%) for Each Unit")

    user_inputs = {
        unit: st.slider(f"{unit}", min_value=0, max_value=100, value=DEFAULT_UNITS.get(unit, 10), key=unit)
        for unit in DEFAULT_UNITS
    }

    filtered_units = {k: v for k, v in user_inputs.items() if v > 0}
    total_loss = sum(filtered_units.values())

    if filtered_units:
        df = pd.DataFrame({"Unit": list(filtered_units.keys()), "Loss (%)": list(filtered_units.values())})

        # Pie Chart
        st.subheader("📈 Energy Loss Distribution")
        fig, ax = plt.subplots()
        ax.pie(df["Loss (%)"], labels=df["Unit"], autopct='%1.1f%%', startangle=140)
        ax.axis("equal")
        st.pyplot(fig)
        get_download_button(fig)

        # Bar Chart
        st.subheader("📊 Interactive Bar Chart")
        bar_fig = px.bar(df, x="Unit", y="Loss (%)", color="Unit", text="Loss (%)", title="Energy Loss by Unit")
        bar_fig.update_traces(textposition='outside')
        bar_fig.update_layout(xaxis_title="Unit", yaxis_title="Loss (%)", showlegend=False)
        st.plotly_chart(bar_fig, use_container_width=True)

        # Efficiency Tips
        st.subheader("🧠 Efficiency Suggestions")
        for unit in filtered_units:
            st.info(f"**{unit}**: {EFFICIENCY_TIPS.get(unit)}")

        if total_loss > 100:
            st.error(f"❗ Total loss exceeds 100% ({total_loss}%). Consider reducing some values.")
        else:
            st.success(f"✅ **Total Loss across units: {total_loss}%**")
    else:
        st.warning("⚠️ Please select at least one unit with loss greater than 0%.")

def run():
    energy_loss_visualizer()