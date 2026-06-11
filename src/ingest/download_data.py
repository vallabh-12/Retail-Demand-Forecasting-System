from ucimlrepo import fetch_ucirepo
from src.config import RAW_DIR, RAW_CSV

def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    dataset = fetch_ucirepo(id=352)
    df = dataset.data.original
    df.to_csv(RAW_CSV, index=False)

    print(f"Saved raw dataset to: {RAW_CSV}")

if __name__ == "__main__":
    main()