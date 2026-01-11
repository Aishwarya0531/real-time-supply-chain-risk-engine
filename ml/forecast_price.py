import pandas as pd
import psycopg2
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from datetime import timedelta

# ---- DB CONNECTION ----
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="supply_chain_risk",
    user="postgres",
    password="1234"
)

query = """
SELECT
    recorded_date,
    price_usd,
    rolling_avg_3,
    rolling_volatility_3,
    price_trend
FROM oil_price_golden_view
ORDER BY recorded_date;
"""

df = pd.read_sql(query, conn)
conn.close()

# ---- BASIC CLEANUP ----
df = df.dropna()

# Encode trend direction
le = LabelEncoder()
df["price_trend_encoded"] = le.fit_transform(df["price_trend"])

# ---- FEATURES & TARGET ----
X = df[["rolling_avg_3", "rolling_volatility_3", "price_trend_encoded"]]
y = df["price_usd"]

# ---- MODEL ----
model = LinearRegression()
model.fit(X, y)

# ---- FORECAST NEXT 7 DAYS ----
last_row = df.iloc[-1]

future_features = pd.DataFrame({
    "rolling_avg_3": [last_row["rolling_avg_3"]] * 7,
    "rolling_volatility_3": [last_row["rolling_volatility_3"]] * 7,
    "price_trend_encoded": [last_row["price_trend_encoded"]] * 7
})

predictions = model.predict(future_features)

forecast_dates = pd.date_range(
    start=last_row["recorded_date"] + timedelta(days=1),
    periods=7
)

forecast_df = pd.DataFrame({
    "forecast_date": forecast_dates,
    "predicted_price": predictions
})

print("\n7-Day Price Forecast:")
print(forecast_df)

# ---- MODEL INTERPRETATION ----
coef_df = pd.DataFrame({
    "feature": X.columns,
    "impact_weight": model.coef_
}).sort_values(by="impact_weight", ascending=False)

print("\nFeature Impact (Driver Analysis):")
print(coef_df)
# ---- RISK ESCALATION CHECK ----
forecast_volatility = forecast_df["predicted_price"].std()
historical_volatility = last_row["rolling_volatility_3"]

print("\nRisk Escalation Check:")
print(f"Recent Historical Volatility: {historical_volatility:.2f}")
print(f"Forecasted Volatility (7-day): {forecast_volatility:.2f}")

if forecast_volatility > historical_volatility:
    print("Risk Escalation Expected: YES")
else:
    print("Risk Escalation Expected: NO")
