# 📚 API Бібліотеки з FastAPI та MongoDB

> **Лабораторна робота 4** - Робота з MongoDB

[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://mongodb.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Motor](https://img.shields.io/badge/Motor-00A046?style=for-the-badge)](https://motor.readthedocs.io)

## 🎯 Огляд проекту

Асинхронний API для управління бібліотечною системою, побудований з використанням сучасних технологій Python та NoSQL бази даних MongoDB.

### ✨ Ключові особливості

- **🚀 CRUD операції** - Повний цикл роботи з книгами (створення, читання, оновлення, видалення)
- **📄 Пагінація** - Limit-Offset пагінація для ефективної роботи з великими обсягами даних
- **🔍 Фільтрація** - Розширені можливості фільтрації за статусом та автором
- **📊 Сортування** - Динамічне сортування за назвою, автором, роком або часом створення
- **✅ Валідація** - Автоматична валідація даних з Pydantic
- **🐳 Docker** - Повна контейнеризація додатку та бази даних
- **🗄️ MongoDB** - Гнучка NoSQL база даних з JSON документами
- **🧪 Тестування** - Комплексний набір юніт тестів з мокуванням
- **⚡ Асинхронність** - Використання async/await для високої продуктивності

## 🏗️ Архітектура проекту

Проект побудований за принципами **чистої архітектури** з чітким розділенням відповідальностей:

```
├── 📁 api/                    # API шар - FastAPI роутери
│   └── books_mongo.py         # Книжкові ендпоінти для MongoDB
├── 📁 schemas/                # Схеми - Pydantic моделі валідації
│   └── book_mongo.py          # Схеми книг з ObjectId підтримкою
├── 📁 services/               # Бізнес-логіка - сервіси додатку
│   └── book_mongo_service.py  # Сервіс роботи з книгами MongoDB
├── 📁 mongodb/                # Доступ до даних - MongoDB репозиторії
│   ├── client.py              # MongoDB клієнт та підключення
│   └── book_repository.py     # Репозиторій книг MongoDB
├── 📁 tests/                  # Тестування - юніт тести
│   └── test_books_mongo.py    # Тести API для MongoDB
├── 🐳 Dockerfile              # Docker образ API
├── 🐳 docker-compose.yml      # Оркестрація контейнерів
├── ⚙️ main.py                 # Головний файл додатку
├── 📦 requirements.txt        # Залежності Python
└── 📖 README.md               # Ця документація
```

## 🚀 Швидкий старт

### 📋 Передумови

- **Docker Desktop** ([завантажити](https://www.docker.com/products/docker-desktop))
- **Git** ([завантажити](https://git-scm.com))

### ⚡ Запуск в 3 команди

```bash
# 1. Клонувати репозиторій
git clone https://github.com/RomaKiberline/REST_API.git
cd REST_API

# 2. Запустити Docker Compose
docker-compose up --build

# 3. Відкрити API документацію
# http://localhost:8000/docs
```

🎉 **Готово!** Ваш API працює на `http://localhost:8000`

## 📖 Детальна документація API

Після запуску API доступний за адресою: **http://localhost:8000**

### 🔗 Ключові посилання
- **📋 Swagger UI**: `http://localhost:8000/docs`
- **🌐 Кореневий ендпоінт**: `http://localhost:8000/`

## 📚 Ендпоінти API

### 📖 Отримання книг з пагінацією

```http
GET /books/
```

#### 🔧 Параметри запиту

| Параметр | Тип | Опис | Приклад |
|----------|-----|------|---------|
| `limit` | integer | Кількість книг на сторінці (1-1000) | `10` |
| `offset` | integer | Кількість книг для пропуску | `0` |
| `status` | string | Фільтр за статусом (`available` або `borrowed`) | `available` |
| `author` | string | Фільтр за автором (частковий збіг) | `Шевченко` |
| `sort_by` | string | Сортування (`title`, `author`, `year` або `created_at`) | `year` |
| `ascending` | boolean | Порядок сортування | `false` |

#### 📤 Відповідь

```json
{
  "books": [
    {
      "id": "507f1f77bcf86cd799439011",
      "title": "Кобзар",
      "author": "Тарас Шевченко",
      "description": "Збірка поезій",
      "status": "available",
      "year": 1840,
      "created_at": "2026-01-01T12:00:00Z"
    }
  ],
  "total": 150,
  "limit": 10,
  "offset": 0,
  "has_next": true,
  "has_prev": false
}
```

#### 🌟 Приклади використання

```bash
# Отримати перші 5 книг
GET /books/?limit=5&offset=0

# Фільтр за доступними книгами
GET /books/?status=available

# Пошук книг Шевченка
GET /books/?author=Шевченко

# Сортування за роком (новіші перші)
GET /books/?sort_by=year&ascending=false

# Комбінований запит
GET /books/?status=available&author=Шевченко&limit=10&sort_by=year&ascending=false
```

### ➕ Створення нової книги

```http
POST /books/
```

#### 📥 Тіло запиту

```json
{
  "title": "Назва книги",
  "author": "Автор книги",
  "description": "Опис книги (опціонально)",
  "status": "available",
  "year": 2026
}
```

#### 📤 Успішна відповідь (201 Created)

```json
{
  "id": "507f1f77bcf86cd799439011",
  "title": "Назва книги",
  "author": "Автор книги",
  "description": "Опис книги",
  "status": "available",
  "year": 2026,
  "created_at": "2026-01-01T12:00:00Z"
}
```

### 📖 Отримання книги за ID

```http
GET /books/{book_id}
```

#### 🆔 Параметри шляху

| Параметр | Тип | Опис | Приклад |
|----------|-----|------|---------|
| `book_id` | string | ObjectId книги | `507f1f77bcf86cd799439011` |

### 🗑️ Видалення книги

```http
DELETE /books/{book_id}
```

#### 📤 Успішна відповідь (204 No Content)
Порожня відповідь - книга успішно видалена.

## 🧪 Тестування

### 🚀 Запуск тестів

```bash
# Запуск всіх тестів
pytest

# Запуск з покриттям коду
pytest --cov=.

# Детальні логи
pytest -v
```

### 📊 Результати тестів

Проект містить комплексний набір тестів:
- ✅ Тестування всіх CRUD операцій
- ✅ Тестування пагінації
- ✅ Тестування фільтрації та сортування
- ✅ Тестування валідації
- ✅ Async mock тестування сервісів

## 🐳 Docker деталі

### 📁 Структура docker-compose.yml

```yaml
version: '3.8'
services:
  mongodb:
    image: mongo:7.0
    environment:
      MONGO_INITDB_ROOT_USERNAME: mongo_admin
      MONGO_INITDB_ROOT_PASSWORD: password
      MONGO_INITDB_DATABASE: library_db
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      MONGODB_URL: mongodb://mongo_admin:password@mongodb:27017/library_db
    depends_on:
      mongodb:
        condition: service_healthy
    volumes:
      - .:/app
    restart: unless-stopped

volumes:
  mongodb_data:
```

### 🔧 Dockerfile

```dockerfile
FROM python:3.11-slim

# Встановлення системних залежностей
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Робоча директорія
WORKDIR /app

# Копіювання та встановлення залежностей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіювання коду проекту
COPY . .

# Запуск додатку
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔧 Розробка та налагодження

### 📝 Локальний запуск (без Docker)

```bash
# 1. Встановіть залежності
pip install -r requirements.txt

# 2. Запустіть MongoDB локально або використовуйте Docker
# Docker MongoDB
docker run -d --name mongo-dev -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=mongo_admin -e MONGO_INITDB_ROOT_PASSWORD=password mongo:7.0

# 3. Встановіть змінну середовища
export MONGODB_URL="mongodb://mongo_admin:password@localhost:27017/library_db"

# 4. Запустіть додаток
uvicorn main:app --reload
```

### 🐛 Debugging

#### Перегляд логів контейнерів
```bash
# Логи API
docker logs restapi-api-1

# Логи MongoDB
docker logs restapi-mongodb-1

# Логи в реальному часі
docker logs -f restapi-api-1
```

#### Підключення до MongoDB
```bash
# Вхід до MongoDB контейнера
docker exec -it restapi-mongodb-1 mongosh --username mongo_admin --password password --authenticationDatabase admin

# Переключення на базу даних
use library_db

# Перевірка колекцій
show collections

# Перевірка даних
db.books.find().limit(5)
```

## 📊 Схема даних MongoDB

### 🗂️ Колекція `books`

| Поле | Тип | Обов'язкове | Опис |
|------|-----|-------------|------|
| `_id` | ObjectId | ✅ | Первинний ключ (генерується MongoDB) |
| `title` | String | ✅ | Назва книги |
| `author` | String | ✅ | Автор книги |
| `description` | String | ❌ | Опис книги |
| `status` | String | ✅ | Статус (`available` або `borrowed`) |
| `year` | Integer | ✅ | Рік видання (1000-2100) |
| `created_at` | Date | ✅ | Час створення |

### 📋 Індекси

Для оптимізації запитів створені індекси:
- `title` - для сортування за назвою
- `author` - для фільтрації за автором
- `year` - для сортування за роком
- `status` - для фільтрації за статусом

## 🚀 Технологічний стек

- **🐍 Python 3.11** - Основна мова програмування
- **⚡ FastAPI** - Високопродуктивний веб-фреймворк
- **🗄️ MongoDB** - NoSQL база даних
- **🔄 Motor** - Асинхронний драйвер MongoDB
- **🔧 Pydantic** - Валідація та серіалізація даних
- **🐳 Docker** - Контейнеризація
- **🧪 Pytest** - Тестування
- **📦 pydantic-mongo** - Підтримка ObjectId в Pydantic

## 🎯 Переваги MongoDB

- **🚀 Гнучкість** - Динамічна схема документів
- **⚡ Продуктивність** - Швидкі операції читання/запису
- **📈 Масштабованість** - Горизонтальне масштабування
- **🔄 Асинхронність** - Високий рівень конкурентності
- **📝 JSON** - Нативна підтримка JSON документів
