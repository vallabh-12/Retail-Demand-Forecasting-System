# src/monitoring/generate_evidently_report.py

from pathlib import Path
import pandas as pd

from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

from src.config import PROCESSED_DIR

MONITORING_DIR = PROCESSED_DIR.parent / "monitoring"
REPORTS_DIR = PROCESSED_DIR.parent / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def main():
    reference_path = MONITORING_DIR / "reference.parquet"
    current_path = MONITORING_DIR / "current.parquet"

    reference = pd.read_parquet(reference_path)
    current = pd.read_parquet(current_path)

    report = Report(metrics=[DataDriftPreset()])

    report.run(reference_data=reference, current_data=current)

    out_path = REPORTS_DIR / "data_drift_report.html"
    report.save_html(str(out_path))

    print("Evidently data drift report saved to:", out_path)


if __name__ == "__main__":
    main()