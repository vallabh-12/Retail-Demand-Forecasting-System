# import duckdb
# from src.config import DUCKDB_FILE, SQL_DIR, PROCESSED_DIR

# def run_sql_file(con, sql_path):
#     with open(sql_path, "r", encoding="utf-8") as f:
#         con.execute(f.read())

# def main():
#     PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

#     con = duckdb.connect(str(DUCKDB_FILE))
#     run_sql_file(con, SQL_DIR / "clean_online_retail.sql")
#     run_sql_file(con, SQL_DIR / "build_daily_features.sql")
#     con.close()

#     print("DuckDB pipeline completed successfully.")

# if __name__ == "__main__":
#     main()




import duckdb
from src.config import DUCKDB_FILE, SQL_DIR, PROCESSED_DIR

def run_sql_file(con, sql_path):
    with open(sql_path, "r", encoding="utf-8") as f:
        con.execute(f.read())

def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(str(DUCKDB_FILE))

    run_sql_file(con, SQL_DIR / "clean_online_retail.sql")
    print("cleaned_retail rows:", con.execute("SELECT COUNT(*) FROM cleaned_retail").fetchone()[0])

    run_sql_file(con, SQL_DIR / "build_daily_features.sql")
    print("daily_demand rows:", con.execute("SELECT COUNT(*) FROM daily_demand").fetchone()[0])
    print("model_features rows:", con.execute("SELECT COUNT(*) FROM model_features").fetchone()[0])

    print(con.execute("SELECT * FROM model_features LIMIT 5").fetchdf())

    con.close()
    print("DuckDB pipeline completed successfully.")

if __name__ == "__main__":
    main()