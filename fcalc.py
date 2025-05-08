import numpy as np
import streamlit as st

def format_inr(amount):
    return f"₹ {amount:,.2f}"

def compound_interest(P, r, n, t):
    A = P * (1 + r/n)**(n*t)
    return A

def loan_repayment(P, r, n):
    M = P * (r * (1 + r)**n) / ((1 + r)**n - 1)
    return M

def savings_growth(P, D, r, t):
    FV = P * (1 + r)**t + D * ((1 + r)**t - 1) / r
    return FV

st.set_page_config(page_title="Indian Financial Calculator", page_icon="💸", layout="centered")

st.markdown("""
    <style>
        .css-18e3th9 {
            background-color: #f1f1f1;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            padding: 10px 24px;
            border: none;
            border-radius: 5px;
        }
        .stSelectbox>div>div>div>input {
            background-color: #fff;
        }
    </style>
""", unsafe_allow_html=True)

st.title('Indian Financial Calculator')

calculation_type = st.selectbox('Choose calculation type', ['Compound Interest', 'Loan Repayment', 'Savings Growth'], index=0)

if calculation_type == 'Compound Interest':
    P = st.number_input('Principal Amount (P):', value=100000, step=1000)
    r = st.slider('Annual Interest Rate (%) (r):', min_value=1.0, max_value=20.0, value=5.0)
    n = st.slider('Number of Compounds per Year (n):', min_value=1, max_value=12, value=4)
    t = st.number_input('Time in Years (t):', value=10, step=1)

    if st.button('Calculate Compound Interest', key='compound_interest'):
        A = compound_interest(P, r / 100, n, t)
        st.write(f'The Amount after {t} years is: {format_inr(A)}')

elif calculation_type == 'Loan Repayment':
    P = st.number_input('Loan Amount (P):', value=500000, step=1000)
    r = st.slider('Monthly Interest Rate (%) (r):', min_value=1.0, max_value=15.0, value=5.0)
    n = st.number_input('Number of Payments (n):', value=60, step=1)

    if st.button('Calculate Loan Repayment', key='loan_repayment'):
        M = loan_repayment(P, r / 100 / 12, n)
        st.write(f'The Monthly Repayment is: {format_inr(M)}')

elif calculation_type == 'Savings Growth':
    P = st.number_input('Initial Deposit (P):', value=100000, step=1000)
    D = st.number_input('Monthly Deposit (D):', value=1000, step=100)
    r = st.slider('Monthly Interest Rate (%) (r):', min_value=1.0, max_value=15.0, value=5.0)
    t = st.number_input('Time in Months (t):', value=120, step=1)

    if st.button('Calculate Savings Growth', key='savings_growth'):
        FV = savings_growth(P, D, r / 100 / 12, t)
        st.write(f'The Future Value of Savings is: {format_inr(FV)}')