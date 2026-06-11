import pandas as pd
from src.config import PROCESSED_DIR

def main():
    df = pd.read_parquet(PROCESSED_DIR / "model_features.parquet")
    df = df.sort_values(["date", "stock_code", "country"]).reset_index(drop=True)

    cutoff_date = df["date"].quantile(0.8)

    train_df = df[df["date"] <= cutoff_date].copy()
    test_df = df[df["date"] > cutoff_date].copy()

    train_df.to_parquet(PROCESSED_DIR / "train.parquet", index=False)
    test_df.to_parquet(PROCESSED_DIR / "test.parquet", index=False)

    print("Cutoff date:", cutoff_date)
    print("Train shape:", train_df.shape)
    print("Test shape:", test_df.shape)

if __name__ == "__main__":
    main()