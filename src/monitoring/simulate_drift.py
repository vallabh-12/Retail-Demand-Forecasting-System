# src/monitoring/simulate_drift.py

from pathlib import Path
import numpy as np
import pandas as pd

from src.config import PROCESSED_DIR

MONITORING_DIR = PROCESSED_DIR.parent / "monitoring"
MONITORING_DIR.mkdir(parents=True, exist_ok=True)


def main():
    test_path = PROCESSED_DIR / "test.parquet"
    df = pd.read_parquet(test_path)

    reference = df.copy()
    reference.to_parquet(MONITORING_DIR / "reference.parquet", index=False)

    current = df.copy()

    current["avg_unit_price"] = current["avg_unit_price"] * 1.35
    current["daily_quantity"] = (current["daily_quantity"] * 0.7).clip(lower=0)
    current["daily_revenue"] = current["daily_revenue"] * 0.8

    weekday_mask = current["is_weekend"] == 0
    flip_idx = current[weekday_mask].sample(frac=0.1, random_state=42).index
    current.loc[flip_idx, "is_weekend"] = 1

    noise = np.random.normal(loc=0.0, scale=5.0, size=len(current))
    current["daily_quantity"] = (current["daily_quantity"] + noise).clip(lower=0)

    current.to_parquet(MONITORING_DIR / "current.parquet", index=False)

    print("Saved reference and current drifted datasets to:", MONITORING_DIR)


if __name__ == "__main__":
    main()