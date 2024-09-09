import redis
from config import REDIS_HOST

class Redis_Cache:
    def __init__(self):
        self.redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0)

    def get_cached_price(self, product_title: str) -> float:
        cached_price = self.redis_client.get(product_title)
        return float(cached_price) if cached_price else None

    def set_cached_price(self, product_title: str, product_price: float):
        self.redis_client.set(product_title, product_price)

cache = Redis_Cache()
