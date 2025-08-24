import streamlit as st
import pandas as pd
import numpy as np
from prophet import Prophet
import matplotlib.pyplot as plt

# --------------------
# Streamlit Page Config
# --------------------
st.set_page_config(page_title="Retail Sales Forecasting", layout="wide")
st.title("📊 Retail Sales Forecasting & Analytics Dashboard")

# --------------------
# File Upload
# --------------------
uploaded_file = st.file_uploader("Upload Sales Data (CSV/Excel)", type=["csv", "xlsx"])

if uploaded_file:
    # --------------------
    # Load Data
    # --------------------
    if uploaded_file.name.endswith("csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Raw Data Preview")
    st.write(df.head())

    # --------------------
    # Basic Data Checks
    # --------------------
    if not {"date", "sales", "product", "region"}.issubset(df.columns):
        st.error("Dataset must contain: date, sales, product, region columns")
    else:
        # Ensure correct data types
        df["date"] = pd.to_datetime(df["date"])
        df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
        df.dropna(subset=["sales"], inplace=True)

        # --------------------
        # Sidebar Filters
        # --------------------
        st.sidebar.header("Filters")
        product_filter = st.sidebar.multiselect("Select Product", options=df["product"].unique(), default=df["product"].unique())
        region_filter = st.sidebar.multiselect("Select Region", options=df["region"].unique(), default=df["region"].unique())

        df_filtered = df[(df["product"].isin(product_filter)) & (df["region"].isin(region_filter))]

        # --------------------
        # KPIs
        # --------------------
        total_sales = df_filtered["sales"].sum()
        avg_monthly_sales = df_filtered.groupby(df_filtered["date"].dt.to_period("M"))["sales"].sum().mean()
        growth_rate = (df_filtered.sort_values("date").iloc[-1]["sales"] - df_filtered.sort_values("date").iloc[0]["sales"]) / df_filtered.sort_values("date").iloc[0]["sales"] * 100

        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Total Sales", f"${total_sales:,.0f}")
        kpi2.metric("Avg Monthly Sales", f"${avg_monthly_sales:,.0f}")
        kpi3.metric("Growth Rate", f"{growth_rate:.2f}%")

        # --------------------
        # Time Series Visualization
        # --------------------
        st.subheader("Sales Over Time")
        sales_over_time = df_filtered.groupby("date")["sales"].sum().reset_index()
        st.line_chart(sales_over_time.set_index("date"))

        # --------------------
        # Top Products & Regions
        # --------------------
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Top Products")
            top_products = df_filtered.groupby("product")["sales"].sum().sort_values(ascending=False).head(5)
            st.bar_chart(top_products)
        with col2:
            st.subheader("Top Regions")
            top_regions = df_filtered.groupby("region")["sales"].sum().sort_values(ascending=False).head(5)
            st.bar_chart(top_regions)

        # --------------------
        # Forecasting with Prophet
        # --------------------
        st.subheader("Sales Forecast")
        forecast_period = st.slider("Months to Forecast", 3, 24, 12)

        forecast_df = sales_over_time.rename(columns={"date": "ds", "sales": "y"})
        model = Prophet()
        model.fit(forecast_df)
        future = model.make_future_dataframe(periods=forecast_period, freq="M")
        forecast = model.predict(future)

        fig1 = model.plot(forecast)
        st.pyplot(fig1)

        st.subheader("Forecast Components")
        fig2 = model.plot_components(forecast)
        st.pyplot(fig2)

else:
    st.info("👆 Please upload a sales dataset to get started. Required columns: date, sales, product, region")