import polars as pl
import sys
from config import Config


def load_data_to_database(df: pl.DataFrame, table_name: str):
    
    try:
        df.write_database(table_name=table_name,connection=Config.DB_URL, if_table_exists="append", engine='sqlalchemy') # type: ignore
    except Exception as e:
        print(f"Error while loading data to postgres: {e}")
        sys.exit(1)
