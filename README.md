# Retail-Demand-Forecasting-System

An end-to-end retail demand forecasting project built using messy transactional retail data. The system uses DuckDB SQL for cleaning and feature engineering, MLflow for experiment tracking, FastAPI for model serving, Evidently for drift monitoring, Streamlit for the frontend, and Docker Compose for containerized execution.

## Overview

This project forecasts daily retail demand from real-world transactional data and demonstrates a complete MLOps workflow from raw data ingestion to live model serving and drift monitoring. The goal was to build something closer to a production-ready ML system rather than only training a model in a notebook. [web:365][web:371]

## Dataset

The project uses the **UCI Online Retail** dataset, which contains raw transaction-level retail data. The data is cleaned and aggregated into daily demand using DuckDB SQL, and forecasting features such as lag values, rolling averages, and calendar features are engineered for model training. 

## Pipeline

- Clean messy retail transactions using DuckDB SQL
- Aggregate data to daily demand level
- Engineer lag, rolling, and calendar features
- Train and compare Linear Regression, XGBoost, and Prophet
- Track experiments and metrics with MLflow
- Serve the best model through FastAPI
- Simulate drift and generate an Evidently report
- Expose predictions and monitoring through Streamlit

This modular workflow reflects common MLOps practices where data preparation, training, serving, and monitoring are treated as separate stages. 

## Architecture

```mermaid
flowchart LR
    A[Raw Retail Data] --> B[DuckDB SQL Cleaning]
    B --> C[Feature Engineering]
    C --> D[Model Training]
    D --> E[MLflow Tracking]
    E --> F[Best Model]
    F --> G[FastAPI /predict]
    G --> H[Streamlit UI]
    C --> I[Reference Data]
    C --> J[Current Drifted Data]
    I --> K[Evidently Drift Report]
    J --> K
    K --> H
```

## Model Comparison

| Model | MAE | RMSE | Notes |
|---|---:|---:|---|
| Linear Regression | 11.63 | 35.67 | Baseline |
| XGBoost | 3.06 | 20.02 | Best-performing model |
| Prophet | 10505.95 | 15297.98 | Time-series benchmark |

The model comparison shows why experiment tracking matters: a simple baseline provides a reference point, while XGBoost performed best on the engineered feature set.




## Run Locally

Install dependencies:

pip install -r requirements.txt

## Run the pipeline and train models:


python -m src.ingest.download_data
python -m src.data.run_duckdb_pipeline
python -m src.features.make_train_test_split
python -m src.train.train_linear
python -m src.train.train_xgboost
python -m src.train.train_prophet

## Start MLflow:

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

## Start FastAPI:

uvicorn src.api.app:app --reload


## Start Streamlit:

streamlit run src/ui/streamlit_app.py

## Docker

Run the frontend and backend together with Docker Compose:

docker compose build
docker compose up


Then open:

- FastAPI docs: `http://localhost:8000/docs`
- Streamlit UI: `http://localhost:8501`

Using separate Streamlit and FastAPI services with Docker Compose is a practical deployment pattern for ML applications with a UI and backend API. 

## Monitoring

The project includes data drift monitoring using Evidently. A drifted “current” dataset is simulated from the processed feature data, compared against reference data, and rendered as a visual report directly inside the Streamlit app. 

## Future Improvements

- CI/CD with GitHub Actions
- Cloud deployment for API and frontend
- Automated retraining
- MLflow registry promotion workflow
- More advanced retail features and hierarchical forecasting

## License

MIT License

## Contact

**Shrivallabha Patil**  
Guildford, England, UK

- GitHub: https://github.com/vallabh-12
- LinkedIn: https://www.linkedin.com/in/shrivallabha-patil/
