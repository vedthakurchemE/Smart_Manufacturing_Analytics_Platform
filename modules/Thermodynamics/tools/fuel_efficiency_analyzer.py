# 🛢️ Fuel Efficiency Analyzer (PetroStream AI Suite)
# 📘 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng
# ⚙️ Fuel property analysis, efficiency estimation | Streamlit + Pandas

import streamlit as st
import pandas as pd
import numpy as np
import io


def run():
    st.title("⛽ Fuel Efficiency Analyzer")
    st.caption("Upload fuel combustion data to estimate efficiency and performance.")

    uploaded_file = st.file_uploader("📂 Upload CSV file with combustion data", type=["csv"])

    if uploaded_file:
        try:
            # Decode file using BytesIO
            stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
            df = pd.read_csv(stringio)
            st.success("✅ File uploaded successfully.")
            st.dataframe(df.head())

            if 'Fuel_Mass' in df.columns and 'Energy_Output' in df.columns:
                df['Efficiency (%)'] = (df['Energy_Output'] / df['Fuel_Mass']) * 100
                st.line_chart(df[['Efficiency (%)']])

                st.metric("🔥 Average Efficiency (%)", round(df['Efficiency (%)'].mean(), 2))

                # Downloadable result
                result_csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Results", result_csv, "fuel_efficiency_results.csv", "text/csv")
            else:
                st.warning("⚠️ Columns `Fuel_Mass` and `Energy_Output` are required.")

        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")

    else:
        st.info("📄 Please upload a .csv file with `Fuel_Mass` and `Energy_Output` columns.")
