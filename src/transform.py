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
    df = df.drop('image', 'roi', strict=True)
    df = df.fill_null(0)
    
    columns_mapping = {
    "id": "coin_id",
    "symbol": "coin_symbol",
    "name": "coin_name",
    "current_price": "price_usd",
    "price_change_percentage_24h": "price_change_pct_24h",
    "price_change_percentage_1h_in_currency": "price_change_pct_1h"
    }
    
    df = df.rename(mapping=columns_mapping, strict=True)
    
    
    df = df.with_columns(
        df["atl_date"].str.to_datetime(),       # Convert Columns to DataTime
        df["ath_date"].str.to_datetime(),       # Convert Columns to DataTime
        df["last_updated"].str.to_datetime(),   # Convert Columns to DataTime
        (pl.col("total_volume") / pl.col("market_cap")).fill_nan(0).alias("volume_marketcap_ratio"),    # Calculate market dominance proxy
        (100 - abs(pl.col("ath_change_percentage"))).alias("distance_from_ath_pct"),   # Distance from ATH(all time high)
        pl.col("coin_symbol").str.to_uppercase()    # Convert coin symbol to uppercase
    )
    output_path = Path("../data/transformed_dump/transformed_market_data.parquet")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet(output_path)
    
    return str(output_path)
