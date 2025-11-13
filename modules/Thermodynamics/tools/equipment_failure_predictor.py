# 📉 Equipment Failure Predictor (Streamlit + ML)
# 🛢 Part of PetroStream AI Suite | Author: Ved Thakur
def equipment_failure_predictor():
    import streamlit as st
    import pandas as pd
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
    import seaborn as sns
    import matplotlib.pyplot as plt
    import io
    import base64

    # ======================== CONFIG ===========================
    st.set_page_config(page_title="📉 Equipment Failure Predictor", layout="wide")
    st.title("📉 Equipment Failure Predictor (ML Module)")
    st.markdown("""
    Predict the possibility of **equipment failure** based on real-time or historical operational data using Random Forest Classifier.
    - Upload `.csv` containing features and failure status
    - Get accuracy, classification report, confusion matrix
    - Visualize top factors contributing to failure
    - Predict custom scenario and download results
    """)

    # ===================== FUNCTIONS ===========================
    def train_model(df, target_col):
        """Split data, train RandomForest, return results"""
        X = df.drop(columns=[target_col])
        y = df[target_col]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

        model = RandomForestClassifier(n_estimators=200, random_state=42)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        conf_matrix = confusion_matrix(y_test, y_pred)

        return model, X_test, y_test, y_pred, acc, report, conf_matrix

    def plot_feature_importance(model, features):
        """Plot sorted feature importances"""
        importances = model.feature_importances_
        sorted_idx = np.argsort(importances)[::-1]
        top_features = features.columns[sorted_idx[:10]]

        fig, ax = plt.subplots()
        sns.barplot(x=importances[sorted_idx[:10]], y=top_features, palette="Reds_r", ax=ax)
        ax.set_title("🔍 Top Contributing Features")
        return fig

    def plot_conf_matrix(cm):
        """Plot confusion matrix"""
        fig, ax = plt.subplots()
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
        ax.set_title("📌 Confusion Matrix")
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        return fig

    def generate_download_link(df, filename="results.csv"):
        """Return download link for dataframe"""
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">📥 Download CSV</a>'
        return href

    # ====================== FILE UPLOAD ========================
    uploaded_file = st.file_uploader("📂 Upload Equipment Failure Dataset (.csv)", type="csv")

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("✅ File uploaded successfully")
            st.dataframe(df.head(), use_container_width=True)

            # Select target column
            target_col = st.selectbox("🎯 Select Target Column (Failure)", df.columns)

            if pd.api.types.is_numeric_dtype(df[target_col]) or df[target_col].nunique() == 2:
                # Drop rows with NaNs
                df = df.dropna()
                model, X_test, y_test, y_pred, acc, report, conf_matrix = train_model(df, target_col)

                # --- Metrics ---
                st.subheader("📊 Model Metrics")
                st.metric("Model Accuracy", f"{acc * 100:.2f}%")

                st.subheader("📋 Classification Report")
                st.dataframe(pd.DataFrame(report).transpose(), use_container_width=True)

                st.subheader("🧮 Confusion Matrix")
                st.pyplot(plot_conf_matrix(conf_matrix))

                st.subheader("📌 Feature Importance")
                st.pyplot(plot_feature_importance(model, df.drop(columns=[target_col])))

                # --- Live Prediction ---
                st.subheader("🔮 Predict Custom Scenario")
                user_input = {}
                input_df = df.drop(columns=[target_col])
                for col in input_df.columns:
                    user_input[col] = st.number_input(f"{col}", value=float(df[col].mean()))
                user_df = pd.DataFrame([user_input])

                prediction = model.predict(user_df)[0]
                st.success(f"💡 Prediction: **{'Failure' if prediction else 'No Failure'}**")

                # --- Export ---
                st.subheader("📁 Export Prediction Results")
                results_df = X_test.copy()
                results_df["Actual"] = y_test.values
                results_df["Predicted"] = y_pred
                st.markdown(generate_download_link(results_df, "failure_predictions.csv"), unsafe_allow_html=True)

            else:
                st.error("❗Target column must be binary (0/1 or Yes/No).")

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
    else:
        st.info("📥 Upload a valid `.csv` file with operational sensor data and a failure column (0/1 or Yes/No).")

def run():
    equipment_failure_predictor()