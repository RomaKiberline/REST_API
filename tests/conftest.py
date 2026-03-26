import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture(scope="session")
def client():
    """Create test client for the app."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def auth_headers(client):
    """Get authentication headers for protected endpoints."""
    response = client.post("/token", data={
        "username": "johndoe",
        "password": "secret"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def sample_book():
    """Sample book data for testing."""
    return {
        "title": "Test Book",
        "author": "Test Author",
        "description": "Test Description",
        "year": 2024,
        "status": "available"
    }
