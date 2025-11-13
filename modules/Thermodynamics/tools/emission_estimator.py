# 🌍 Emission Estimator (Streamlit + Calculation + Visualization)
# 📦 Part of the PetroStream AI Suite
# 👨‍💻 Author: Ved Thakur

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ===== Constants =====
@st.cache_data
def get_emission_factors():
    return pd.DataFrame({
        "Energy Source": ["Natural Gas [m³]", "Diesel [litres]", "Gasoline [litres]", "Coal [kg]", "Electricity [kWh]"],
        "Emission Factor (kg CO₂/unit)": [2.75, 2.68, 2.31, 2.42, 0.92]
    })

# ===== Utility Functions =====
def calculate_emissions_row(row):
    return row["Consumption"] * row["Emission Factor (kg CO₂/unit)"]

def plot_emissions(df):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(df["Energy Source"], df["CO₂ Emissions (kg)"], color='orange')
    total = df["CO₂ Emissions (kg)"].sum()
    for i, value in enumerate(df["CO₂ Emissions (kg)"]):
        percent = (value / total) * 100
        ax.text(i, value + 5, f"{percent:.1f}%", ha='center', va='bottom', fontsize=9)
    ax.set_xlabel("Energy Source")
    ax.set_ylabel("CO₂ Emissions (kg)")
    ax.set_title("Emission Contribution by Source")
    plt.xticks(rotation=30, ha='right')
    st.pyplot(fig)

# ===== Main App =====
def emission_estimator():
    st.set_page_config(page_title="🌍 Emission Estimator", layout="centered")
    st.title("🌍 Emission Estimator")
    st.markdown("Estimate CO₂ emissions from petroleum-related energy use.")

    with st.expander("ℹ️ About this tool"):
        st.info("""
        This calculator estimates CO₂ emissions based on your energy consumption.
        Emission factors used are industry standards. Results are shown in both kg and tonnes.
        """)

    df = get_emission_factors()
    st.subheader("📥 Input Energy Consumption")

    df["Consumption"] = df["Energy Source"].apply(
        lambda src: st.number_input(f"{src}", min_value=0.0, step=0.1, key=src)
    )

    df["CO₂ Emissions (kg)"] = df.apply(calculate_emissions_row, axis=1)
    df["CO₂ Emissions (tonnes)"] = df["CO₂ Emissions (kg)"] / 1000

    df_filtered = df[df["Consumption"] > 0]

    if not df_filtered.empty:
        st.success("✅ Emission Results")

        total_kg = df_filtered["CO₂ Emissions (kg)"].sum()
        total_tonnes = total_kg / 1000

        total_row = pd.DataFrame({
            "Energy Source": ["🔢 Total"],
            "Emission Factor (kg CO₂/unit)": [""],
            "Consumption": [df_filtered["Consumption"].sum()],
            "CO₂ Emissions (kg)": [total_kg],
            "CO₂ Emissions (tonnes)": [total_tonnes]
        })

        df_final = pd.concat([df_filtered, total_row], ignore_index=True)

        st.dataframe(df_final, use_container_width=True)

        # Download
        csv = df_final.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV Report", data=csv, file_name="emission_report.csv", mime="text/csv")

        # Visualization
        st.subheader("📊 Emission Breakdown by Source")
        plot_emissions(df_filtered)

        # Highlight
        st.info(f"🌡 **Total Emissions**: **{total_kg:.2f} kg** / **{total_tonnes:.2f} tonnes**")
    else:
        st.warning("⚠️ Enter at least one non-zero value to calculate emissions.")

# ===== Entry Point for Central App =====
def run():
    emission_estimator()
