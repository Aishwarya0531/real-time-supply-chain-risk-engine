CREATE TABLE oil_price_raw (
    id SERIAL PRIMARY KEY,
    price_usd NUMERIC(10,2),
    recorded_at TIMESTAMP,
    source TEXT,
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE oil_price_clean (
    id SERIAL PRIMARY KEY,
    price_usd NUMERIC(10,2) NOT NULL,
    recorded_date DATE NOT NULL,
    source TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO oil_price_raw (price_usd, recorded_at, source)
VALUES (82.45, '2026-01-05 18:00:00', 'manual_test');

INSERT INTO oil_price_clean (price_usd, recorded_date, source)
SELECT
    price_usd,
    DATE(recorded_at),
    source
FROM oil_price_raw;
select * from oil_price_clean;
SELECT * FROM oil_price_raw
ORDER BY inserted_at DESC;

SELECT recorded_at, source, COUNT(*)
FROM oil_price_raw
GROUP BY recorded_at, source
HAVING COUNT(*) > 1;
DELETE FROM oil_price_raw a
USING oil_price_raw b
WHERE a.ctid > b.ctid
  AND a.recorded_at = b.recorded_at
  AND a.source = b.source;
ALTER TABLE oil_price_raw
ADD CONSTRAINT unique_oil_price_per_day
UNIQUE (recorded_at, source);

select * from oil_price_raw;
INSERT INTO oil_price_clean (recorded_date, price_usd, source)
SELECT
    recorded_at::DATE,
    price_usd,
    source
FROM oil_price_raw
ON CONFLICT (recorded_date) DO NOTHING;
ALTER TABLE oil_price_clean
ADD CONSTRAINT unique_clean_oil_date
UNIQUE (recorded_date);
INSERT INTO oil_price_clean (recorded_date, price_usd, source)
SELECT
    recorded_at::DATE,
    price_usd,
    source
FROM oil_price_raw
ON CONFLICT (recorded_date) DO NOTHING;
ALTER TABLE oil_price_clean
ADD CONSTRAINT unique_clean_oil_date
UNIQUE (recorded_date);
CREATE OR REPLACE VIEW oil_price_risk_final AS
SELECT
    recorded_date,
    price_usd,
    rolling_volatility_3,
    price_trend,

    CASE
        WHEN rolling_volatility_3 > 5 AND price_trend = 'UP'
            THEN 'HIGH_INFLATION_RISK'

        WHEN rolling_volatility_3 > 5 AND price_trend = 'DOWN'
            THEN 'DEMAND_RISK'

        WHEN rolling_volatility_3 BETWEEN 2 AND 5
            THEN 'MEDIUM_RISK'

        ELSE 'LOW_RISK'
    END AS risk_category

FROM oil_price_trend_signal;
SELECT *
FROM oil_price_risk_final
ORDER BY recorded_date DESC
LIMIT 10;
CREATE OR REPLACE VIEW oil_price_risk_final AS
SELECT
    recorded_date,
    price_usd,
    rolling_volatility_3,
    price_trend,

    CASE
        WHEN rolling_volatility_3 > 5 AND price_trend = 'UP'
            THEN 'HIGH_INFLATION_RISK'

        WHEN rolling_volatility_3 > 5 AND price_trend = 'DOWN'
            THEN 'DEMAND_RISK'

        WHEN rolling_volatility_3 BETWEEN 2 AND 5
            THEN 'MEDIUM_RISK'

        ELSE 'LOW_RISK'
    END AS risk_category

FROM oil_price_trend_signal;
SELECT *
FROM oil_price_risk_final
ORDER BY recorded_date DESC
LIMIT 10;
CREATE OR REPLACE VIEW oil_price_golden_view AS
SELECT
    recorded_date,
    price_usd,
    ROUND(
        AVG(price_usd) OVER (
            ORDER BY recorded_date
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS rolling_avg_3,

    rolling_volatility_3,
    price_trend,
    risk_category

FROM oil_price_risk_final
ORDER BY recorded_date;
SELECT *
FROM oil_price_golden_view
ORDER BY recorded_date DESC
LIMIT 10;

