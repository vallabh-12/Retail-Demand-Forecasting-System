import os
from pathlib import Path
import tempfile

import pandas as pd
import requests
import streamlit as st
import streamlit.components.v1 as components
from evidently import Report
from evidently.presets import DataDriftPreset

API_URL = os.getenv(
    "API_URL",
    "https://retail-demand-forecasting-system-7v3n.onrender.com/predict",
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MONITORING_DIR = PROJECT_ROOT / "data" / "monitoring"

REFERENCE_PATH = MONITORING_DIR / "reference.parquet"
CURRENT_PATH = MONITORING_DIR / "current.parquet"

st.set_page_config(
    page_title="Retail Demand Forecast UI",
    page_icon="📈",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 95rem;
        padding-top: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    iframe {
        width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📈 Retail Demand Forecast UI")
st.write("This app sends your inputs to the FastAPI model server and shows the predicted demand.")

try:
    base_api_url = API_URL.rsplit("/predict", 1)[0]
    health_resp = requests.get(base_api_url + "/docs", timeout=5)
    if health_resp.status_code == 200:
        st.success("API status: Connected")
    else:
        st.warning("API status: API reachable, but check endpoint setup.")
except Exception:
    st.error("API status: Cannot reach FastAPI service")

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
        with st.spinner("Generating forecast..."):
            resp = requests.post(API_URL, json=payload, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            st.success(f"Predicted demand: **{data['forecast']:.2f} units**")
        else:
            st.error(f"API error {resp.status_code}: {resp.text}")
    except Exception as e:
        st.error(f"Error contacting API: {e}")

st.markdown("---")
st.header("🔍 Data Drift Report")
st.caption(
    "This compares the current monitoring data with the reference dataset. "
    "If drift is detected in many columns, it may indicate that the live data is changing from the training pattern."
)

if REFERENCE_PATH.exists() and CURRENT_PATH.exists():
    if st.button("Generate drift report"):
        try:
            with st.spinner("Generating live drift report..."):
                reference = pd.read_parquet(REFERENCE_PATH)
                current = pd.read_parquet(CURRENT_PATH)

                report = Report(metrics=[DataDriftPreset()])
                eval_result = report.run(reference_data=reference, current_data=current)

                with tempfile.NamedTemporaryFile(mode="w+b", suffix=".html", delete=False) as tmp:
                    temp_path = tmp.name

                try:
                    eval_result.save_html(temp_path)
                    html = Path(temp_path).read_text(encoding="utf-8")

                    components.html(
                        html,
                        height=1200,
                        scrolling=True,
                    )
                finally:
                    try:
                        Path(temp_path).unlink(missing_ok=True)
                    except Exception:
                        pass

            st.info(
                "Interpretation tip: if drift is detected for 0 out of 13 columns, "
                "the current data is statistically similar to the reference data."
            )

        except Exception as e:
            st.error(f"Failed to generate drift report: {e}")
else:
    st.warning("Reference/current monitoring files not found.")