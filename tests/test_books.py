import pytest
from fastapi.testclient import TestClient
from uuid import uuid4

from main import app
from schemas.book import BookStatus


client = TestClient(app)


@pytest.fixture
def sample_book():
    return {
        "title": "Test Book",
        "author": "Test Author",
        "description": "A test book description",
        "year": 2023,
        "status": "available"
    }


@pytest.fixture(autouse=True)
def clear_books():
    """Clear all books before each test"""
    response = client.get("/books/")
    if response.status_code == 200:
        books = response.json()
        for book in books:
            client.delete(f"/books/{book['id']}")


@pytest.fixture
def created_book(sample_book):
    response = client.post("/books/", json=sample_book)
    return response.json()


class TestBookEndpoints:
    
    def test_create_book(self, sample_book):
        response = client.post("/books/", json=sample_book)
        assert response.status_code == 201
        
        data = response.json()
        assert data["title"] == sample_book["title"]
        assert data["author"] == sample_book["author"]
        assert data["description"] == sample_book["description"]
        assert data["year"] == sample_book["year"]
        assert data["status"] == sample_book["status"]
        assert "id" in data
    
    def test_create_book_minimal_data(self):
        book_data = {
            "title": "Minimal Book",
            "author": "Minimal Author",
            "year": 2023
        }
        response = client.post("/books/", json=book_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["title"] == book_data["title"]
        assert data["author"] == book_data["author"]
        assert data["year"] == book_data["year"]
        assert data["status"] == "available"  # Default value
        assert data["description"] is None
    
    def test_create_book_invalid_data(self):
        invalid_book = {
            "title": "",  # Empty title
            "author": "Test Author",
            "year": 2023
        }
        response = client.post("/books/", json=invalid_book)
        assert response.status_code == 422
    
    def test_get_all_books_empty(self):
        response = client.get("/books/")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_all_books_with_data(self, created_book):
        response = client.get("/books/")
        assert response.status_code == 200
        
        books = response.json()
        assert len(books) >= 1
        assert any(book["id"] == created_book["id"] for book in books)
    
    def test_get_book_by_id(self, created_book):
        response = client.get(f"/books/{created_book['id']}")
        assert response.status_code == 200
        
        book = response.json()
        assert book["id"] == created_book["id"]
        assert book["title"] == created_book["title"]
    
    def test_get_book_by_id_not_found(self):
        fake_id = str(uuid4())
        response = client.get(f"/books/{fake_id}")
        assert response.status_code == 404
    
    def test_get_book_by_id_invalid_format(self):
        response = client.get("/books/invalid-id")
        assert response.status_code == 400
    
    def test_delete_book(self, created_book):
        response = client.delete(f"/books/{created_book['id']}")
        assert response.status_code == 204
        
        # Verify book is deleted
        response = client.get(f"/books/{created_book['id']}")
        assert response.status_code == 404
    
    def test_delete_book_not_found(self):
        fake_id = str(uuid4())
        response = client.delete(f"/books/{fake_id}")
        assert response.status_code == 204  # Idempotent operation
    
    def test_delete_book_invalid_format(self):
        response = client.delete("/books/invalid-id")
        assert response.status_code == 400
    
    def test_filter_books_by_status(self, sample_book):
        # Create books with different statuses
        available_book = {**sample_book, "title": "Available Book", "status": "available"}
        borrowed_book = {**sample_book, "title": "Borrowed Book", "status": "borrowed"}
        
        client.post("/books/", json=available_book)
        client.post("/books/", json=borrowed_book)
        
        # Test filtering by available status
        response = client.get("/books/?status=available")
        assert response.status_code == 200
        books = response.json()
        assert all(book["status"] == "available" for book in books)
        
        # Test filtering by borrowed status
        response = client.get("/books/?status=borrowed")
        assert response.status_code == 200
        books = response.json()
        assert all(book["status"] == "borrowed" for book in books)
    
    def test_filter_books_by_author(self, sample_book):
        # Create books by different authors
        client.post("/books/", json={**sample_book, "title": "Book 1", "author": "John Doe"})
        client.post("/books/", json={**sample_book, "title": "Book 2", "author": "Jane Smith"})
        client.post("/books/", json={**sample_book, "title": "Book 3", "author": "John Johnson"})
        
        # Test filtering by author
        response = client.get("/books/?author=John")
        assert response.status_code == 200
        books = response.json()
        assert all("john" in book["author"].lower() for book in books)
    
    def test_sort_books_by_title(self, sample_book):
        # Create books with different titles
        client.post("/books/", json={**sample_book, "title": "C Book"})
        client.post("/books/", json={**sample_book, "title": "A Book"})
        client.post("/books/", json={**sample_book, "title": "B Book"})
        
        # Test ascending sort by title
        response = client.get("/books/?sort_by=title&ascending=true")
        assert response.status_code == 200
        books = response.json()
        titles = [book["title"] for book in books if book["title"] in ["A Book", "B Book", "C Book"]]
        assert titles == sorted(titles)
        
        # Test descending sort by title
        response = client.get("/books/?sort_by=title&ascending=false")
        assert response.status_code == 200
        books = response.json()
        titles = [book["title"] for book in books if book["title"] in ["A Book", "B Book", "C Book"]]
        assert titles == sorted(titles, reverse=True)
    
    def test_sort_books_by_year(self, sample_book):
        # Create books with different years
        client.post("/books/", json={**sample_book, "title": "Old Book", "year": 2020})
        client.post("/books/", json={**sample_book, "title": "New Book", "year": 2023})
        client.post("/books/", json={**sample_book, "title": "Middle Book", "year": 2021})
        
        # Test ascending sort by year
        response = client.get("/books/?sort_by=year&ascending=true")
        assert response.status_code == 200
        books = response.json()
        years = [book["year"] for book in books if book["year"] in [2020, 2021, 2023]]
        assert years == sorted(years)
        
        # Test descending sort by year
        response = client.get("/books/?sort_by=year&ascending=false")
        assert response.status_code == 200
        books = response.json()
        years = [book["year"] for book in books if book["year"] in [2020, 2021, 2023]]
        assert years == sorted(years, reverse=True)
    
    def test_invalid_sort_field(self):
        response = client.get("/books/?sort_by=invalid_field")
        assert response.status_code == 400
        assert "sort_by must be either 'title' or 'year'" in response.json()["detail"]
    
    def test_combined_filters_and_sort(self, sample_book):
        # Create test data
        client.post("/books/", json={**sample_book, "title": "Available 2021", "author": "John Doe", "year": 2021, "status": "available"})
        client.post("/books/", json={**sample_book, "title": "Available 2023", "author": "John Doe", "year": 2023, "status": "available"})
        client.post("/books/", json={**sample_book, "title": "Borrowed 2022", "author": "John Doe", "year": 2022, "status": "borrowed"})
        
        # Test combined filter and sort
        response = client.get("/books/?author=John&status=available&sort_by=year&ascending=true")
        assert response.status_code == 200
        books = response.json()
        assert all(book["status"] == "available" for book in books)
        assert all("john" in book["author"].lower() for book in books)
        years = [book["year"] for book in books]
        assert years == sorted(years)


class TestRootEndpoint:
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data
        assert "redoc" in data
