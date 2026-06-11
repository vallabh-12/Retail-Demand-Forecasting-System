import os
import time
import joblib
import pandas as pd
import mlflow

from prophet import Prophet
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

from src.config import PROCESSED_DIR

mlflow.set_tracking_uri("sqlite:///mlflow.db")


def load_daily_series():
    df = pd.read_parquet(PROCESSED_DIR / "daily_demand.parquet")

    series_df = (
        df.groupby("date", as_index=False)["daily_quantity"]
        .sum()
        .sort_values("date")
        .rename(columns={"date": "ds", "daily_quantity": "y"})
    )

    return series_df


def main():
    df = load_daily_series()

    cutoff = df["ds"].quantile(0.8)

    train_df = df[df["ds"] <= cutoff].copy()
    test_df = df[df["ds"] > cutoff].copy()

    mlflow.set_experiment("retail-demand-forecasting")

    with mlflow.start_run(run_name="prophet_baseline"):
        model = Prophet(
            daily_seasonality=False,
            weekly_seasonality=True,
            yearly_seasonality=True
        )

        start_time = time.time()
        model.fit(train_df)
        training_time = time.time() - start_time

        future = test_df[["ds"]].copy()
        forecast = model.predict(future)

        preds = forecast["yhat"].values
        actuals = test_df["y"].values

        mae = mean_absolute_error(actuals, preds)
        rmse = root_mean_squared_error(actuals, preds)

        mlflow.log_param("model_type", "Prophet")
        mlflow.log_param("daily_seasonality", False)
        mlflow.log_param("weekly_seasonality", True)
        mlflow.log_param("yearly_seasonality", True)
        mlflow.log_param("train_rows", len(train_df))
        mlflow.log_param("test_rows", len(test_df))

        mlflow.log_metric("mae", mae)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("training_time_sec", training_time)

        os.makedirs("artifacts", exist_ok=True)
        model_path = "artifacts/prophet_model.pkl"
        joblib.dump(model, model_path)
        mlflow.log_artifact(model_path, artifact_path="model_artifacts")

        print("Prophet completed")
        print("MAE:", mae)
        print("RMSE:", rmse)
        print("Training time:", training_time)


if __name__ == "__main__":
    main()