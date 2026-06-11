from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
SQL_DIR = PROJECT_ROOT / "sql"

RAW_CSV = RAW_DIR / "online_retail_raw.csv"
DUCKDB_FILE = DATA_DIR / "retail.duckdb"
DAILY_OUTPUT = PROCESSED_DIR / "daily_demand.parquet"