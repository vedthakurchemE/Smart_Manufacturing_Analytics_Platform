# 🔬 Process Yield Predictor (Streamlit App + ML)
# Author: Ved Thakur | IPS Academy Indore | ChemEng

import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

def run():
    st.title("🔬 Process Yield Predictor")
    st.write("Upload a dataset, select your features and target, and predict chemical process yield.")

    uploaded_file = st.file_uploader("📂 Upload your dataset (CSV)", type=["csv"])

    if uploaded_file:
        try:
            data = pd.read_csv(uploaded_file)

            if data.empty:
                st.error("❌ Uploaded CSV is empty.")
                return

            st.subheader("📊 Data Preview")
            st.dataframe(data.head())

            st.subheader("🧮 Column Selection")
            target = st.selectbox("🎯 Select the target column (what you want to predict)", data.columns)
            features = st.multiselect("🧩 Select input features (independent variables)",
                                      [col for col in data.columns if col != target])

            if not features or not target:
                st.warning("⚠️ Please select at least one feature and a target.")
                return

            # Drop rows where target is NaN
            data = data.dropna(subset=[target])

            X = data[features]
            y = data[target]

            # Separate numeric and categorical columns
            numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
            categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()

            # Create transformers
            numeric_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='mean')),
                ('scaler', StandardScaler())
            ])

            categorical_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore'))
            ])

            preprocessor = ColumnTransformer(transformers=[
                ('num', numeric_transformer, numeric_cols),
                ('cat', categorical_transformer, categorical_cols)
            ])

            # Final pipeline
            model = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('regressor', LinearRegression())
            ])

            # Train/Test Split
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Fit model
            model.fit(X_train, y_train)

            # Predict
            y_pred = model.predict(X_test)

            # Metrics
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            st.subheader("✅ Model Performance")
            st.write(f"**Mean Squared Error:** {mse:.2f}")
            st.write(f"**R² Score:** {r2:.2f}")

            # Plot Actual vs Predicted
            st.subheader("📈 Actual vs Predicted Yield")
            fig, ax = plt.subplots()
            ax.scatter(y_test, y_pred, alpha=0.6)
            ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
            ax.set_xlabel("Actual Yield")
            ax.set_ylabel("Predicted Yield")
            ax.set_title("Actual vs Predicted")
            st.pyplot(fig)

            # Optional: Display transformed columns
            with st.expander("🧠 Show Model Pipeline Details"):
                ct = model.named_steps['preprocessor']
                if hasattr(ct, 'transformers_'):
                    st.write("Transformers used:")
                    for name, trans, cols in ct.transformers_:
                        st.write(f"**{name}** → Columns: {cols}")
                else:
                    st.warning("Pipeline not yet fitted.")

        except Exception as e:
            st.error(f"❌ Error: {e}")
