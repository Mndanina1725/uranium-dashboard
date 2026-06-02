import pandas as pd
import sqlite3
import shutil
import os

# Build DB in system temp dir to avoid filesystem restrictions, then copy to project
TMP_DB = "/tmp/uranium_dashboard.db"
FINAL_DB = "uranium_dashboard.db"

conn = sqlite3.connect(TMP_DB)

pd.read_csv("data/cleaned/dim_country.csv").to_sql(
    "dim_country", conn, if_exists="replace", index=False)
pd.read_csv("data/cleaned/fact_uranium_price.csv").to_sql(
    "fact_uranium_price", conn, if_exists="replace", index=False)
pd.read_csv("data/cleaned/fact_production.csv").to_sql(
    "fact_production", conn, if_exists="replace", index=False)
pd.read_csv("data/cleaned/fact_nuclear_generation.csv").to_sql(
    "fact_nuclear_generation", conn, if_exists="replace", index=False)

# Verify row counts
for table in ["dim_country", "fact_uranium_price", "fact_production", "fact_nuclear_generation"]:
    count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"{table}: {count} rows")

conn.close()

# Copy to project folder
shutil.copy(TMP_DB, FINAL_DB)
print(f"uranium_dashboard.db created at: {os.path.abspath(FINAL_DB)}")
