CREATE TABLE crypto_market (
    coin_id TEXT,
    coin_symbol TEXT,
    coin_name TEXT,

    price_usd DOUBLE PRECISION,
    market_cap DOUBLE PRECISION,
    market_cap_rank INTEGER,
    fully_diluted_valuation DOUBLE PRECISION,

    total_volume DOUBLE PRECISION,
    high_24h DOUBLE PRECISION,
    low_24h DOUBLE PRECISION,

    price_change_24h DOUBLE PRECISION,
    price_change_pct_24h DOUBLE PRECISION,

    market_cap_change_24h DOUBLE PRECISION,
    market_cap_change_percentage_24h DOUBLE PRECISION,

    circulating_supply DOUBLE PRECISION,
    total_supply DOUBLE PRECISION,
    max_supply DOUBLE PRECISION,

    ath DOUBLE PRECISION,
    ath_change_percentage DOUBLE PRECISION,
    ath_date TIMESTAMP,

    atl DOUBLE PRECISION,
    atl_change_percentage DOUBLE PRECISION,
    atl_date TIMESTAMP,

    last_updated TIMESTAMP,

    price_change_pct_1h DOUBLE PRECISION,

    volume_marketcap_ratio DOUBLE PRECISION,
    distance_from_ath_pct DOUBLE PRECISION
);