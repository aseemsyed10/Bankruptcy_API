# frontend/app.py

import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Bankruptcy Predictor", layout="wide")
st.title("💼 Bankruptcy Prediction Dashboard")

API_URL = "http://localhost:8000"

st.subheader("📥 Enter 95 Financial Features")
features = []
cols = st.columns(5)
for i in range(95):
    with cols[i % 5]:
        val = st.number_input(f"Feature {i+1}", value=0.0, step=0.01, format="%.2f")
        features.append(val)

if st.button("✅ Validate Input"):
    with st.spinner("Validating..."):
        val_resp = requests.post(f"{API_URL}/validate", json={"features": features})
        if val_resp.status_code == 200:
            st.success("✅ Input passed validation!")
        else:
            st.error("❌ Validation failed.")
            st.json(val_resp.json())

if st.button("📊 Predict Bankruptcy"):
    with st.spinner("Predicting..."):
        predict_resp = requests.post(f"{API_URL}/predict", json={"features": features})
        if predict_resp.status_code == 200:
            result = predict_resp.json()
            pred = "Bankrupt" if result["prediction"] == 1 else "Not Bankrupt"
            prob = result["probability"]
            st.success(f"### Prediction: **{pred}**")
            st.metric("📈 Bankruptcy Probability", f"{prob*100:.2f}%")
        else:
            st.error("Prediction failed.")
            st.json(predict_resp.json())

        explain_resp = requests.post(f"{API_URL}/explain", json={"features": features})
        if explain_resp.status_code == 200:
            data = explain_resp.json()
            df = pd.DataFrame({
                "Feature": data["feature_names"],
                "SHAP Value": data["shap_values"],
                "Input Value": data["feature_values"]
            })
            st.subheader("🧠 SHAP Feature Importance")
            fig = px.strip(df, x="SHAP Value", y="Feature", hover_data=["Input Value"], orientation='h')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("SHAP explanation failed.")
