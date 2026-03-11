import sys
import os
sys.path.append(os.path.abspath(".."))
import requests
import json
from config import Config
from utils import chunk_list # type: ignore
import time
from pathlib import Path

Path("../data/extraction_dumps").mkdir(parents=True, exist_ok=True)

headers = {"x-cg-demo-api-key": Config.COINGECKO_API_KEY}

def fetch_coin_data() -> list[dict]: # type: ignore
    
    """
    fetch list of coins available on COINGECKO platform.
    
    Returns:
        dict: coin list with all the metadata related to coins from COINGECKO.
    """
    
    url = "https://api.coingecko.com/api/v3/coins/list?include_platform=false"
    
    
    
    try:
        response = requests.get(url=url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        with open("../data/extraction_dumps/coin_list.json", "w")  as file:
            json.dump(data, file, indent=4)
            
        return data
    # Dump coin_list_data in coin_list.json
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"An Error Occurred: {e}")
        sys.exit(1)

def fetch_market_data(coin_data:dict) -> list[dict]: # type: ignore
    """
    fetch all coin market data available on COINGECKO platform using the coin ids from `coin data` dict.

    Args:
        coin_data (dict): using this dict to get all the ids of markets

    Returns:
        dict: returns data of all markets in COINGECKO
    """
    list_of_ids = [coin["id"] for coin in coin_data] # type: ignore ## Only 1000 coin details
    
    market_data = []
    try:
        for batch in chunk_list(list_of_ids, 50): # type: ignore
            coin_ids_str = ",".join(batch) # type: ignore
            url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={coin_ids_str}&price_change_percentage=1h"
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 429:
                time.sleep(1)
                continue
            response.raise_for_status()
            market_data.extend(response.json()) # type: ignore
            
        # Dump market_data in market_data.json
        with open("../data/extraction_dumps/market_data.json", "w")  as file:
            json.dump(market_data, file, indent=4)
        return market_data # type: ignore
    
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"An Error Occurred: {e}")
        sys.exit(1)
