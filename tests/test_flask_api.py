import pytest
import json
from app import app
from models.flask_book import flask_books_list

@pytest.fixture
def client():
    """Створення тестового клієнта"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_book():
    """Приклад книги для тестування"""
    return {
        'title': 'Тестова книга',
        'author': 'Тестовий автор',
        'description': 'Тестовий опис',
        'year': 2024,
        'status': 'available'
    }

class TestBookAPI:
    """Тести для API книг"""
    
    def test_get_all_books(self, client):
        """Тест отримання всіх книг"""
        response = client.get('/api/books')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_get_book_by_id(self, client):
        """Тест отримання книги за ID"""
        response = client.get('/api/books')
        books = json.loads(response.data)
        
        if books:
            book_id = books[0]['id']
            response = client.get(f'/api/books/{book_id}')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['id'] == book_id
    
    def test_get_nonexistent_book(self, client):
        """Тест отримання неіснуючої книги"""
        response = client.get('/api/books/99999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_create_book(self, client, sample_book):
        """Тест створення нової книги"""
        response = client.post('/api/books', 
                              data=json.dumps(sample_book),
                              content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['title'] == sample_book['title']
        assert data['author'] == sample_book['author']
        assert 'id' in data
    
    def test_create_book_missing_fields(self, client):
        """Тест створення книги з відсутніми полями"""
        incomplete_book = {
            'title': 'Тестова книга'
        }
        response = client.post('/api/books',
                              data=json.dumps(incomplete_book),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_update_book(self, client, sample_book):
        """Тест оновлення книги"""
        response = client.post('/api/books',
                              data=json.dumps(sample_book),
                              content_type='application/json')
        book_id = json.loads(response.data)['id']
        
        updated_data = {
            'title': 'Оновлена назва',
            'author': 'Оновлений автор'
        }
        response = client.put(f'/api/books/{book_id}',
                             data=json.dumps(updated_data),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == 'Оновлена назва'
        assert data['author'] == 'Оновлений автор'
    
    def test_update_nonexistent_book(self, client):
        """Тест оновлення неіснуючої книги"""
        updated_data = {
            'title': 'Оновлена назва'
        }
        response = client.put('/api/books/99999',
                             data=json.dumps(updated_data),
                             content_type='application/json')
        assert response.status_code == 404
    
    def test_delete_book(self, client, sample_book):
        """Тест видалення книги"""
        response = client.post('/api/books',
                              data=json.dumps(sample_book),
                              content_type='application/json')
        book_id = json.loads(response.data)['id']
        
        response = client.delete(f'/api/books/{book_id}')
        assert response.status_code == 204
        
        response = client.get(f'/api/books/{book_id}')
        assert response.status_code == 404
    
    def test_delete_nonexistent_book(self, client):
        """Тест видалення неіснуючої книги"""
        response = client.delete('/api/books/99999')
        assert response.status_code == 404

class TestSwaggerDocumentation:
    """Тести для Swagger документації"""
    
    def test_swagger_ui_accessible(self, client):
        """Тест доступності Swagger UI"""
        response = client.get('/apidocs/')
        assert response.status_code == 200
    
    def test_api_spec_accessible(self, client):
        """Тест доступності API специфікації"""
        response = client.get('/apispec_1.json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'info' in data
        assert 'paths' in data
