import polars as pl
from pathlib import Path


Path("../data/transformed_dump").mkdir(parents=True, exist_ok=True)
        
def transform_data(file_path: str) -> str:
    """
        Transforms raw crypto market data:
        - drops unnecessary columns
        - renames fields
        - converts timestamps
        - derives analytics metrics
    """
    df = pl.read_json(file_path)
    df = df.fill_null(0)
    
    columns_mapping = {
    "id": "coin_id",
    "symbol": "coin_symbol",
    "name": "coin_name",
    "current_price": "price_usd",
    }
    
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
    
    df = df.rename(mapping=columns_mapping)
    
    
    df = df.with_columns(
        df["last_updated"].str.to_datetime(),   # Convert Columns to DataTime
        (pl.col("total_volume") / pl.col("market_cap")).fill_nan(0).fill_null(0).alias("volume_marketcap_ratio"),    # Calculate market dominance proxy
        (100 - abs(pl.col("ath_change_percentage"))).alias("distance_from_ath_pct"),   # Distance from ATH(all time high)
        pl.col("coin_symbol").str.to_uppercase()    # Convert coin symbol to uppercase
    )
    
    df = df.drop(cols_to_drop)
    df = df.drop_nulls(subset="market_cap").sort(by="market_cap", descending=True).top_k(k=500, by="market_cap")    # keeping only 500 crypto by largest Market cap.
    output_path = Path("../data/transformed_dump/transformed_market_data.parquet")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet(output_path)
    
    return str(output_path)
