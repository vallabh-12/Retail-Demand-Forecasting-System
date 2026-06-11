import pandas as pd
from src.config import PROCESSED_DIR

def main():
    df = pd.read_parquet(PROCESSED_DIR / "model_features.parquet")

    print("\nShape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nDtypes:")
    print(df.dtypes)

    print("\nHead:")
    print(df.head())

    print("\nMissing values:")
    print(df.isna().sum())

    print("\nDate range:")
    print(df["date"].min(), "to", df["date"].max())

if __name__ == "__main__":
    main()