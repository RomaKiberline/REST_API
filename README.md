# Library API - Flask + Flask-RESTful + Swagger

## Опис

API для управління бібліотекою книг, реалізоване з використанням Flask, Flask-RESTful та автоматичною Swagger документацією через Flasgger.

## Технологічний стек

- **Python 3.11** - Основна мова програмування
- **Flask** - Легкий веб-фреймворк
- **Flask-RESTful** - Розширення для створення REST API
- **Flasgger** - Автоматична генерація Swagger документації
- **Pytest** - Тестування
- **Docker** - Контейнеризація

## Функціональність

### CRUD операції з книгами:
- `GET /api/books` - Отримати всі книги
- `POST /api/books` - Створити нову книгу
- `GET /api/books/{id}` - Отримати книгу за ID
- `PUT /api/books/{id}` - Оновити книгу
- `DELETE /api/books/{id}` - Видалити книгу

### Swagger документація:
- `GET /apidocs/` - Swagger UI
- `GET /apispec_1.json` - OpenAPI специфікація

## Запуск проєкту

### Локальний запуск

```bash
pip install -r requirements-flask.txt
python app.py
```

### Docker

```bash
docker-compose -f docker-compose-flask.yml up -d --build
```

## Документація API

### Swagger UI
Відкрийте у браузері: http://localhost:5000/apidocs/

### Приклади запитів

#### Отримати всі книги
```bash
curl -X GET http://localhost:5000/api/books
```

#### Створити нову книгу
```bash
curl -X POST http://localhost:5000/api/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Нова книга",
    "author": "Автор книги",
    "description": "Опис книги",
    "year": 2024,
    "status": "available"
  }'
```

## Тестування

```bash
pytest tests/test_flask_api.py -v
```

## Модель даних

### Book
```json
{
  "id": 1,
  "title": "Назва книги",
  "author": "Автор книги",
  "description": "Опис книги",
  "year": 2024,
  "status": "available|borrowed",
  "created_at": "2024-01-01T12:00:00",
  "updated_at": "2024-01-01T12:00:00"
}
```

## Структура проєкту

```
REST_API/
├── app.py                     # Головний Flask додаток
├── requirements-flask.txt      # Залежності для Flask
├── Dockerfile-flask            # Docker образ для Flask
├── docker-compose-flask.yml    # Docker Compose конфігурація
├── resources/                 # Flask-RESTful ресурси
│   ├── __init__.py
│   └── book_resource.py          # Ресурси книг
├── models/                     # Моделі даних
│   ├── __init__.py
│   └── flask_book.py             # Модель книги
└── tests/                      # Тести
    └── test_flask_api.py         # Тести API
```