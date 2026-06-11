import requests
import os
import streamlit as st
import pandas as pd
import tempfile
import streamlit.components.v1 as components

from pathlib import Path
from evidently import Report
from evidently.metric_preset import DataDriftPreset


# FastAPI endpoint (for local dev)
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/predict")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MONITORING_DIR = PROJECT_ROOT / "data" / "monitoring"


st.set_page_config(
    page_title="Retail Demand Forecast UI",
    page_icon="📈",
    layout="centered",
)

st.title("📈 Retail Demand Forecast UI")
st.write(
    "This app sends your inputs to the FastAPI model server and shows the predicted demand."
)

st.header("Input features")

col1, col2 = st.columns(2)

with col1:
    daily_revenue = st.number_input("Daily revenue", min_value=0.0, value=500.0, step=10.0)
    avg_unit_price = st.number_input("Average unit price", min_value=0.0, value=5.0, step=0.1)
    is_weekend = st.selectbox("Is weekend", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    day_of_week = st.slider("Day of week", min_value=0, max_value=6, value=2)
    month = st.slider("Month", min_value=1, max_value=12, value=6)

with col2:
    week_of_year = st.slider("Week of year", min_value=1, max_value=53, value=24)
    lag_1 = st.number_input("Lag 1 (yesterday's quantity)", min_value=0.0, value=95.0, step=1.0)
    lag_7 = st.number_input("Lag 7 (quantity 7 days ago)", min_value=0.0, value=100.0, step=1.0)
    rolling_mean_7 = st.number_input("Rolling mean 7 days", min_value=0.0, value=98.5, step=0.5)
    rolling_sum_7 = st.number_input("Rolling sum 7 days", min_value=0.0, value=690.0, step=5.0)

if st.button("Get forecast"):
    payload = {
        "daily_revenue": daily_revenue,
        "avg_unit_price": avg_unit_price,
        "is_weekend": is_weekend,
        "day_of_week": day_of_week,
        "month": month,
        "week_of_year": week_of_year,
        "lag_1": lag_1,
        "lag_7": lag_7,
        "rolling_mean_7": rolling_mean_7,
        "rolling_sum_7": rolling_sum_7,
    }

    try:
        resp = requests.post(API_URL, json=payload, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            st.success(f"Predicted demand: **{data['forecast']:.2f} units**")
        else:
            st.error(f"API error {resp.status_code}: {resp.text}")
    except Exception as e:
        st.error(f"Error contacting API: {e}")

st.markdown("---")
st.header("🔍 Data Drift Report")

reference_path = MONITORING_DIR / "reference.parquet"
current_path = MONITORING_DIR / "current.parquet"

if reference_path.exists() and current_path.exists():
    if st.button("Generate drift report"):
        try:
            reference = pd.read_parquet(reference_path)
            current = pd.read_parquet(current_path)

            report = Report(metrics=[DataDriftPreset()])
            report.run(reference_data=reference, current_data=current)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
                report.save_html(tmp.name)

            with open(tmp.name, "r", encoding="utf-8") as f:
                html = f.read()

            components.html(html, height=900, scrolling=True)

        except Exception as e:
            st.error(f"Failed to generate drift report: {e}")
else:
    st.warning("Reference/current monitoring files not found.")