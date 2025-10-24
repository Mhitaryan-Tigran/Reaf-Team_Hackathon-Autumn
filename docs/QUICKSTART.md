# ⚡ Quick Start Guide - Быстрый старт

> Минимальная инструкция для запуска проекта за 5 минут

---

## 🚀 Запуск через Docker (рекомендуется)

### Шаг 1: Клонировать и настроить

```bash
# Клонировать репозиторий
git clone <repository-url>
cd host-checker

# Скопировать переменные окружения
cp .env.example .env

# Отредактировать (опционально)
nano .env
```

### Шаг 2: Запустить всё одной командой

```bash
# Запустить все сервисы
docker-compose up -d

# Проверить статус
docker-compose ps

# Посмотреть логи
docker-compose logs -f
```

### Шаг 3: Инициализация БД

```bash
# Применить миграции
docker-compose exec backend alembic upgrade head

# Создать тестового пользователя (опционально)
docker-compose exec backend python -m app.cli create-user
```

### Шаг 4: Открыть приложение

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🛠 Локальная разработка (без Docker)

### Требования

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+

### Backend

```bash
# Перейти в директорию
cd backend

# Установить зависимости
pip install poetry
poetry install

# Настроить БД
poetry run alembic upgrade head

# Запустить сервер
poetry run uvicorn app.main:app --reload

# Доступен на http://localhost:8000
```

### Frontend

```bash
# Перейти в директорию
cd frontend

# Установить зависимости
npm install

# Запустить dev server
npm run dev

# Доступен на http://localhost:3000
```

### Agent

```bash
# Перейти в директорию
cd agent

# Установить зависимости
poetry install

# Настроить переменные
export API_URL=http://localhost:8000
export AGENT_TOKEN=your-token
export AGENT_NAME=Local-Agent
export AGENT_LOCATION=Local

# Запустить агента
poetry run python -m agent.main
```

---

## 🔑 Регистрация агента

### Получить токен регистрации

```bash
# Через API (нужен master token)
curl -X POST http://localhost:8000/api/agents/register \
  -H "X-Registration-Token: master-secret-token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Agent",
    "location": "Moscow, Russia"
  }'

# Ответ:
# {
#   "agent_id": "550e8400-e29b-41d4-a716-446655440000",
#   "api_token": "generated-unique-token"
# }
```

### Запустить агента с токеном

```bash
# Docker
docker run -d \
  -e API_URL=http://backend:8000 \
  -e AGENT_TOKEN=generated-unique-token \
  -e AGENT_NAME="My Agent" \
  -e AGENT_LOCATION="Moscow, Russia" \
  hostchecker/agent:latest

# Или docker-compose
export AGENT_TOKEN=generated-unique-token
docker-compose up -d agent
```

---

## 📝 Первая проверка

### Через UI

1. Открыть http://localhost:3000
2. Ввести target: `google.com`
3. Выбрать проверки: HTTP, Ping, DNS
4. Нажать "Run Check"
5. Посмотреть результаты

### Через API

```bash
# Создать проверку
curl -X POST http://localhost:8000/api/checks \
  -H "Content-Type: application/json" \
  -d '{
    "target": "google.com",
    "checks": ["http", "ping", "dns"],
    "agents": ["all"]
  }'

# Ответ:
# {
#   "check_id": "660f9511-e29b-41d4-a716-446655440001",
#   "status": "pending"
# }

# Получить результат
curl http://localhost:8000/api/checks/660f9511-e29b-41d4-a716-446655440001
```

---

## 🐛 Troubleshooting

### Сервисы не запускаются

```bash
# Проверить логи
docker-compose logs backend
docker-compose logs frontend
docker-compose logs agent

# Перезапустить
docker-compose restart

# Полный перезапуск
docker-compose down
docker-compose up -d
```

### CORS ошибки

```bash
# Проверить настройки в backend
cat backend/app/main.py | grep CORS

# Должно быть:
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     ...
# )
```

### База данных не подключается

```bash
# Проверить PostgreSQL
docker-compose exec postgres pg_isready

# Проверить подключение
docker-compose exec backend python -c "from app.database import engine; print(engine)"

# Пересоздать БД
docker-compose down -v
docker-compose up -d postgres
docker-compose exec backend alembic upgrade head
```

### Redis не работает

```bash
# Проверить Redis
docker-compose exec redis redis-cli ping
# Должно вернуть: PONG

# Проверить очередь
docker-compose exec redis redis-cli LLEN tasks:pending
```

---

## 📦 Полезные команды

### Docker Compose

```bash
# Запуск
docker-compose up -d                 # Фоновый режим
docker-compose up                    # С выводом логов

# Остановка
docker-compose stop                  # Остановить
docker-compose down                  # Остановить и удалить
docker-compose down -v               # + удалить volumes

# Логи
docker-compose logs -f               # Все сервисы
docker-compose logs -f backend       # Конкретный сервис
docker-compose logs --tail=100       # Последние 100 строк

# Перезапуск
docker-compose restart               # Все сервисы
docker-compose restart backend       # Конкретный сервис

# Масштабирование
docker-compose up -d --scale agent=3  # 3 агента

# Exec команды
docker-compose exec backend bash     # Зайти в контейнер
docker-compose exec postgres psql -U postgres  # PostgreSQL CLI
```

