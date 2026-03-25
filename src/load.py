import polars as pl
from sqlalchemy import create_engine, text
from config import Config
from utils import get_logger

logger = get_logger(__name__)

engine = create_engine(Config.DB_URL)


def load_dim_coin(file_path: str):

    try:
        logger.info("Loading dim_coin...")

        df = pl.read_parquet(file_path)

        with engine.begin() as conn:
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_coin (
                coin_id TEXT PRIMARY KEY,
                coin_symbol TEXT,
                coin_name TEXT
            )
            """))

            
            conn.execute(text("DELETE FROM dim_coin"))

        df.write_database(
            table_name="dim_coin",
            connection=engine,
            if_table_exists="append"
        )

        logger.info("dim_coin loaded successfully")

    except Exception as e:
        logger.error(f"Error loading dim_coin: {e}")
        raise


def load_fact_crypto(file_path: str):
    """
    Loads fact table with idempotency (daily overwrite).
    """
    try:
        logger.info("Loading fact_crypto_price...")

        df = pl.read_parquet(file_path)

        with engine.begin() as conn:
            
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS fact_crypto_price (
                    id SERIAL PRIMARY KEY,
                    coin_id TEXT,
                    price_usd FLOAT,
                    market_cap FLOAT,
                    total_volume FLOAT,
                    volume_marketcap_ratio FLOAT,
                    distance_from_ath_pct FLOAT,
                    last_updated TIMESTAMP
                )
            """))

           
            conn.execute(text("""
                DELETE FROM fact_crypto_price
                WHERE DATE(last_updated) = CURRENT_DATE
            """))

        df.write_database(
            table_name="fact_crypto_price",
            connection=engine,
            if_table_exists="append"
        )

        logger.info("fact_crypto_price loaded successfully")

    except Exception as e:
        logger.error(f"Error loading fact table: {e}")
        raise