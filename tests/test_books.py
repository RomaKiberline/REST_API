import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

# Patch database before importing app
with patch('database.create_engine'), \
     patch('database.SessionLocal'), \
     patch('database.get_db'):
    from main import app
    from schemas.book import BookStatus

client = TestClient(app)


class TestBookEndpoints:
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()

    def test_create_book(self):
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "description": "Test Description",
            "year": 2023,
            "status": "available"
        }
        
        with patch('services.book_service.BookService') as mock_service:
            mock_instance = mock_service.return_value
            mock_instance.create_book.return_value = {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Test Book",
                "author": "Test Author",
                "description": "Test Description",
                "year": 2023,
                "status": "available",
                "created_at": "2023-01-01T00:00:00Z"
            }
            
            response = client.post("/books/", json=book_data)
            assert response.status_code == 201
            data = response.json()
            assert data["title"] == "Test Book"
            assert data["author"] == "Test Author"
            assert "id" in data

    def test_get_all_books_empty(self):
        with patch('services.book_service.BookService') as mock_service:
            mock_instance = mock_service.return_value
            mock_instance.get_all_books_cursor.return_value = {
                "books": [],
                "next_cursor": None,
                "has_next": False,
                "limit": 100
            }
            
            response = client.get("/books/")
            assert response.status_code == 200
            
            data = response.json()
            assert data["books"] == []
            assert data["next_cursor"] is None
            assert data["has_next"] is False
            assert data["limit"] == 100

    def test_cursor_pagination(self):
        with patch('services.book_service.BookService') as mock_service_class:
            mock_service = mock_service_class.return_value
            mock_service.get_all_books_cursor.return_value = {
                "books": [
                    {"id": "550e8400-e29b-41d4-a716-446655440000", "title": "Book 1", "author": "Author 1", "year": 2023, "status": "available", "description": None, "created_at": "2023-01-01T00:00:00Z"},
                    {"id": "550e8400-e29b-41d4-a716-446655440001", "title": "Book 2", "author": "Author 2", "year": 2023, "status": "available", "description": None, "created_at": "2023-01-02T00:00:00Z"}
                ],
                "next_cursor": "550e8400-e29b-41d4-a716-446655440001",
                "has_next": True,
                "limit": 2
            }
            
            response = client.get("/books/?limit=2")
            assert response.status_code == 200
            data = response.json()
            assert len(data["books"]) == 2
            assert data["limit"] == 2
            assert data["next_cursor"] == "550e8400-e29b-41d4-a716-446655440001"
            assert data["has_next"] is True

    def test_cursor_pagination_with_cursor(self):
        with patch('services.book_service.BookService') as mock_service_class:
            mock_service = mock_service_class.return_value
            mock_service.get_all_books_cursor.return_value = {
                "books": [
                    {"id": "550e8400-e29b-41d4-a716-446655440002", "title": "Book 3", "author": "Author 3", "year": 2023, "status": "available", "description": None, "created_at": "2023-01-03T00:00:00Z"}
                ],
                "next_cursor": None,
                "has_next": False,
                "limit": 2
            }
            
            response = client.get("/books/?limit=2&cursor=550e8400-e29b-41d4-a716-446655440001")
            assert response.status_code == 200
            data = response.json()
            assert len(data["books"]) == 1
            assert data["next_cursor"] is None
            assert data["has_next"] is False

    def test_get_book_by_id(self):
        with patch('services.book_service.BookService') as mock_service:
            mock_instance = mock_service.return_value
            mock_instance.get_book_by_id.return_value = {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Test Book",
                "author": "Test Author",
                "year": 2023,
                "status": "available",
                "description": "Test Description",
                "created_at": "2023-01-01T00:00:00Z"
            }
            
            response = client.get("/books/550e8400-e29b-41d4-a716-446655440000")
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "550e8400-e29b-41d4-a716-446655440000"
            assert data["title"] == "Test Book"

    def test_delete_book(self):
        with patch('services.book_service.BookService') as mock_service:
            mock_instance = mock_service.return_value
            mock_instance.delete_book.return_value = True
            
            response = client.delete("/books/550e8400-e29b-41d4-a716-446655440000")
            assert response.status_code == 204

class TestRootEndpoint:
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data
