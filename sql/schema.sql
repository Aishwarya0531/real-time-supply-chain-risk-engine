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

