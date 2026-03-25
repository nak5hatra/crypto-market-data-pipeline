import polars as pl
from pathlib import Path
from utils import get_logger

logger = get_logger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
STAGING_DIR = BASE_DIR / "data" / "staging"
STAGING_DIR.mkdir(parents=True, exist_ok=True)


def transform_data(file_path: str) -> dict:

    try:
        logger.info("Reading raw data...")
        df = pl.read_json(file_path)

        if df.is_empty():
            raise ValueError("Input data is empty")

        df = df.fill_null(0)

        
        columns_mapping = {
            "id": "coin_id",
            "symbol": "coin_symbol",
            "name": "coin_name",
            "current_price": "price_usd",
        }

        df = df.rename(columns_mapping)

        
        logger.info("Applying transformations...")

        df = df.with_columns(
            df["last_updated"].str.to_datetime().alias("last_updated"),
            (pl.col("total_volume") / pl.col("market_cap"))
            .fill_nan(0)
            .fill_null(0)
            .alias("volume_marketcap_ratio"),
            (100 - abs(pl.col("ath_change_percentage")))
            .alias("distance_from_ath_pct"),
            pl.col("coin_symbol").str.to_uppercase()
        )

        
        cols_to_drop = [
            "image",
            "fully_diluted_valuation",
            "high_24h",
            "low_24h",
            "price_change_24h",
            "price_change_percentage_24h",
            "market_cap_change_24h",
            "market_cap_change_percentage_24h",
            "total_supply",
            "ath",
            "ath_change_percentage",
            "ath_date",
            "atl",
            "atl_change_percentage",
            "atl_date",
            "roi",
            "price_change_percentage_1h_in_currency"
        ]

        existing_cols_to_drop = [col for col in cols_to_drop if col in df.columns]
        df = df.drop(existing_cols_to_drop)

        df = (
            df.drop_nulls(subset="market_cap")
            .sort("market_cap", descending=True)
            .top_k(500, by="market_cap")
        )
        
        dim_coin = (
            df.select(["coin_id", "coin_symbol", "coin_name"])
            .unique()
        )

        dim_path = STAGING_DIR / "dim_coin.parquet"
        dim_coin.write_parquet(dim_path)

        fact_table = df.select([
            "coin_id",
            "price_usd",
            "market_cap",
            "total_volume",
            "volume_marketcap_ratio",
            "distance_from_ath_pct",
            "last_updated"
        ])

        fact_path = STAGING_DIR / "fact_crypto_price.parquet"
        fact_table.write_parquet(fact_path)

        logger.info("Transformation completed successfully")

        return {
            "dim_coin": str(dim_path),
            "fact_crypto": str(fact_path)
        }

    except Exception as e:
        logger.error(f"Transformation failed: {e}")
        raise