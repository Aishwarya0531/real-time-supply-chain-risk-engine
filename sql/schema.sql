CREATE TABLE oil_price_raw (
    id SERIAL PRIMARY KEY,
    price_usd NUMERIC(10,2),
    recorded_at TIMESTAMP,
    source TEXT,
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
