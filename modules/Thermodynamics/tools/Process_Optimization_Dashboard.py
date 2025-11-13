# 🔧 Process Optimization Dashboard (Streamlit + Real-Time Suggestions + UX Enhancements)
# 📦 Part of the PetroStream AI Suite
# 👨‍💻 Author: Ved Thakur (Improved)

import streamlit as st

# ===== Constants =====
OPTIMIZATION_TIPS = {
    "Temperature (°C)": [
        "Maintain within optimal range for catalyst activity.",
        "Avoid overheating to prevent side reactions."
    ],
    "Pressure (bar)": [
        "Optimize to balance reaction rate and equipment safety.",
        "Lower pressure can reduce energy consumption."
    ],
    "Flow Rate (m³/h)": [
        "Ensure uniform flow distribution.",
        "Avoid flow surges to maintain steady-state."
    ],
    "Catalyst Loading (kg)": [
        "Use optimal catalyst amount to maximize yield.",
        "Avoid excess catalyst to reduce costs."
    ]
}

# ===== Core Logic =====
def evaluate_parameters(params):
    """
    Evaluate process parameters against heuristic rules
    and return a list of optimization suggestions.
    """
    suggestions = []

    temp = params["Temperature (°C)"]
    if temp < 150:
        suggestions.append("Increase temperature to improve reaction rate.")
    elif temp > 250:
        suggestions.append("Decrease temperature to avoid catalyst deactivation.")

    pressure = params["Pressure (bar)"]
    if pressure < 1:
        suggestions.append("Increase pressure for better conversion.")
    elif pressure > 5:
        suggestions.append("Reduce pressure to save energy.")

    flow = params["Flow Rate (m³/h)"]
    if flow < 10:
        suggestions.append("Increase flow rate to enhance throughput.")
    elif flow > 100:
        suggestions.append("Reduce flow rate to maintain control.")

    catalyst = params["Catalyst Loading (kg)"]
    if catalyst < 5:
        suggestions.append("Add more catalyst to improve conversion.")
    elif catalyst > 20:
        suggestions.append("Reduce catalyst loading to lower costs.")

    return suggestions

# ===== UI Helper Functions =====
def display_general_tips():
    st.subheader("📚 General Tips")
    for param, tips in OPTIMIZATION_TIPS.items():
        st.markdown(f"**{param}**")
        for tip in tips:
            st.markdown(f"- {tip}")

def create_reset_button():
    if st.button("🔄 Reset Parameters"):
        st.session_state.clear()
        st.rerun()

# ===== Main App =====
def process_optimization_dashboard():
    st.set_page_config(page_title="🔧 Process Optimization Dashboard", layout="centered")
    st.title("🔧 Process Optimization Dashboard")
    st.markdown("""
    Input your process parameters to get **real-time optimization suggestions** for improving yield and reducing costs.
    """)

    create_reset_button()

    st.subheader("⚙️ Input Process Parameters")

    # Use columns for compact layout
    col1, col2 = st.columns(2)

    params = {}
    with col1:
        params["Temperature (°C)"] = st.number_input(
            label="Temperature (°C)",
            min_value=0, max_value=500, value=200, step=1,
            help="Optimal range is 150-250°C for catalyst activity."
        )
        params["Pressure (bar)"] = st.number_input(
            label="Pressure (bar)",
            min_value=0.1, max_value=10.0, value=3.0, step=0.1,
            help="Pressure affects reaction rate and energy consumption."
        )
    with col2:
        params["Flow Rate (m³/h)"] = st.number_input(
            label="Flow Rate (m³/h)",
            min_value=1, max_value=200, value=50, step=1,
            help="Maintain steady flow to avoid surges."
        )
        params["Catalyst Loading (kg)"] = st.number_input(
            label="Catalyst Loading (kg)",
            min_value=1, max_value=50, value=10, step=1,
            help="Optimize catalyst quantity to balance cost and yield."
        )

    # Validate inputs (basic check)
    if any(v is None for v in params.values()):
        st.warning("⚠️ Please fill all parameter inputs.")
        return

    # Generate suggestions
    suggestions = evaluate_parameters(params)

    st.subheader("💡 Optimization Suggestions")
    if suggestions:
        for suggestion in suggestions:
            st.info(f"⚠️ {suggestion}")
    else:
        st.success("✅ All parameters are within optimal ranges!")

    st.markdown("---")
    display_general_tips()

    # Download suggestions as text file
    if suggestions:
        suggestions_text = "\n".join(suggestions)
        st.download_button(
            label="📥 Download Suggestions",
            data=suggestions_text,
            file_name="optimization_suggestions.txt",
            mime="text/plain"
        )

# ===== Entry Point for Suite Integration =====
def run():
    process_optimization_dashboard()
