import polars as pl
from pathlib import Path
import sys
import json

Path("../data/transformed_dump").mkdir(parents=True, exist_ok=True)

def load_data(file_path:str | Path) -> pl.DataFrame:
    
    """
    Function load_data() takes json data dump from data extraction and return polars DataFrame.
    """
    path = Path(file_path)
    
    try:
        df = pl.read_json(path)
        return df
    except FileNotFoundError:
        print(f"File {path} not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error decoding JSON from the file")
        sys.exit(1)
        
def transform_data(df: pl.DataFrame) -> pl.DataFrame:
    """
        Transforms raw crypto market data:
        - drops unnecessary columns
        - renames fields
        - converts timestamps
        - derives analytics metrics
    """
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
    
    return df
