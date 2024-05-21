# FastAPI and Redis

This repository contains a tutorial on setting up a FastAPI application with Redis, using `pydanticV2`, `functools.lru_cache`, `Depends`

## Features

- FastAPI for building the web API
- Redis for caching and data storage
- Pydantic v2 for configuration management
- LRU Cache for efficient connection handling
- Depends for injecting dependencies into route function



## Configuration

Configuration settings are managed using `pydantic` v2. All settings are defined in `config.py`.

### Example `config.py`:

```python
from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    redis_host: str = "redis cloud server"
    redis_port: int = 12345

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    """
    Function to get the application settings using Pydantic.
    
    This function uses functools.lru_cache to cache the settings object,
    ensuring that the settings are loaded only once and subsequent calls 
    return the cached settings without recomputation.
    
    Returns:
        Settings: The application settings.
    """
    return Settings()
```

## Depends:

In FastAPI, Depends is a mechanism used for injecting dependencies into route functions. When a route function requires certain resources or objects to execute, Depends ensures those dependencies are resolved before the function is invoked.

In our application, `Depends(get_redis)` refers to a dependency declaration where `get_redis` is a function responsible for creating and returning a Redis client instance. This dependency ensures that the Redis client is available to the route function before it's executed.


