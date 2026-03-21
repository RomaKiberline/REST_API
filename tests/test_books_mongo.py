import pytest
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from main import app
from mongodb.client import MongoDB
from schemas.book_mongo import BookStatus

# Mock MongoDB client
@pytest.fixture
def mock_mongo_client():
    """Mock MongoDB client for testing"""
    with patch('mongodb.client.AsyncIOMotorClient') as mock_client:
        mock_db = MagicMock()
        mock_client.return_value.database = mock_db
        
        # Mock collection
        mock_collection = AsyncMock()
        mock_db.books = mock_collection
        
        # Mock indexes
        mock_collection.create_index = AsyncMock()
        
        yield mock_collection

@pytest.fixture
def client(mock_mongo_client):
    """Test client with mocked MongoDB"""
    with patch('mongodb.client.MongoDB.get_database') as mock_get_db:
        mock_db = MagicMock()
        mock_db.books = mock_mongo_client
        mock_get_db.return_value = mock_db
        
        with TestClient(app) as test_client:
            yield test_client

@pytest.fixture
def sample_book():
    """Sample book data for testing"""
    return {
        "title": "Test Book",
        "author": "Test Author",
        "description": "Test Description",
        "status": "available",
        "year": 2023
    }

@pytest.fixture
def sample_book_response():
    """Sample book response from MongoDB"""
    return {
        "_id": "507f1f77bcf86cd799439011",
        "title": "Test Book",
        "author": "Test Author",
        "description": "Test Description",
        "status": "available",
        "year": 2023,
        "created_at": "2023-01-01T00:00:00"
    }

class TestBookMongoAPI:
    """Test cases for MongoDB Book API"""

    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert "Library API with MongoDB" in response.json()["message"]

    @pytest.mark.asyncio
    async def test_create_book(self, client, sample_book, sample_book_response, mock_mongo_client):
        """Test book creation"""
        # Mock insert_one
        mock_result = AsyncMock()
        mock_result.inserted_id = "507f1f77bcf86cd799439011"
        mock_mongo_client.insert_one.return_value = mock_result
        
        # Mock find_one for response
        mock_mongo_client.find_one.return_value = sample_book_response
        
        response = client.post("/books/", json=sample_book)
        assert response.status_code == 201
        
        data = response.json()
        assert data["title"] == sample_book["title"]
        assert data["author"] == sample_book["author"]
        assert data["status"] == sample_book["status"]

    @pytest.mark.asyncio
    async def test_get_all_books(self, client, sample_book_response, mock_mongo_client):
        """Test getting all books"""
        # Mock find cursor
        mock_cursor = AsyncMock()
        mock_cursor.__aiter__ = AsyncMock(return_value=iter([sample_book_response]))
        mock_mongo_client.find.return_value = mock_cursor
        
        # Mock count_documents
        mock_mongo_client.count_documents.return_value = 1
        
        response = client.get("/books/")
        assert response.status_code == 200
        
        data = response.json()
        assert "books" in data
        assert data["total"] == 1
        assert len(data["books"]) == 1

    @pytest.mark.asyncio
    async def test_get_book_by_id(self, client, sample_book_response, mock_mongo_client):
        """Test getting book by ID"""
        mock_mongo_client.find_one.return_value = sample_book_response
        
        response = client.get("/books/507f1f77bcf86cd799439011")
        assert response.status_code == 200
        
        data = response.json()
        assert data["title"] == sample_book_response["title"]
        assert data["id"] == "507f1f77bcf86cd799439011"

    @pytest.mark.asyncio
    async def test_get_book_not_found(self, client, mock_mongo_client):
        """Test getting non-existent book"""
        mock_mongo_client.find_one.return_value = None
        
        response = client.get("/books/507f1f77bcf86cd799439011")
        assert response.status_code == 404
        assert "Book not found" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_update_book(self, client, sample_book_response, mock_mongo_client):
        """Test updating a book"""
        # Mock find_one for existing book
        mock_mongo_client.find_one.return_value = sample_book_response
        
        # Mock update_one
        mock_mongo_client.update_one.return_value = None
        
        update_data = {"title": "Updated Book Title"}
        response = client.put("/books/507f1f77bcf86cd799439011", json=update_data)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_delete_book(self, client, mock_mongo_client):
        """Test deleting a book"""
        # Mock delete_one
        mock_result = AsyncMock()
        mock_result.deleted_count = 1
        mock_mongo_client.delete_one.return_value = mock_result
        
        response = client.delete("/books/507f1f77bcf86cd799439011")
        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_delete_book_not_found(self, client, mock_mongo_client):
        """Test deleting non-existent book"""
        # Mock delete_one
        mock_result = AsyncMock()
        mock_result.deleted_count = 0
        mock_mongo_client.delete_one.return_value = mock_result
        
        response = client.delete("/books/507f1f77bcf86cd799439011")
        assert response.status_code == 404
        assert "Book not found" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_pagination(self, client, sample_book_response, mock_mongo_client):
        """Test pagination functionality"""
        # Mock find cursor with multiple books
        mock_cursor = AsyncMock()
        mock_cursor.__aiter__ = AsyncMock(return_value=iter([sample_book_response] * 2))
        mock_mongo_client.find.return_value = mock_cursor
        
        # Mock count_documents
        mock_mongo_client.count_documents.return_value = 25
        
        response = client.get("/books/?limit=10&offset=5")
        assert response.status_code == 200
        
        data = response.json()
        assert data["limit"] == 10
        assert data["offset"] == 5
        assert data["has_next"] is True
        assert data["has_prev"] is True

    @pytest.mark.asyncio
    async def test_filtering(self, client, sample_book_response, mock_mongo_client):
        """Test filtering functionality"""
        # Mock find cursor
        mock_cursor = AsyncMock()
        mock_cursor.__aiter__ = AsyncMock(return_value=iter([sample_book_response]))
        mock_mongo_client.find.return_value = mock_cursor
        
        # Mock count_documents
        mock_mongo_client.count_documents.return_value = 1
        
        response = client.get("/books/?status=available&author=Test")
        assert response.status_code == 200
        
        # Verify the query was called with correct filters
        mock_mongo_client.find.assert_called_once()
        call_args = mock_mongo_client.find.call_args[0][0]
        assert "status" in call_args
        assert "author" in call_args

    @pytest.mark.asyncio
    async def test_sorting(self, client, sample_book_response, mock_mongo_client):
        """Test sorting functionality"""
        # Mock find cursor
        mock_cursor = AsyncMock()
        mock_cursor.__aiter__ = AsyncMock(return_value=iter([sample_book_response]))
        mock_mongo_client.find.return_value = mock_cursor
        
        # Mock count_documents
        mock_mongo_client.count_documents.return_value = 1
        
        response = client.get("/books/?sort_by=year&ascending=false")
        assert response.status_code == 200
        
        # Verify sort was called
        mock_mongo_client.find.return_value.sort.assert_called_once()

    def test_invalid_sort_field(self, client):
        """Test validation of sort field"""
        response = client.get("/books/?sort_by=invalid_field")
        assert response.status_code == 400
        assert "sort_by must be one of" in response.json()["detail"]

if __name__ == "__main__":
    pytest.main([__file__])
