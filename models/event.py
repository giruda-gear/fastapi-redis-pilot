from redis_om import HashModel
from redis_connection import get_redis


class Event(HashModel):
    delivery_id: str = None
    type: str
    data: str

    class Meta:
        database = get_redis()
