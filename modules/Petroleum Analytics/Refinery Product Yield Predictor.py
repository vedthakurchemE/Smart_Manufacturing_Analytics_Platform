# 📘 Module 2: Refinery Product Yield Predictor | PetroStream AI Suite
# 🔍 Predict gasoline, diesel, LPG yield based on crude properties
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

def run():
    st.set_page_config(page_title="⛽ Refinery Product Yield Predictor", layout="wide")
    st.title("⛽ Refinery Product Yield Predictor")
    st.markdown("Predict yields of gasoline, diesel, and LPG based on crude assay properties.")

    # ---- Sample Data ----
    # Insert or load your DataFrame here instead of upload
    # Example demo DataFrame (replace this with real data or a loading method)
    df = pd.DataFrame({
        'Density': [0.82, 0.85, 0.83, 0.86],
        'Sulfur': [0.8, 1.2, 0.9, 1.5],
        'Viscosity': [1.1, 1.3, 1.4, 1.2],
        'Gasoline': [38, 35, 37, 33],
        'Diesel': [45, 47, 44, 49],
        'LPG': [7, 8, 7.5, 8.2]
    })

    st.subheader("🔍 Input Data Preview")
    st.dataframe(df.head(), use_container_width=True)

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    with st.expander("🛠️ Configure Inputs"):
        features = st.multiselect("Select Features (Crude Properties)", options=numeric_cols, default=numeric_cols[:-3])
        targets = st.multiselect("Select Targets (Yields)", options=numeric_cols, default=numeric_cols[-3:])

    if features and targets:
        X = df[features]
        y = df[targets]

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Model training
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Predict and evaluate
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)

        st.success("✅ Model trained successfully!")
        st.markdown(f"**🎯 R² Score:** `{r2:.3f}`")
        st.markdown(f"**📉 Mean Absolute Error:** `{mae:.3f}`")

        # Plot actual vs predicted
        st.subheader("📊 Actual vs Predicted Yields")
        fig, ax = plt.subplots(figsize=(10, 4))
        for i, target in enumerate(targets):
            ax.scatter(y_test[target], y_pred[:, i], label=target)
            ax.plot([y_test[target].min(), y_test[target].max()],
                    [y_test[target].min(), y_test[target].max()], linestyle='--', color='gray')
        ax.set_xlabel("Actual")
        ax.set_ylabel("Predicted")
        ax.legend()
        st.pyplot(fig)

        st.subheader("🧪 Make New Predictions")
        input_data = {}
        for feature in features:
            input_data[feature] = st.number_input(f"{feature}", value=float(df[feature].mean()))

        if st.button("🔮 Predict Yields"):
            input_df = pd.DataFrame([input_data])
            prediction = model.predict(input_df)[0]
            result = pd.DataFrame({"Product": targets, "Predicted Yield (%)": prediction.round(2)})
            st.table(result)
