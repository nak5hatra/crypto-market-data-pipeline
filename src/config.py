import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
    DB_URL = os.getenv('DB_URL')
    CRYPTO_TABLE = os.getenv('CRYPTO_TABLE')