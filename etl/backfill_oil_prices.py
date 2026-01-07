import requests
import psycopg2
import os

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

if not API_KEY:
    raise Exception("ALPHAVANTAGE_API_KEY not set")

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "supply_chain_risk",
    "user": "postgres",
    "password": "1234"
}

url = "https://www.alphavantage.co/query"
params = {
    "function": "WTI",
    "apikey": API_KEY
}

response = requests.get(url, params=params)
data = response.json()

if "data" not in data:
    raise Exception(f"Unexpected API response: {data}")

conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

insert_query = """
INSERT INTO oil_price_raw (price_usd, recorded_at, source)
VALUES (%s, %s, %s)
ON CONFLICT (recorded_at, source) DO NOTHING;
"""

rows_inserted = 0

for record in data["data"]:
    price = float(record["value"])
    recorded_at = record["date"]

    cursor.execute(
        insert_query,
        (price, recorded_at, "AlphaVantage")
    )
    rows_inserted += 1

conn.commit()
cursor.close()
conn.close()

print(f"Backfill completed. Processed {rows_inserted} records.")
