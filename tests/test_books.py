import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

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
                "id": "test-uuid",
                "title": "Test Book",
                "author": "Test Author",
                "description": "Test Description",
                "year": 2023,
                "status": "available"
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
            mock_instance.get_all_books.return_value = {
                "books": [],
                "total": 0,
                "limit": 100,
                "offset": 0,
                "has_next": False,
                "has_prev": False
            }
            
            response = client.get("/books/")
            assert response.status_code == 200
            
            data = response.json()
            assert data["books"] == []
            assert data["total"] == 0
            assert data["limit"] == 100
            assert data["offset"] == 0
            assert data["has_next"] is False
            assert data["has_prev"] is False

    def test_pagination(self):
        with patch('services.book_service.BookService') as mock_service:
            mock_instance = mock_service.return_value
            
            # Mock first page
            mock_instance.get_all_books.return_value = {
                "books": [
                    {"id": "1", "title": "Book 1", "author": "Author 1", "year": 2023, "status": "available", "description": None},
                    {"id": "2", "title": "Book 2", "author": "Author 2", "year": 2023, "status": "available", "description": None}
                ],
                "total": 5,
                "limit": 2,
                "offset": 0,
                "has_next": True,
                "has_prev": False
            }
            
            response = client.get("/books/?limit=2&offset=0")
            assert response.status_code == 200
            data = response.json()
            assert len(data["books"]) == 2
            assert data["limit"] == 2
            assert data["offset"] == 0
            assert data["has_next"] is True
            assert data["has_prev"] is False

    def test_get_book_by_id(self):
        with patch('services.book_service.BookService') as mock_service:
            mock_instance = mock_service.return_value
            mock_instance.get_book_by_id.return_value = {
                "id": "test-uuid",
                "title": "Test Book",
                "author": "Test Author",
                "year": 2023,
                "status": "available",
                "description": "Test Description"
            }
            
            response = client.get("/books/test-uuid")
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "test-uuid"
            assert data["title"] == "Test Book"

    def test_delete_book(self):
        with patch('services.book_service.BookService') as mock_service:
            mock_instance = mock_service.return_value
            mock_instance.delete_book.return_value = True
            
            response = client.delete("/books/test-uuid")
            assert response.status_code == 204

class TestRootEndpoint:
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data
