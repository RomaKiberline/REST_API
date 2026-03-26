# Library API - FastAPI + JWT Authentication

## Опис

API для управління бібліотекою книг з JWT автентифікацією та авторизацією. Реалізовано access token + refresh token flow.

## Технологічний стек

- **FastAPI** - Високопродуктивний веб-фреймворк
- **JWT** - JSON Web Tokens для автентифікації
- **OAuth2** - OAuth2PasswordBearer для токенів
- **Passlib** - Хешування паролів
- **Pydantic** - Валідація даних
- **Pytest** - Тестування

## Функціональність

###  Автентифікація:
- `POST /auth/token` - Логін та отримання токенів
- `POST /auth/refresh` - Оновлення access token
- `GET /auth/me` - Інформація про поточного користувача

###  Захищені ендпоінти книг:
- `GET /books` - Отримати всі книги
- `GET /books/{id}` - Отримати книгу за ID
- `POST /books` - Створити нову книгу
- `PUT /books/{id}` - Оновити книгу
- `DELETE /books/{id}` - Видалити книгу

###  Публічні ендпоінти:
- `GET /` - Інформація про API
- `GET /health` - Перевірка здоров'я

## Запуск проєкту

### Встановлення залежностей
```bash
pip install -r requirements-jwt.txt
```

### Запуск
```bash
python main_jwt.py
```

## Документація API

### Swagger UI
Відкрийте у браузері: http://localhost:8000/docs

##  JWT Token Flow

### 1. Логін (отримання токенів)
```bash
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=secret"
```

**Відповідь:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### 2. Використання Access Token
```bash
curl -X GET "http://localhost:8000/books" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

### 3. Оновлення Access Token
```bash
curl -X POST "http://localhost:8000/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."}'
```

##  Тестові користувачі

### Користувач 1:
- **Username:** `johndoe`
- **Password:** `secret`
- **Email:** `johndoe@example.com`

### Користувач 2:
- **Username:** `alice`
- **Password:** `secret123`
- **Email:** `alice@example.com`

##Тестування

```bash
pytest tests/test_jwt_auth.py -v
```

## Моделі даних

### Token
```json
{
  "access_token": "string",
  "refresh_token": "string",
  "token_type": "bearer"
}
```

### User
```json
{
  "username": "string",
  "email": "string",
  "full_name": "string",
  "disabled": "boolean"
}
```

### Book
```json
{
  "id": "integer",
  "title": "string",
  "author": "string",
  "description": "string",
  "year": "integer",
  "status": "string",
  "created_at": "datetime"
}
```

## Конфігурація JWT

### Access Token:
- **Термін дії:** 30 хвилин
- **Алгоритм:** HS256
- **Тип:** "access"

### Refresh Token:
- **Термін дії:** 7 днів
- **Алгоритм:** HS256
- **Тип:** "refresh"


## Розгортання

### Docker
```bash
FROM python:3.11-slim
WORKDIR /app
COPY requirements-jwt.txt .
RUN pip install -r requirements-jwt.txt
COPY . .
EXPOSE 8000
CMD ["python", "main_jwt.py"]
```

### Environment Variables
```bash
export SECRET_KEY="your-secret-key"
export ACCESS_TOKEN_EXPIRE_MINUTES=30
export REFRESH_TOKEN_EXPIRE_DAYS=7
```

## Структура проєкту

```
REST_API/
├── main_jwt.py                 # FastAPI додаток з JWT
├── requirements-jwt.txt        # Залежності для JWT
├── auth/                       # Модуль автентифікації
│   ├── __init__.py
│   ├── jwt_config.py           # JWT конфігурація
│   └── auth_routes.py          # Автентифікаційні маршрути
└── tests/
    └── test_jwt_auth.py        # Тести JWT
```
