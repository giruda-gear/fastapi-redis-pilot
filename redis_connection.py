from redis_om import get_redis_connection
from config import get_settings
from functools import lru_cache


@lru_cache
def get_redis():
    settings = get_settings()
    
    return get_redis_connection(
        host=settings.redis_host,
        port=settings.redis_port,
        password=settings.redis_password,
        decode_responses=True,
    ) 
