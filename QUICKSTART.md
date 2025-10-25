# ⚡ Quick Start Guide

Быстрый старт для локальной разработки и тестирования.

## 📋 Требования

- Python 3.13+
- Node.js 18+
- Docker & Docker Compose (для БД)
- Git

## 🚀 Локальный запуск за 5 минут

### Шаг 1: Клонирование репозитория

```bash
git clone <your-repo-url>
cd Reaf-Team_Hackathon-Autumn
```

### Шаг 2: Запуск БД (Docker)

```bash
# PostgreSQL
docker run -d --name hostchecker-postgres \
  -e POSTGRES_PASSWORD=hakatonski123 \
  -e POSTGRES_USER=SERVER \
  -e POSTGRES_DB=serverDB \
  -p 5432:5432 \
  postgres:latest

# Redis
docker run -d --name hostchecker-redis \
  -p 6379:6379 \
  redis:latest

# Проверка
docker ps
```

### Шаг 3: Инициализация БД

```bash
# Установите psql если нужно
# macOS: brew install postgresql
# Ubuntu: sudo apt install postgresql-client

# Выполните миграцию
psql -h localhost -U SERVER -d serverDB -f database_migration.sql
```

### Шаг 4: Backend

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск backend
python -m uvicorn backend_main:app --reload --port 8000
```

✅ Backend: http://localhost:8000  
📖 API Docs: http://localhost:8000/docs

### Шаг 5: Frontend

Откройте новый терминал:

```bash
cd frontend

# Установка зависимостей
npm install

# Создайте .env файл
echo "VITE_API_URL=http://localhost:8000" > .env

# Запуск
npm run dev
```

✅ Frontend: http://localhost:3000

### Шаг 6: Agent (опционально)

Откройте еще один терминал:

```bash
# Настройте переменные
export MAIN_SERVER_URL=http://localhost:8000
export AGENT_COUNTRY=Russia
export AGENT_NAME=Agent-Local
export AGENT_UIID=local-agent-001
export AGENT_API_TOKEN=local-token

# Запуск
python -m uvicorn agent_production:app --reload --port 8001
```

✅ Agent: http://localhost:8001

## 🧪 Тестирование

### Регистрация агента

```bash
curl -X POST http://localhost:8000/api/agents/register \
  -H "Content-Type: application/json" \
  -H "X-Registration-Token: master-registration-token" \
  -d '{
    "name": "Test Agent",
    "location": "Local Machine",
    "metadata": {"test": true}
  }'
```

Сохраните `agent_id` и `api_token` из ответа.

### Создание проверки

```bash
curl -X POST http://localhost:8000/api/checks \
  -H "Content-Type: application/json" \
  -d '{
    "target": "google.com",
    "checks": ["http", "ping", "dns"]
  }'
```

Сохраните `id` проверки.

### Просмотр результатов

```bash
curl http://localhost:8000/api/checks/{check_id}
```

## 🔧 Troubleshooting

### PostgreSQL не подключается

```bash
# Проверьте статус контейнера
docker ps -a | grep postgres

# Посмотрите логи
docker logs hostchecker-postgres

# Перезапустите
docker restart hostchecker-postgres
```

### Redis не работает

```bash
# Проверка
docker ps -a | grep redis

# Тест подключения
redis-cli -h localhost -p 6379 ping
# Ожидаемый ответ: PONG
```

### Frontend не видит backend

Проверьте `.env` файл в `frontend/`:
```env
VITE_API_URL=http://localhost:8000
```

### Agent не получает задачи

1. Убедитесь, что `AGENT_UIID` совпадает с зарегистрированным агентом
2. Проверьте логи backend'а
3. Убедитесь, что agent отправил heartbeat:

```bash
curl -X POST http://localhost:8000/api/agents/heartbeat \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "your-agent-id"}'
```

## 📊 Полезные команды

### Backend

```bash
# Запуск с автоперезагрузкой
uvicorn backend_main:app --reload

# Запуск на другом порту
uvicorn backend_main:app --port 8080

# Запуск с логами
uvicorn backend_main:app --log-level debug
```

### Frontend

```bash
# Dev сервер
npm run dev

# Build для production
npm run build

# Preview production build
npm run preview

# Линтинг
npm run lint
```

### Database

```bash
# Подключение к БД
psql -h localhost -U SERVER -d serverDB

# Список таблиц
\dt

# Просмотр схемы таблицы
\d agents

# Просмотр данных
SELECT * FROM agents;
SELECT * FROM checks ORDER BY created_at DESC LIMIT 10;

# Очистка старых проверок (>30 дней)
SELECT cleanup_old_checks(30);
```

### Docker

```bash
# Остановить все контейнеры
docker stop hostchecker-postgres hostchecker-redis

# Удалить контейнеры
docker rm hostchecker-postgres hostchecker-redis

# Удалить volumes
docker volume prune

# Логи
docker logs -f hostchecker-postgres
```

## 🎉 Готово!

Теперь у вас запущена полная локальная версия Host Checker!

**Следующие шаги:**
- 📖 Прочитайте [DEPLOYMENT.md](./DEPLOYMENT.md) для деплоя в production
- 🏗 Изучите [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) для понимания архитектуры
- 🔧 Посмотрите [API документацию](http://localhost:8000/docs)

**Полезные ссылки:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Agent: http://localhost:8001

