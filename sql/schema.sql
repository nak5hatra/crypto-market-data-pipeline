CREATE TABLE dim_coin (
    coin_id TEXT PRIMARY KEY,
    coin_symbol TEXT,
    coin_name TEXT
);

CREATE TABLE fact_crypto_price (
    id SERIAL PRIMARY KEY,
    coin_id TEXT NOT NULL REFERENCES dim_coin(coin_id),
    price_usd NUMERIC NOT NULL,
    market_cap NUMERIC,
    total_volume NUMERIC,
    volume_marketcap_ratio NUMERIC,
    distance_from_ath_pct NUMERIC,
    last_updated TIMESTAMP NOT NULL,
    
    UNIQUE (coin_id, last_updated)
);

CREATE INDEX idx_fact_coin_time
ON fact_crypto_price (coin_id, last_updated);