import requests
import psycopg2
import os

# -------------------------------
# CONFIG
# -------------------------------
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

if not API_KEY:
    raise Exception("ALPHAVANTAGE_API_KEY not set in environment variables")

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "supply_chain_risk",
    "user": "postgres",
    "password": "1234"
}

# -------------------------------
# STEP 1: FETCH DATA FROM API
# -------------------------------
url = "https://www.alphavantage.co/query"
params = {
    "function": "WTI",
    "apikey": API_KEY
}

response = requests.get(url, params=params)

if response.status_code != 200:
    raise Exception(f"API request failed with status code {response.status_code}")

data = response.json()

if "data" not in data:
    raise Exception(f"Unexpected API response: {data}")

latest = data["data"][0]
price = float(latest["value"])
recorded_date = latest["date"]

# -------------------------------
# STEP 2: CONNECT TO POSTGRESQL
# -------------------------------
conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

# -------------------------------
# STEP 3: INSERT INTO RAW TABLE
# -------------------------------
insert_query = """
INSERT INTO oil_price_raw (price_usd, recorded_at, source)
VALUES (%s, %s, %s)
ON CONFLICT (recorded_at, source) DO NOTHING;

"""

cursor.execute(
    insert_query,
    (price, recorded_date, "AlphaVantage")
)

conn.commit()

cursor.close()
conn.close()

print("Inserted oil price successfully.")
