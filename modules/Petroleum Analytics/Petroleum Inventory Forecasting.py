# 📘 Module 6: Petroleum Inventory Forecasting | PetroStream AI Suite
# 🛢️ Forecast future tank levels using historical inflow, outflow & inventory data
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from prophet import Prophet
import plotly.express as px

def run():
    st.set_page_config(page_title="📦 Inventory Forecaster", layout="wide")
    st.title("📦 Petroleum Inventory Forecaster")
    st.markdown("Forecast future tank levels using Prophet time series model.")

    st.sidebar.header("📥 Upload Inventory Dataset")
    uploaded_file = st.sidebar.file_uploader("Upload CSV (Date, Inventory)", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if "Date" not in df.columns or "Inventory" not in df.columns:
            st.error("❌ CSV must contain 'Date' and 'Inventory' columns.")
            return
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date")
    else:
        # Simulated data
        st.sidebar.info("No file uploaded. Using simulated tank data.")
        dates = pd.date_range("2024-01-01", periods=100)
        inventory = np.cumsum(np.random.normal(0, 10, 100)) + 500
        df = pd.DataFrame({"Date": dates, "Inventory": inventory})

    st.subheader("📊 Historical Inventory Data")
    st.line_chart(df.set_index("Date"))

    # Prophet expects 'ds' and 'y' columns
    prophet_df = df.rename(columns={"Date": "ds", "Inventory": "y"})

    # Forecast Period
    future_days = st.slider("🔮 Forecast Days", 7, 90, 30)

    # Train model
    m = Prophet()
    m.fit(prophet_df)
    future = m.make_future_dataframe(periods=future_days)
    forecast = m.predict(future)

    # Plot
    st.subheader("📈 Forecasted Inventory Levels")
    fig1 = m.plot(forecast)
    st.pyplot(fig1)

    # Summary metrics
    st.subheader("📉 Forecast Summary")
    future_forecast = forecast[["ds", "yhat"]].tail(future_days)
    st.dataframe(future_forecast.rename(columns={"ds": "Date", "yhat": "Forecasted Inventory"}), use_container_width=True)

    # Download
    st.subheader("📁 Download Forecast")
    download_df = pd.merge(df, forecast[["ds", "yhat"]], left_on="Date", right_on="ds", how="left").drop(columns=["ds"])
    csv = download_df.to_csv(index=False)
    st.download_button("⬇️ Download Forecast CSV", data=csv, file_name="inventory_forecast.csv", mime="text/csv")
