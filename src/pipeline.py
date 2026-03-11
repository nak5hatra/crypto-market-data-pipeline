from extract import fetch_coin_data, fetch_market_data  # type: ignore
from transform import load_data, transform_data
from load import load_data_to_database
from pathlib import Path

RAW_DATA_PATH = Path("../data/extraction_dumps/market_data.json")
TABLE_NAME = 'crypto_market'
if __name__ == "__main__":
    try:
        print('fetching coin list...')
        coin_list_data = fetch_coin_data() # type: ignore
        
        print('coin list fetch completed...')
        print('fetching crypto market data...')
        fetch_market_data(coin_list_data) # type: ignore
        
        print('crypto market data fetched...')
        print('loading raw crypto market data for transformation...')
        data = load_data(file_path=RAW_DATA_PATH)
        
        print("data loaded successfully...")
        print("transforming raw data...")
        transform_market_data = transform_data(data)
        
        print('data transformation is completed...')
        print('loading data to postgres Database...')
        load_data_to_database(transform_market_data, table_name=TABLE_NAME) # type: ignore
        
        print("data loaded to postgres database successfully...")
        print("Pipeline task successfully completed...")
        
        
    except Exception as e:
        print(f"Pipeline failed: {e}")