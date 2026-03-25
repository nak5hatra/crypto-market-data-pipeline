import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
    DB_URL = os.getenv("DB_URL")
    CRYPTO_TABLE = os.getenv("CRYPTO_TABLE")

    if not COINGECKO_API_KEY:
        raise ValueError("COINGECKO_API_KEY is missing")

    if not DB_URL:
        raise ValueError("DB_URL is missing")