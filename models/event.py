import redis
from redis_om import HashModel


class Event(HashModel):
    delivery_id: str = None
    type: str
    data: str

    class Meta:
        database = redis
