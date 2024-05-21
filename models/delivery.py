import redis
from redis_om import HashModel


class Devlivery(HashModel):
    budget: int = 0
    notes: str = ""

    class Meta:
        database = redis
