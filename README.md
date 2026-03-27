# Library API - FastAPI + JWT + Rate Limiter

## Опис

API для управління бібліотекою книг з JWT автентифікацією та Rate Limiter на основі Redis.

## Функціональність

### Rate Limiting:
- **Анонімні користувачі:** 2 запити за хвилину
- **Авторизовані користувачі:** 10 запитів за хвилину
- **Sliding time window** алгоритм

### API Ендпоінти:
- POST /token - Логін та отримання токенів
- GET /books - Отримати книги (авторизовані)
- POST /books - Створити книгу (авторизовані)
- GET /health - Перевірка здоров'я (без ліміту)

## Запуск

### Встановлення:
pip install -r requirements.txt

### Запуск з Redis:
docker-compose up -d redis
python main.py

### Запуск без Redis:
python main.py

## Документація

Swagger UI: http://localhost:8000/docs

## Тестування

pytest tests/test_rate_limiter.py -v
pytest tests/test_auth_no_redis.py -v

## Структура проєкту

REST_API/
├── main.py                    # FastAPI додаток
├── rate_limiter.py            # Rate limiter логіка
├── redis_config.py            # Redis конфігурація
├── requirements.txt           # Залежності
├── docker-compose.yml         # Docker з Redis
└── tests/                     # Тести

## Тестові користувачі

- johndoe / secret
- alice / secret123

## Ліцензія

MIT License
