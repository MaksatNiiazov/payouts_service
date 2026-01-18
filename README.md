# Payouts Service

Backend-сервис для управления заявками на выплату средств.  
Заявки создаются через REST API и обрабатываются асинхронно с использованием Celery.

Проект сфокусирован на **надёжности**, **транзакционной целостности** и **предсказуемом поведении API**, что критично для финтех-сценариев.

---

## Основные принципы

- **Транзакционная безопасность**
  - постановка Celery-задач происходит только после успешного commit (`transaction.on_commit`)
- **Идемпотентность API**
  - защита от повторных запросов клиента
- **Чёткие границы ответственности**
  - API — приём и валидация данных  
  - сервисный слой — бизнес-сценарии  
  - Celery — асинхронная обработка
- **Воспроизводимое окружение**
  - Docker Compose
  - фиксированные зависимости (Poetry + lock)
- **Тестируемость**
  - unit и интеграционные тесты
  - корректная проверка `on_commit` и асинхронных сценариев

---

## Технологический стек

- Python 3.12
- Django 4.2
- Django REST Framework
- PostgreSQL 16
- Celery 5 + Redis 7
- Poetry
- Pytest + pytest-django
- Swagger / Redoc (drf-spectacular)

---

## Архитектура

```

payouts/  
├── models.py # доменные модели (Payout)  
├── serializers.py # валидация входных данных  
├── views.py # REST API  
├── services.py # бизнес-сценарии и транзакции  
├── tasks.py # Celery-задачи  
├── middleware.py # Idempotency-Key  
└── tests/ # unit / integration tests

```

Бизнес-логика вынесена в сервисный слой, чтобы:
- не перегружать views,
- упростить тестирование,
- централизовать работу с транзакциями и побочными эффектами.

---

## API

Базовый путь:

```

/api/payouts/

````

### Эндпоинты

- `GET /api/payouts/` — список заявок
- `GET /api/payouts/{id}/` — получить заявку
- `POST /api/payouts/` — создать заявку
- `PATCH /api/payouts/{id}/` — частичное обновление
- `DELETE /api/payouts/{id}/` — удалить заявку

### Пример создания заявки

```http
POST /api/payouts/
Content-Type: application/json

{
  "amount": "100.00",
  "currency": "USD",
  "recipient_details": "Card ****1234",
  "comment": "Test payout"
}
````

---

## Идемпотентность

Для `POST /api/payouts/` поддерживается заголовок:

```
Idempotency-Key: <unique-value>
```

Поведение:

- повторный запрос с тем же ключом **не создаёт новую заявку**
    
- возвращается сохранённый ответ первого запроса
    
- защищает от повторной доставки запросов при сетевых сбоях и ретраях
    

---

## Асинхронная обработка

После создания заявки сервис:

1. сохраняет данные в транзакции,
    
2. регистрирует callback через `transaction.on_commit`,
    
3. **только после commit** ставит Celery-задачу на обработку.

Такой подход исключает:

- фантомные задачи,
    
- гонки состояний,
    
- неконсистентные выплаты.

---

## Документация API

- Swagger UI:  
    `http://localhost:8000/api/schema/swagger-ui/`
    
- Redoc:  
    `http://localhost:8000/api/schema/redoc/`
    
- OpenAPI schema:  
    `http://localhost:8000/api/schema/`

---

## Запуск проекта (Docker)

### Переменные окружения

Создай `.env` в корне проекта:

```env
DJANGO_SECRET_KEY=dev-secret-key
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=payouts
POSTGRES_USER=payouts
POSTGRES_PASSWORD=payouts
POSTGRES_HOST=db
POSTGRES_PORT=5432

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1
```

### Запуск сервисов

```bash
docker compose up --build
```

API будет доступно по адресу:

```
http://localhost:8000
```

### Миграции

```bash
docker compose exec web python manage.py migrate
```

---

## Тесты

Тесты запускаются в отдельном контейнере:

```bash
docker compose run --rm test
```

### Примечание о транзакциях

Тесты, проверяющие вызов Celery-задач через `transaction.on_commit`, используют:

```python
pytest.mark.django_db(transaction=True)
```

Это необходимо, так как стандартная транзакционная обёртка pytest-django выполняет rollback и `on_commit` callback не будет исполнен.

---

## Деплой (подход)

В production-окружении сервис разворачивается как набор отдельных компонентов:

- Django API (gunicorn)
    
- Celery worker
    
- PostgreSQL
    
- Redis
    
- reverse-proxy (Nginx / Traefik)

Базовый сценарий:

1. выполнение миграций при релизе,
    
2. запуск web-процесса,
    
3. запуск worker-процессов,
    
4. настройка логирования и мониторинга очередей.

---

## Итог

Проект демонстрирует:

- аккуратную работу с транзакциями,
    
- корректную интеграцию Celery,
    
- идемпотентность API,
    
- чистую архитектуру,
    
- готовность к использованию в production-среде.
    




