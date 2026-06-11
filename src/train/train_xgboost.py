import mlflow
import time
import pandas as pd
import mlflow
import mlflow.sklearn

from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

from src.config import PROCESSED_DIR

FEATURES = [
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

TARGET = "daily_quantity"


def load_data():
    train_df = pd.read_parquet(PROCESSED_DIR / "train.parquet")
    test_df = pd.read_parquet(PROCESSED_DIR / "test.parquet")
    return train_df, test_df


def main():
    train_df, test_df = load_data()

    X_train = train_df[FEATURES]
    y_train = train_df[TARGET]

    X_test = test_df[FEATURES]
    y_test = test_df[TARGET]

    model_params = {
        "objective": "reg:squarederror",
        "n_estimators": 300,
        "max_depth": 6,
        "learning_rate": 0.05,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "random_state": 42,
        "n_jobs": -1,
        "tree_method": "hist"
    }

    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("retail-demand-forecasting")

    with mlflow.start_run(run_name="xgboost_baseline"):
        model = XGBRegressor(**model_params)

        start_time = time.time()
        model.fit(X_train, y_train)
        training_time = time.time() - start_time

        preds = model.predict(X_test)

        mae = mean_absolute_error(y_test, preds)
        rmse = root_mean_squared_error(y_test, preds)

        mlflow.log_param("model_type", "XGBRegressor")
        mlflow.log_params(model_params)
        mlflow.log_param("features", ",".join(FEATURES))
        mlflow.log_param("train_rows", len(train_df))
        mlflow.log_param("test_rows", len(test_df))

        mlflow.log_metric("mae", mae)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("training_time_sec", training_time)

        mlflow.sklearn.log_model(model, name="model")

        print("XGBoost completed")
        print("MAE:", mae)
        print("RMSE:", rmse)
        print("Training time:", training_time)


if __name__ == "__main__":
    main()