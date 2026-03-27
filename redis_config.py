import redis.asyncio as redis
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = "" 
    
    class Config:
        env_file = ".env"

settings = Settings()

RATE_LIMITS = {
    "anonymous": {"limit": 2, "period": 60},  
    "authenticated": {"limit": 10, "period": 60}  
}

async def get_redis_client():
    """Get Redis client connection."""
    return redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
        password=settings.redis_password,
        decode_responses=True
    )