### Backend (FastAPI)

```bash
# Миграции
alembic revision --autogenerate -m "Description"
alembic upgrade head
alembic downgrade -1
alembic history
alembic current

# Тестирование
pytest
pytest -v                            # Verbose
pytest tests/test_api.py            # Конкретный файл
pytest -k "test_create_check"       # Конкретный тест

# Линтинг
black app/                           # Форматирование
ruff check app/                      # Проверка
mypy app/                            # Type checking

# Dev server
uvicorn app.main:app --reload       # С автоперезагрузкой
uvicorn app.main:app --port 8001    # Другой порт
```

### Frontend (React)

```bash
# Разработка
npm run dev                          # Dev server
npm run dev -- --port 3001          # Другой порт

# Билд
npm run build                        # Production build
npm run preview                      # Превью production

# Тестирование
npm test                             # Запустить тесты
npm run test:watch                   # Watch mode

# Линтинг
npm run lint                         # ESLint
npm run format                       # Prettier
```

### Agent

```bash
# Запуск
python -m agent.main                 # Обычный режим
python -m agent.main --verbose       # С debug логами

# Тестирование отдельных проверок
python -m agent.checks.http google.com
python -m agent.checks.ping google.com
python -m agent.checks.dns google.com A
```

### База данных

```bash
# Подключение
docker-compose exec postgres psql -U postgres -d hostchecker

# SQL команды
\dt                                  # Список таблиц
\d checks                           # Описание таблицы
SELECT * FROM checks LIMIT 10;      # Запрос
\q                                  # Выход

# Бэкап
docker-compose exec postgres pg_dump -U postgres hostchecker > backup.sql

# Восстановление
docker-compose exec -T postgres psql -U postgres hostchecker < backup.sql
```

### Redis

```bash
# Подключение
docker-compose exec redis redis-cli

# Команды
PING                                 # Проверка
LLEN tasks:pending                   # Длина очереди
LPUSH tasks:pending "task"           # Добавить в очередь
RPOP tasks:pending                   # Взять из очереди
KEYS *                               # Все ключи (только для dev!)
FLUSHALL                             # Очистить всё (осторожно!)
```

---

## 🎯 Быстрые тесты

### Health check

```bash
# Backend
curl http://localhost:8000/health
# {"status":"ok","database":"connected","redis":"connected"}

# Frontend
curl http://localhost:3000
# HTML страница

# Swagger docs
open http://localhost:8000/docs
```

### Создать и проверить check

```bash
# 1. Создать проверку
CHECK_ID=$(curl -s -X POST http://localhost:8000/api/checks \
  -H "Content-Type: application/json" \
  -d '{"target":"google.com","checks":["http"],"agents":["all"]}' \
  | jq -r '.check_id')

echo "Check ID: $CHECK_ID"

# 2. Подождать 5 секунд
sleep 5

# 3. Получить результат
curl http://localhost:8000/api/checks/$CHECK_ID | jq
```

### Проверить агенты

```bash
# Список агентов
curl http://localhost:8000/api/agents | jq

# Статус конкретного агента
curl http://localhost:8000/api/agents/{agent_id} | jq

# Статистика агента
curl http://localhost:8000/api/agents/{agent_id}/stats | jq
```

---

## 📊 Мониторинг

### Логи в реальном времени

```bash
# Все сервисы цветные
docker-compose logs -f --tail=100

# Только ошибки
docker-compose logs -f | grep -i error

# Конкретный агент
docker-compose logs -f agent
```

### Метрики

```bash
# Количество проверок
curl http://localhost:8000/api/stats/checks | jq

# Количество онлайн агентов
curl http://localhost:8000/api/stats/agents | jq

# Средняя latency
curl http://localhost:8000/api/stats/latency | jq
```

### Производительность

```bash
# PostgreSQL
docker-compose exec postgres psql -U postgres -d hostchecker \
  -c "SELECT COUNT(*) FROM checks;"

# Redis
docker-compose exec redis redis-cli INFO stats

# Docker stats
docker stats
```

---

## 🔧 Настройка .env

```bash
# .env файл

# Database
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/hostchecker

# Redis
REDIS_URL=redis://redis:6379

# Backend
SECRET_KEY=your-secret-key-change-in-production
REGISTRATION_TOKEN=master-token-for-agent-registration
CORS_ORIGINS=http://localhost:3000

# Frontend
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000

# Agent
API_URL=http://backend:8000
AGENT_TOKEN=
AGENT_NAME=Local-Agent-1
AGENT_LOCATION=Local
```

---

## 🎓 Полезные ссылки

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **React Docs**: https://react.dev
- **PostgreSQL Docs**: https://postgresql.org/docs
- **Redis Docs**: https://redis.io/docs
- **Docker Compose Docs**: https://docs.docker.com/compose

---

## 💡 Pro Tips

```bash
# Алиасы для удобства
alias dc='docker-compose'
alias dcl='docker-compose logs -f'
alias dce='docker-compose exec'

# Использование
dc up -d
dcl backend
dce backend bash

# Быстрая очистка
dc down -v && dc up -d

# Пересборка образов
dc build --no-cache
dc up -d --force-recreate
```

---

**Готово! Система запущена! 🎉**

Теперь откройте http://localhost:3000 и создайте первую проверку!

