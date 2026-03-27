#!/usr/bin/env python3
"""
Тестовий скрипт для перевірки Mock API з Prism
"""
import requests
import json

MOCK_BASE_URL = "http://localhost:4010"

def test_endpoint(method, endpoint, data=None, headers=None, description=""):
    """Тестування ендпоінту"""
    print(f"\n{'='*60}")
    print(f" {description}")
    print(f" {method.upper()} {endpoint}")
    
    try:
        if method.upper() == "GET":
            response = requests.get(f"{MOCK_BASE_URL}{endpoint}", headers=headers)
        elif method.upper() == "POST":
            if endpoint == "/token":
                response = requests.post(f"{MOCK_BASE_URL}{endpoint}", 
                                       data=data, 
                                       headers=headers)
            else:
                response = requests.post(f"{MOCK_BASE_URL}{endpoint}", 
                                       json=data, 
                                       headers=headers)
        
        print(f"Status Code: {response.status_code}")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        return response
        
    except requests.exceptions.ConnectionError:
        print("Помилка: Переконайтесь, що Mock API запущено на порту 4010")
        return None
    except Exception as e:
        print(f"Помилка: {e}")
        return None

def main():
    """Головна функція тестування"""
    print("Тестування Mock API з Prism")
    print(f"Base URL: {MOCK_BASE_URL}")
    
    auth_token = None
    
    # 1. Тест публічних ендпоінтів
    test_endpoint("GET", "/", description="1. Інформація про API")
    test_endpoint("GET", "/health", description="2. Перевірка здоров'я")
    
    # 2. Логін
    login_data = {"username": "johndoe", "password": "secret"}
    login_response = test_endpoint("POST", "/token", 
                                 data=login_data, 
                                 description="3. Логін")
    
    if login_response and login_response.status_code == 200:
        auth_token = login_response.json().get("access_token")
        print(f"Токен отримано: {auth_token[:20]}...")
    
    # 3. Тест без токена (401)
    test_endpoint("GET", "/books", description="4. Книги без токена (має бути 401)")
    
    # 4. Тест з токеном
    if auth_token:
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        test_endpoint("GET", "/books", 
                     headers=headers, 
                     description="5. Книги з токеном")
        
        test_endpoint("GET", "/books/1", 
                     headers=headers, 
                     description="6. Книга за ID")
        
        test_endpoint("GET", "/users/me", 
                     headers=headers, 
                     description="7. Профіль користувача")
        
        # Створення книги
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "description": "Test Description",
            "year": 2024
        }
        test_endpoint("POST", "/books", 
                     data=book_data,
                     headers=headers, 
                     description="8. Створення книги")
    
    print(f"\n{'='*60}")
    print("Тестування завершено!")

if __name__ == "__main__":
    main()
