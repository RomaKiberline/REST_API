import pytest
import time
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from main import app
from redis_config import RATE_LIMITS

client = TestClient(app)

class TestRateLimiter:
    """Test rate limiter functionality."""
    
    @pytest.mark.asyncio
    async def test_anonymous_user_within_limit(self):
        """Test anonymous user within rate limit - should return 200."""
        with patch('rate_limiter.get_redis_client') as mock_redis:
            mock_client = AsyncMock()
            mock_redis.return_value = mock_client
            
            mock_client.zremrangebyscore.return_value = 0
            mock_client.zcard.return_value = 1 
            mock_client.zadd.return_value = 1
            mock_client.expire.return_value = 1
            
            response = client.get("/")
            
            assert response.status_code == 200
            assert "message" in response.json()
    
    @pytest.mark.asyncio
    async def test_anonymous_user_exceeds_limit(self):
        """Test anonymous user exceeding rate limit - should return 429."""
        with patch('rate_limiter.get_redis_client') as mock_redis:
            mock_client = AsyncMock()
            mock_redis.return_value = mock_client
            
            mock_client.zremrangebyscore.return_value = 0
            mock_client.zcard.return_value = 2
            
            response = client.get("/")
            
            assert response.status_code == 429
            assert "Too many requests" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_authenticated_user_within_limit(self):
        """Test authenticated user within rate limit - should return 200."""
        with patch('rate_limiter.get_redis_client') as mock_redis:
            mock_client = AsyncMock()
            mock_redis.return_value = mock_client
            
            mock_client.zremrangebyscore.return_value = 0
            mock_client.zcard.return_value = 5
            mock_client.zadd.return_value = 1
            mock_client.expire.return_value = 1
            
            with patch('main.rate_limit') as mock_rate_limit:
                mock_rate_limit.return_value = None
                
                login_response = client.post("/token", data={
                    "username": "johndoe",
                    "password": "secret"
                })
                token = login_response.json()["access_token"]
                
                response = client.get("/books", headers={
                    "Authorization": f"Bearer {token}"
                })
                
                assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_authenticated_user_exceeds_limit(self):
        """Test authenticated user exceeding rate limit - should return 429."""
        with patch('main.rate_limit') as mock_login_rate_limit:
            mock_login_rate_limit.return_value = None
            
            login_response = client.post("/token", data={
                "username": "johndoe",
                "password": "secret"
            })
            token = login_response.json()["access_token"]
        
        with patch('rate_limiter.get_redis_client') as mock_redis:
            mock_client = AsyncMock()
            mock_redis.return_value = mock_client
            
            mock_client.zremrangebyscore.return_value = 0
            mock_client.zcard.return_value = 10
            
            response = client.get("/books", headers={
                "Authorization": f"Bearer {token}"
            })
            
            assert response.status_code == 429
            assert "Too many requests" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_rate_limit_configuration(self):
        """Test that rate limit configuration is correct."""
        assert "anonymous" in RATE_LIMITS
        assert "authenticated" in RATE_LIMITS
        assert RATE_LIMITS["anonymous"]["limit"] == 2
        assert RATE_LIMITS["anonymous"]["period"] == 60
        assert RATE_LIMITS["authenticated"]["limit"] == 10
        assert RATE_LIMITS["authenticated"]["period"] == 60
    
    @pytest.mark.asyncio
    async def test_sliding_window_cleanup(self):
        """Test that old entries are cleaned up from sliding window."""
        with patch('rate_limiter.get_redis_client') as mock_redis:
            mock_client = AsyncMock()
            mock_redis.return_value = mock_client
            
            mock_client.zremrangebyscore.return_value = 5
            mock_client.zcard.return_value = 1
            mock_client.zadd.return_value = 1
            mock_client.expire.return_value = 1
            
            response = client.get("/")
            
            mock_client.zremrangebyscore.assert_called_once()
            
            assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_health_check_no_rate_limit(self):
        """Test that health check endpoint has no rate limiting."""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
