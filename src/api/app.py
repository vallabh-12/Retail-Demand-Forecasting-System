from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import mlflow


# IMPORTANT: replace this with your actual XGBoost run ID
BEST_MODEL_URI = "runs:/dd759092ef2d4975902bdf03e28e9c8a/model"

FEATURE_COLUMNS = [
    "daily_revenue",
    "avg_unit_price",
    "is_weekend",
    "day_of_week",
    "month",
    "week_of_year",
    "lag_1",
    "lag_7",
    "rolling_mean_7",
    "rolling_sum_7",
]

mlflow.set_tracking_uri("sqlite:///mlflow.db")

app = FastAPI(title="Retail Demand Forecast API")

model = mlflow.pyfunc.load_model(BEST_MODEL_URI)


class DemandRequest(BaseModel):
    daily_revenue: float
    avg_unit_price: float
    is_weekend: int
    day_of_week: int
    month: int
    week_of_year: int
    lag_1: float
    lag_7: float
    rolling_mean_7: float
    rolling_sum_7: float


class DemandBatchRequest(BaseModel):
    records: List[DemandRequest]

@app.get("/")
def root():
    return {
        "message": "Retail Demand Forecast API is running",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/predict")
def predict_single(payload: DemandRequest):
    data = pd.DataFrame([payload.dict()], columns=FEATURE_COLUMNS)
    prediction = model.predict(data)[0]
    return {"forecast": float(prediction)}


@app.post("/predict_batch")
def predict_batch(payload: DemandBatchRequest):
    data = pd.DataFrame([r.dict() for r in payload.records], columns=FEATURE_COLUMNS)
    preds = model.predict(data)
    return {"forecasts": [float(p) for p in preds]}