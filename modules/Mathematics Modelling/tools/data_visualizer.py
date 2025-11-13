# 📘 Module 6: Real-World Data Visualizer | EpiModelAI Suite
# 📊 Visualize real infection data from CSV or API sources
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def run():
    # === Title ===
    st.title("📘 Real-World Data Visualizer")
    st.markdown("Upload COVID-19, Flu, or other disease datasets and visualize infection trends.")

    # === File Upload ===
    file = st.file_uploader("📁 Upload CSV Dataset", type=["csv"])

    if file:
        try:
            df = pd.read_csv(file)
            st.success("📈 Data Loaded Successfully!")
            st.dataframe(df.head())

            # === Column Selection ===
            with st.sidebar:
                st.header("📂 Column Selection")
                date_col = st.selectbox("Select Date Column", df.columns)
                case_col = st.selectbox("Select Cases Column", df.columns)
                optional_col = st.selectbox("Optional: Select Recovered/Deaths Column", ["None"] + list(df.columns))

            # === Date Parsing Safely ===
            try:
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                df = df.dropna(subset=[date_col])
            except Exception as e:
                st.error(f"❌ Could not parse date column: {date_col}. Please ensure it contains valid dates.")
                return

            # === Sorting by Date ===
            df = df.sort_values(by=date_col)

            # === Plot Cases Over Time ===
            st.subheader("📊 Case Timeline")
            fig, ax = plt.subplots()
            ax.plot(df[date_col], df[case_col], label="Cases", color="red")
            if optional_col != "None":
                ax.plot(df[date_col], df[optional_col], label=optional_col, color="green")
            ax.set_xlabel("Date")
            ax.set_ylabel("Count")
            ax.set_title("Cases Over Time")
            ax.legend()
            st.pyplot(fig)

            # === Daily Change Plot ===
            st.subheader("📈 Daily Change")
            df["daily_cases"] = df[case_col].diff().fillna(0)
            fig2, ax2 = plt.subplots()
            ax2.bar(df[date_col], df["daily_cases"], color="orange")
            ax2.set_title("Daily New Cases")
            ax2.set_xlabel("Date")
            ax2.set_ylabel("New Cases")
            st.pyplot(fig2)

            # === Summary Metrics ===
            st.subheader("📊 Key Stats")
            col1, col2 = st.columns(2)
            col1.metric("Total Cases", int(df[case_col].sum()))
            col2.metric("Peak Daily Cases", int(df["daily_cases"].max()))

        except Exception as e:
            st.error(f"🚫 Error loading file: {e}")

    else:
        st.warning("👆 Please upload a `.csv` file to begin.")

    with st.expander("📘 Format Instructions"):
        st.markdown("""
        **Your CSV should include columns like:**  
        - `"date"` (e.g. 2020-04-15)  
        - `"cases"` (e.g. daily or cumulative)  
        - `"recovered"` or `"deaths"` (optional)  

        Example:
        ```
        date,cases,recovered
        2020-04-01,34,5
        2020-04-02,60,9
        ```
        """)
