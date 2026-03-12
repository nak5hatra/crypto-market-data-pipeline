import polars as pl
import sys
from config import Config


def load_data_to_database(file_path: str, table_name: str):
    """
    Load a Polars DataFrame into a PostgreSQL table.

    Args:
        df (pl.DataFrame): Transformed data to be inserted into the database.
        table_name (str): Name of the target table in PostgreSQL.
    """
    
    try:
        df = pl.read_parquet(file_path)
        df.write_database(table_name=table_name,connection=Config.DB_URL, if_table_exists="append", engine='sqlalchemy') # type: ignore
    except Exception as e:
        print(f"Error while loading data to postgres: {e}")
        sys.exit(1)
