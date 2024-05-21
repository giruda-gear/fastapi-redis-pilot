from redis_om import HashModel
from redis_connection import get_redis


class Devlivery(HashModel):
    budget: int = 0
    notes: str = ""

    class Meta:
        database = get_redis()
