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

### **Swagger документація:**
- `GET /apidocs/` - Swagger UI
- `GET /apispec_1.json` - OpenAPI специфікація

## Структура проєкту

```
REST_API/
├── 📁 app.py                     # Головний Flask додаток
├── 📁 requirements-flask.txt      # Залежності для Flask
├── 📁 Dockerfile-flask            # Docker образ для Flask
├── 📁 docker-compose-flask.yml    # Docker Compose конфігурація
├── 📁 resources/                 # Flask-RESTful ресурси
│   ├── __init__.py
│   └── book_resource.py          # Ресурси книг
├── 📁 models/                     # Моделі даних
│   ├── __init__.py
│   └── flask_book.py             # Модель книги
├── 📁 tests/                      # Тести
│   └── test_flask_api.py         # Тести API
└── 📁 README-Flask.md             # Цей файл
```

## Запуск проєкту

### **Docker Compose**

```bash
# Запуск з Docker Compose
docker-compose -f docker-compose-flask.yml up -d --build

# Перевірка статусу
docker-compose -f docker-compose-flask.yml ps

# Перегляд логів
docker-compose -f docker-compose-flask.yml logs -f flask-api
```

### **Локальний запуск**

```bash
# Встановлення залежностей
pip install -r requirements-flask.txt

# Запуск додатку
python app.py
```

## Документація API

### **Swagger UI**
Відкрийте у браузері: http://localhost:5000/apidocs/

### **OpenAPI специфікація**
http://localhost:5000/apispec_1.json

### **Приклади запитів**

#### **Отримати всі книги**
```bash
curl -X GET http://localhost:5000/api/books
```

#### **Створити нову книгу**
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

#### **Отримати книгу за ID**
```bash
curl -X GET http://localhost:5000/api/books/1
```

#### **Оновити книгу**
```bash
curl -X PUT http://localhost:5000/api/books/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Оновлена назва",
    "author": "Оновлений автор"
  }'
```

#### **Видалити книгу**
```bash
curl -X DELETE http://localhost:5000/api/books/1
```

## Тестування

```bash
# Запуск всіх тестів
pytest tests/test_flask_api.py -v

# Запуск з покриттям
pytest tests/test_flask_api.py -v --cov=resources --cov-report=html

# Запуск конкретного тесту
pytest tests/test_flask_api.py::TestBookAPI::test_get_all_books -v
```

## Модель даних

### **Book**
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

## Налаштування Swagger

Flasgger автоматично генерує документацію на основі:

- **Docstrings** в методах ресурсів
- **YAML/JSON** специфікацій в коментарях
- **Flask-RESTful** маршрутів

### **Приклад документації методу**
```python
def get(self):
    """
    Отримати список всіх книг
    ---
    responses:
      200:
        description: Список книг успішно отримано
        schema:
          type: array
          items:
            $ref: '#/definitions/Book'
    """
    pass
```

## Переваги Flask + Flask-RESTful

- **Простота** - Легкий та швидкий для розробки
- **Гнучкість** - Мінімалістичний підхід
- **Автодокументація** - Flasgger генерує Swagger
- **Тестування** - Вбудована підтримка тестів
- **Контейнеризація** - Легко розгортати

## Деталі Docker

### **Dockerfile-flask**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements-flask.txt .
RUN pip install --no-cache-dir -r requirements-flask.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### **docker-compose-flask.yml**
- **Порт:** 5000
- **Health check:** Перевірка `/api/books`
- **Volume:** Монтування коду для розробки

## Обробка помилок

API повертає стандартні HTTP коди:

- **200** - Успіх
- **201** - Створено
- **204** - Видалено (без контенту)
- **400** - Помилка валідації
- **404** - Не знайдено

## Моніторинг

```bash
curl -f http://localhost:5000/api/books
curl http://localhost:5000/apispec_1.json | jq .
```

## Розробка

### **Додавання нових ендпоінтів**
1. Створіть новий ресурс в `resources/`
2. Додайте маршрут в `app.py`
3. Напишіть тести в `tests/`
4. Додайте документацію Flasgger

### **Стиль кодування**
- **PEP 8** - стандарт Python
- **Docstrings** - для документації
- **Type hints** - для кращої читабельності
