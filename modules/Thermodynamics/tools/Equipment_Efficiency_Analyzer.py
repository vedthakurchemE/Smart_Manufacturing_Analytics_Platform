def Equipment_Efficiency_Analyzer():
    import streamlit as st
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from fpdf import FPDF
    import base64
    from io import BytesIO

    # App Configuration
    st.set_page_config(page_title="🛢️ Fuel Efficiency Analyzer", layout="wide")
    st.title("🛢️ Fuel Efficiency Analyzer")
    st.markdown(
        "Upload your petroleum plant dataset to analyze fuel input-output efficiency, visualize patterns, and export results.")

    # Sidebar Configuration
    st.sidebar.header("📊 Efficiency Category Thresholds")
    high_thresh = st.sidebar.slider("High Efficiency ≥", 80, 100, 90)
    med_thresh = st.sidebar.slider("Medium Efficiency ≥", 50, high_thresh, 70)
    anom_thresh = st.sidebar.slider("⚠️ Anomaly Threshold (eff < X%)", 0, 70, 50)

    if st.sidebar.checkbox("👁️ Show All Column Names"):
        st.sidebar.text("📃 Available Columns:")
        uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    else:
        uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.subheader("🔍 Raw Data Preview")
            st.dataframe(df.head(), use_container_width=True)

            numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
            if len(numeric_cols) < 2:
                st.warning("⚠️ Need at least two numeric columns for input/output.")
            else:
                input_col = st.selectbox("🔌 Select Input Fuel Column", numeric_cols)
                output_col = st.selectbox("⚡ Select Output Energy Column",
                                          [col for col in numeric_cols if col != input_col])
                time_col = st.selectbox("🕒 Select Time Column (Optional)", ["None"] + list(df.columns))

                # Efficiency calculation
                df["Efficiency (%)"] = (df[output_col] / df[input_col]) * 100

                def classify_eff(val):
                    if val >= high_thresh:
                        return "High"
                    elif val >= med_thresh:
                        return "Medium"
                    else:
                        return "Low"

                df["Category"] = df["Efficiency (%)"].apply(classify_eff)
                anomalies = df[df["Efficiency (%)"] < anom_thresh]

                st.subheader("📈 Efficiency Statistics")
                st.write(df[["Efficiency (%)", "Category"]].describe())

                # Category counts
                cat_counts = df["Category"].value_counts().to_dict()

                st.markdown("#### 🔹 Efficiency Category Counts")
                for cat, count in cat_counts.items():
                    st.markdown(f"- **{cat}:** {count} records")

                # Trend detection
                if time_col != "None":
                    try:
                        df[time_col] = pd.to_datetime(df[time_col], errors="coerce")
                        df_sorted = df.sort_values(by=time_col)
                        trend = "📈 Increasing" if df_sorted["Efficiency (%)"].iloc[-1] > \
                                                  df_sorted["Efficiency (%)"].iloc[0] else "📉 Decreasing"
                        st.info(f"Efficiency Trend Over Time: **{trend}**")
                    except:
                        st.warning("⚠️ Time column could not be parsed for trend analysis.")

                # Summary table
                st.subheader("📋 Summary Table")
                summary_df = pd.DataFrame({
                    "Metric": ["Average", "Max", "Min"],
                    "Efficiency (%)": [
                        f"{df['Efficiency (%)'].mean():.2f}",
                        f"{df['Efficiency (%)'].max():.2f}",
                        f"{df['Efficiency (%)'].min():.2f}"
                    ]
                })
                st.table(summary_df)

                # Visualizations
                st.subheader("📊 Visualizations")
                col1, col2 = st.columns(2)

                with col1:
                    fig1, ax1 = plt.subplots()
                    sns.histplot(df["Efficiency (%)"], kde=True, ax=ax1, color="skyblue")
                    ax1.set_title("Efficiency Distribution")
                    st.pyplot(fig1)

                with col2:
                    pie_data = df["Category"].value_counts()
                    fig2, ax2 = plt.subplots()
                    ax2.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%", colors=["green", "orange", "red"])
                    ax2.set_title("Efficiency Categories")
                    st.pyplot(fig2)

                if time_col != "None":
                    try:
                        df[time_col] = pd.to_datetime(df[time_col])
                        st.subheader("📈 Time Series Efficiency")
                        smoothing = st.slider("🪄 Smooth (Moving Avg Window)", 1, 30, 1)

                        fig3, ax3 = plt.subplots()
                        if smoothing > 1:
                            df["Smoothed"] = df["Efficiency (%)"].rolling(window=smoothing).mean()
                            sns.lineplot(data=df, x=time_col, y="Efficiency (%)", ax=ax3, label="Actual")
                            sns.lineplot(data=df, x=time_col, y="Smoothed", ax=ax3, label="Smoothed", color="orange")
                        else:
                            sns.lineplot(data=df, x=time_col, y="Efficiency (%)", ax=ax3)
                        ax3.set_title("Efficiency Over Time")
                        st.pyplot(fig3)
                    except Exception as e:
                        st.error(f"⏳ Time parsing failed: {e}")

                # Anomalies display
                st.subheader(f"🚨 Low-Efficiency Records (< {anom_thresh}%)")
                st.dataframe(anomalies)

                # CSV Export
                st.subheader("📥 Download Analyzed CSV")
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("Download CSV", csv, file_name="efficiency_results.csv", mime="text/csv")

                # PDF Export
                st.subheader("📝 Download Efficiency Report (PDF)")
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", "B", 16)
                pdf.cell(200, 10, txt="Fuel Efficiency Report", ln=True, align="C")
                pdf.set_font("Arial", size=12)

                mean_eff = df["Efficiency (%)"].mean()
                max_eff = df["Efficiency (%)"].max()
                min_eff = df["Efficiency (%)"].min()
                total = len(df)

                pdf.cell(200, 10, txt=f"Total Records: {total}", ln=True)
                pdf.cell(200, 10, txt=f"Average Efficiency: {mean_eff:.2f}%", ln=True)
                pdf.cell(200, 10, txt=f"Max Efficiency: {max_eff:.2f}%", ln=True)
                pdf.cell(200, 10, txt=f"Min Efficiency: {min_eff:.2f}%", ln=True)
                pdf.cell(200, 10, txt=f"High Efficiency Records: {cat_counts.get('High', 0)}", ln=True)
                pdf.cell(200, 10, txt=f"Medium Efficiency Records: {cat_counts.get('Medium', 0)}", ln=True)
                pdf.cell(200, 10, txt=f"Low Efficiency Records: {cat_counts.get('Low', 0)}", ln=True)

                pdf_buffer = BytesIO()
                pdf.output(pdf_buffer)
                b64_pdf = base64.b64encode(pdf_buffer.getvalue()).decode("utf-8")
                href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="fuel_efficiency_report.pdf">📄 Download PDF Report</a>'
                st.markdown(href, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ File loading failed: {e}")

def run():
    Equipment_Efficiency_Analyzer()