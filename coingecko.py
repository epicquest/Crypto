import requests
import os
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
COINGECKO_API_URL = os.getenv("COINGECKO_API_URL")
CURRENCY = "usd"
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)


def fetch_crypto_info(symbol: str):
    cache_key = f"crypto:{symbol}"
    cached_data = redis_client.get(cache_key)

    if cached_data:
        return eval(cached_data)

    response = requests.get(f"{COINGECKO_API_URL}/markets", params={"vs_currency": CURRENCY})

    if response.status_code == 200:
        for coin in response.json():
            if coin["symbol"].lower() == symbol.lower():
                redis_client.set(cache_key, str(coin), ex=3600)
                return coin
    return None


def fetch_crypto_prices(symbols: list[str]) -> dict[str, float]:
    """Fetch updated crypto prices from CoinGecko."""
    response = requests.get(f"{COINGECKO_API_URL}/markets", params={"vs_currency": CURRENCY})

    if response.status_code != 200:
        return {}

    prices = {}
    for coin in response.json():
        symbol = coin["symbol"].lower()
        if symbol in symbols:
            prices[symbol] = coin["current_price"]
            redis_client.set(f"crypto:{symbol}", str(coin), ex=3600)  # Cache results

    return prices