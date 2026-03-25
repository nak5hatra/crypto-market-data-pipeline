from pathlib import Path
import requests
import json
import time
from config import Config
from utils import chunk_list, get_logger

logger = get_logger()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)

COIN_LIST_PATH = DATA_DIR / "coin_list.json"
MARKET_DATA_PATH = DATA_DIR / "market_data.json"

headers = {"x-cg-demo-api-key": Config.COINGECKO_API_KEY}


def fetch_coin_data():
    url = "https://api.coingecko.com/api/v3/coins/list?include_platform=false"

    try:
        logger.info("Fetching coin list...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        with open(COIN_LIST_PATH, "w") as f:
            json.dump(data, f)

        logger.info("Coin list saved successfully")
        return str(COIN_LIST_PATH)

    except Exception as e:
        logger.error(f"Error fetching coin data: {e}")
        raise


def fetch_market_data():
    try:
        logger.info("Loading coin list...")
        with open(COIN_LIST_PATH) as f:
            coin_data = json.load(f)

        list_of_ids = [coin["id"] for coin in coin_data]
        market_data = []

        for batch in chunk_list(list_of_ids, 100):
            coin_ids_str = ",".join(batch)
            url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={coin_ids_str}"

            for attempt in range(3):
                response = requests.get(url, headers=headers, timeout=10)

                if response.status_code == 429:
                    time.sleep(2 ** attempt)
                    continue

                response.raise_for_status()
                data = response.json()

                if not isinstance(data, list):
                    raise ValueError("Invalid API response")

                market_data.extend(data)
                break

        with open(MARKET_DATA_PATH, "w") as f:
            json.dump(market_data, f)

        logger.info("Market data saved successfully")
        return str(MARKET_DATA_PATH)

    except Exception as e:
        logger.error(f"Error fetching market data: {e}")
        raise