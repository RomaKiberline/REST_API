import time
from fastapi import Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from redis_config import get_redis_client, RATE_LIMITS
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    password: Optional[str] = None

async def rate_limit(request: Request, user: Optional[User] = None):
    """
    Rate limiter using sliding time window approach.
    
    Args:
        request: FastAPI Request object
        user: Optional authenticated user
        
    Raises:
        HTTPException: If rate limit is exceeded (429)
    """
    r = await get_redis_client()
    
    if user:
        identity = user.username
        limit_type = "authenticated"
    else:
        identity = request.client.host
        limit_type = "anonymous"
    
    limit_config = RATE_LIMITS[limit_type]
    limit = limit_config["limit"]
    period = limit_config["period"]
    
    key = f"rate_limit_{identity}"
    
    now = int(time.time())
    window_start = now - period
    
    await r.zremrangebyscore(key, min=0, max=window_start)
    
    request_count = await r.zcard(key)
    
    if request_count >= limit:
        raise HTTPException(
            status_code=429,
            detail="Too many requests",
            headers={"Retry-After": str(period)}
        )
    
    await r.zadd(key, {str(now): now})
    
    await r.expire(key, period)

async def get_current_user_optional(token: str = Depends(oauth2_scheme)):
    """Get current user if token is provided, otherwise None."""
    if not token:
        return None
    
    try:
        from main import verify_token, get_user, fake_users_db
        
        token_data = verify_token(token, "access")
        if token_data is None:
            return None
        
        user = get_user(fake_users_db, token_data.username)
        return user
    except:
        return None
