# Library Mock API - Lab 8

## Опис

Mock API для бібліотеки книг з використанням Stoplight Prism.

## Вимоги лабораторної

- Stoplight Prism framework для HTTP mocking
- OpenAPI специфікація
- Docker Compose з командою для запуску mock сервісу

## Функціональність

### Ендпоінти:
- `GET /` - Інформація про API
- `GET /health` - Перевірка здоров'я
- `POST /token` - Логін та JWT токени
- `POST /refresh` - Оновлення токена
- `GET /books` - Список книг (авторизація)
- `POST /books` - Створення книги (авторизація)
- `GET /books/{id}` - Книга за ID (авторизація)
- `GET /users/me` - Профіль користувача (авторизація)

## Запуск

### Через Prism CLI:
```bash
npx @stoplight/prism-cli mock openapi.yaml -h 0.0.0.0 -p 4010
```

### Через Docker Compose:
```bash
docker-compose up -d
```

Command для запуску mock сервісу:
```
mock -h 0.0.0.0 -p 4010 /tmp/openapi.yaml
```

## Тестування

```bash
# Запуск Mock API
npx @stoplight/prism-cli mock openapi.yaml -h 0.0.0.0 -p 4010

# Тести
python tests/test_mock_api.py
```

## Структура проєкту

```
REST_API/
├── openapi.yaml               # OpenAPI специфікація для API
├── docker-compose.yaml        # Docker Compose з Prism
├── tests/
│   └── test_mock_api.py       # Тестовий скрипт
├── requirements.txt           # Python залежності
└── README.md                  # Документація
```

## Тестові користувачі

- johndoe / secret
- alice / secret123