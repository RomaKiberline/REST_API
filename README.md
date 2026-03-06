# 📚 API Бібліотеки з Cursor пагінацією та Docker

> **Лабораторна робота 3** - REST API для управління книгами в бібліотеці з використанням PostgreSQL, SQLAlchemy та Docker контейнеризації з Cursor пагінацією.

[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1E90FF?style=for-the-badge)](https://sqlalchemy.org)

## 🎯 Огляд проекту

Простий та ефективний API для управління бібліотечною системою, побудований з використанням сучасних технологій Python.

### ✨ Ключові особливості

- **🚀 CRUD операції** - Повний цикл роботи з книгами (створення, читання, оновлення, видалення)
- **📄 Пагінація** - Limit-Offset пагінація для ефективної роботи з великими обсягами даних
- **🔍 Фільтрація** - Розширені можливості фільтрації за статусом та автором
- **📊 Сортування** - Динамічне сортування за назвою або роком видання
- **✅ Валідація** - Автоматична валідація даних з Pydantic
- **🐳 Docker** - Повна контейнеризація додатку та бази даних
- **🗄️ PostgreSQL** - Надійна реляційна база даних
- **🧪 Тестування** - Комплексний набір юніт тестів

## 🏗️ Архітектура проекту

Проект побудований за принципами **чистої архітектури** з чітким розділенням відповідальностей:

```
├── 📁 api/              # 🌐 API шар - FastAPI роутери
│   └── books.py         # Книжкові ендпоінти
├── 📁 schemas/          # 📋 Схеми - Pydantic моделі валідації
│   ├── book.py          # Схеми книг
│   └── pagination.py    # Схеми пагінації
├── 📁 services/         # 💼 Бізнес-логіка - сервіси додатку
│   └── book_service.py  # Сервіс роботи з книгами
├── 📁 repository/       # 🗃️ Доступ до даних - репозиторії
│   └── book_repository.py # Репозиторій книг
├── 📁 models/           # 🏗️ Дані моделі - SQLAlchemy ORM
│   └── book.py          # Модель книги
├── 📁 tests/            # 🧪 Тестування - юніт тести
│   └── test_books.py    # Тести API
├── 📁 alembic/          # 🔄 Міграції БД
│   ├── versions/        # Версії міграцій
│   └── env.py           # Конфігурація Alembic
├── 🐳 Dockerfile        # Docker образ API
├── 🐳 docker-compose.yml # Оркестрація контейнерів
├── ⚙️ main.py           # Головний файл додатку
├── 🗄️ database.py       # Конфігурація БД
├── 📦 requirements.txt  # Залежності Python
└── 📖 README.md         # Ця документація
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

### 📖 Отримання книг з Cursor пагінацією

```http
GET /books/
```

#### 🔧 Параметри запиту

| Параметр | Тип | Опис | Приклад |
|----------|-----|------|---------|
| `limit` | integer | Кількість книг на сторінці (1-1000) | `10` |
| `cursor` | string | Cursor для пагінації (ID останньої книги з попередньої сторінки) | `550e8400-e29b-41d4-a716-446655440000` |
| `status` | string | Фільтр за статусом (`available` або `borrowed`) | `available` |
| `author` | string | Фільтр за автором (частковий збіг) | `Шевченко` |
| `sort_by` | string | Сортування (`title`, `year` або `created_at`) | `created_at` |
| `ascending` | boolean | Порядок сортування | `false` |

#### 📤 Відповідь

```json
{
  "books": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Кобзар",
      "author": "Тарас Шевченко",
      "description": "Збірка поезій",
      "status": "available",
      "year": 1840,
      "created_at": "2026-01-01T12:00:00Z"
    }
  ],
  "next_cursor": "550e8400-e29b-41d4-a716-446655440001",
  "has_next": true,
  "limit": 10
}
```

#### 🌟 Приклади використання

```bash
# Отримати перші 5 книг
GET /books/?limit=5

# Отримати наступну сторінку використовуючи cursor
GET /books/?limit=5&cursor=550e8400-e29b-41d4-a716-446655440000

# Фільтр за доступними книгами
GET /books/?status=available

# Пошук книг Шевченка
GET /books/?author=Шевченко

# Сортування за часом створення (новіші перші)
GET /books/?sort_by=created_at&ascending=false

# Комбінований запит
GET /books/?status=available&author=Шевченко&limit=10&sort_by=year&ascending=false
```

#### 🔄 Як працює Cursor пагінація:

1. **Перший запит**: `GET /books/?limit=10` - повертає перші 10 книг
2. **Наступні сторінки**: Використовуйте `next_cursor` з попередньої відповіді
3. **Приклад**: `GET /books/?limit=10&cursor=550e8400-e29b-41d4-a716-446655440000`
4. **Кінець**: Коли `has_next: false`, більше сторінок немає

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
  "id": "550e8400-e29b-41d4-a716-446655440000",
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
| `book_id` | string | UUID книги | `550e8400-e29b-41d4-a716-446655440000` |

#### 📤 Успішна відповідь (200 OK)

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Кобзар",
  "author": "Тарас Шевченко",
  "description": "Збірка поезій",
  "status": "available",
  "year": 1840,
  "created_at": "2026-01-01T12:00:00Z"
}
```

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
- ✅ Mock тестування сервісів

## 🐳 Docker деталі

### 📁 Структура docker-compose.yml

```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: library_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/library_db
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - .:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

volumes:
  postgres_data:
```

### 🔧 Dockerfile

```dockerfile
FROM python:3.11-slim

# Встановлення системних залежностей
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
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

# 2. Запустіть PostgreSQL локально або використовуйте Docker
# Варіант 1: Docker PostgreSQL
docker run -d --name postgres-dev -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:15

# Варіант 2: Локальний PostgreSQL
# Створіть базу даних library_db

# 3. Запустіть міграції
alembic upgrade head

# 4. Запустіть додаток
uvicorn main:app --reload
```

### 🐛 Debugging

#### Перегляд логів контейнерів
```bash
# Логи API
docker logs restapi-api-1

# Логи PostgreSQL
docker logs restapi-db-1

# Логи в реальному часі
docker logs -f restapi-api-1
```

#### Підключення до БД
```bash
# Вхід до PostgreSQL контейнера
docker exec -it restapi-db-1 psql -U postgres -d library_db

# Перевірка таблиць
\dt

# Перевірка даних
SELECT * FROM books LIMIT 5;
```

## 📊 Схема даних

### 🗂️ Таблиця `books`

| Поле | Тип | Обов'язкове | Опис |
|------|-----|-------------|------|
| `id` | UUID | ✅ | Первинний ключ |
| `title` | VARCHAR(200) | ✅ | Назва книги |
| `author` | VARCHAR(100) | ✅ | Автор книги |
| `description` | VARCHAR(1000) | ❌ | Опис книги |
| `status` | ENUM | ✅ | Статус (`available` або `borrowed`) |
| `year` | INTEGER | ✅ | Рік видання (1000-2100) |
| `created_at` | TIMESTAMP | ✅ | Час створення |


