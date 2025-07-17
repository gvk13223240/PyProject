import streamlit as st
import pandas as pd
import numpy as np
import joblib

model = joblib.load('model.pkl')
model_features = joblib.load('model_columns.pkl')

st.title("Customer Churn Prediction App")
st.write("Enter customer information to predict if they are likely to churn.")

gender = st.selectbox("Gender", ["Select...", "Male", "Female"])
senior_citizen = st.selectbox("Senior Citizen", ["Select...", "Yes", "No"])
partner = st.selectbox("Has Partner", ["Select...", "Yes", "No"])
dependents = st.selectbox("Has Dependents", ["Select...", "Yes", "No"])
tenure = st.slider("Tenure (months)", 0, 72, 1)
internet_service = st.selectbox("Internet Service", ["Select...", "DSL", "Fiber optic", "No"])
contract = st.selectbox("Contract Type", ["Select...", "Month-to-month", "One year", "Two year"])
monthly_charges = st.number_input("Monthly Charges", min_value=0.0, max_value=200.0)
total_charges = st.number_input("Total Charges", min_value=0.0, max_value=10000.0)

if st.button("Predict Churn"):
    if "Select..." in [gender, senior_citizen, partner, dependents, internet_service, contract]:
        st.warning("Please select all dropdown options.")
    else:
        input_data = pd.DataFrame({
            'gender': [gender],
            'SeniorCitizen': [1 if senior_citizen == "Yes" else 0],
            'Partner': [partner],
            'Dependents': [dependents],
            'tenure': [tenure],
            'InternetService': [internet_service],
            'Contract': [contract],
            'MonthlyCharges': [monthly_charges],
            'TotalCharges': [total_charges]
        })

        input_encoded = pd.get_dummies(input_data)
        for col in model_features:
            if col not in input_encoded:
                input_encoded[col] = 0
        input_encoded = input_encoded[model_features]

        prediction = model.predict(input_encoded)[0]
        prob = model.predict_proba(input_encoded)[0][1]

        if prediction == 1:
            st.error(f"🚨 This customer is likely to churn. (Confidence: {prob:.2%})")
        else:
            st.success(f"✅ This customer is likely to stay. (Confidence: {1 - prob:.2%})")
