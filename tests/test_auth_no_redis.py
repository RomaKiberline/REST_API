import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

client = TestClient(__import__('main').app)

def test_root_endpoint():
    """Test root endpoint (public)."""
    with patch('main.rate_limit') as mock_rate_limit:
        mock_rate_limit.return_value = None
        
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "JWT Authentication" in data["message"]

def test_health_endpoint():
    """Test health check endpoint (public)."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_login_success():
    """Test successful login."""
    with patch('main.rate_limit') as mock_rate_limit:
        mock_rate_limit.return_value = None
        
        response = client.post("/token", data={
            "username": "johndoe",
            "password": "secret"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

def test_login_invalid_credentials():
    """Test login with invalid credentials."""
    with patch('main.rate_limit') as mock_rate_limit:
        mock_rate_limit.return_value = None
        
        response = client.post("/token", data={
            "username": "johndoe",
            "password": "wrongpassword"
        })
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

def test_protected_books_without_token():
    """Test accessing books endpoint without token."""
    response = client.get("/books")
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]

def test_protected_books_with_token():
    """Test accessing books endpoint with valid token."""
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
        books = response.json()
        assert isinstance(books, list)
        assert len(books) > 0

def test_create_book_with_token():
    """Test creating a new book with authentication."""
    with patch('main.rate_limit') as mock_rate_limit:
        mock_rate_limit.return_value = None
        
        login_response = client.post("/token", data={
            "username": "johndoe",
            "password": "secret"
        })
        token = login_response.json()["access_token"]
        
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "description": "Test Description",
            "year": 2024,
            "status": "available"
        }
        response = client.post("/books", json=book_data, headers={
            "Authorization": f"Bearer {token}"
        })
        assert response.status_code == 200
        book = response.json()
        assert book["title"] == "Test Book"
        assert book["author"] == "Test Author"

def test_get_user_info():
    """Test getting current user info."""
    with patch('main.rate_limit') as mock_rate_limit:
        mock_rate_limit.return_value = None
        
        login_response = client.post("/token", data={
            "username": "johndoe",
            "password": "secret"
        })
        token = login_response.json()["access_token"]
        
        response = client.get("/users/me", headers={
            "Authorization": f"Bearer {token}"
        })
        assert response.status_code == 200
        user = response.json()
        assert user["username"] == "johndoe"
        assert user["email"] == "johndoe@example.com"
