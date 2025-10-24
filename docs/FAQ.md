# ❓ FAQ - Частые вопросы

## 📚 Содержание

- [Общие вопросы](#-общие-вопросы)
- [Технические вопросы](#-технические-вопросы)
- [Проблемы и решения](#-проблемы-и-решения)
- [Оптимизация](#-оптимизация)
- [Развёртывание](#-развёртывание)

---

## 🎯 Общие вопросы

### Это реально сделать за хакатон?

**Да!** MVP (минимальная рабочая версия) реализуется за **12-16 часов** при правильном подходе:
- Backend (FastAPI): 5 часов
- Agent: 4 часа
- Frontend: 5 часов
- Docker + Docs: 2 часа

### Какой стек самый оптимальный?

```
✅ Backend:  FastAPI (Python)
✅ Frontend: React + TypeScript
✅ Database: PostgreSQL
✅ Queue:    Redis
✅ Agent:    Python CLI
✅ Deploy:   Docker Compose
```

**Почему?** Быстрая разработка + много готовых библиотек + хорошая документация.

### Нужен ли опыт с Docker?

Базовый опыт достаточно. Основные команды:
```bash
docker-compose up -d      # Запустить
docker-compose logs -f    # Логи
docker-compose down       # Остановить
```

### Сколько агентов нужно для демо?

**Минимум 1, оптимально 2-3** для демонстрации распределённости.

Можно запустить несколько агентов локально с разными именами:
```bash
docker-compose up -d --scale agent=3
```

---

## 🔧 Технические вопросы

### Как реализовать ping без sudo?

**Вариант 1:** Библиотека `ping3`
```python
import ping3

# Автоматически использует ICMP socket или fallback
latency = ping3.ping('google.com', timeout=2)
```

**Вариант 2:** Системный вызов
```python
import subprocess

result = subprocess.run(
    ['ping', '-c', '1', target],
    capture_output=True,
    timeout=5
)
success = result.returncode == 0
```

**Вариант 3:** TCP-based ping (fallback)
```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(2)
result = sock.connect_ex((target, 80))
success = result == 0
```

### Как работает очередь задач на Redis?

**Подход 1: Lists (простой)**
```python
# Backend: добавить задачу
await redis.lpush('tasks:pending', json.dumps(task))

# Agent: получить задачу (blocking)
task_json = await redis.brpop('tasks:pending', timeout=5)
task = json.loads(task_json[1])
```

**Подход 2: Streams (масштабируемый)**
```python
# Backend: добавить задачу
await redis.xadd('tasks', {'data': json.dumps(task)})

# Agent: читать задачи
messages = await redis.xread(
    {'tasks': last_id},
    count=10,
    block=5000
)
```

**Подход 3: Pub/Sub (real-time)**
```python
# Backend: публиковать
await redis.publish('tasks:new', json.dumps(task))

# Agent: подписаться
async for message in redis.subscribe('tasks:new'):
    task = json.loads(message['data'])
```

**Рекомендация:** Начать с Lists, при необходимости перейти на Streams.

### Как реализовать heartbeat?

**Backend:**
```python
@router.post("/agents/heartbeat")
async def heartbeat(
    agent_id: UUID,
    token: str = Header(alias="X-Agent-Token")
):
    # Проверить токен
    agent = await get_agent_by_token(token)
    
    # Обновить timestamp
    agent.last_heartbeat = datetime.now()
    await db.commit()
    
    # Кэш в Redis (TTL 30s)
    await redis.setex(
        f"agent:{agent_id}:heartbeat",
        30,
        json.dumps({"status": "online"})
    )
    
    return {"status": "ok"}
```

**Agent:**
```python
async def heartbeat_loop():
    while True:
        try:
            await api_client.post(
                '/agents/heartbeat',
                headers={'X-Agent-Token': TOKEN}
            )
        except Exception as e:
            logger.error(f"Heartbeat failed: {e}")
        
        await asyncio.sleep(10)  # каждые 10 секунд
```

**Проверка offline:**
```python
# Background task каждые 30 секунд
async def check_offline_agents():
    threshold = datetime.now() - timedelta(seconds=30)
    
    offline_agents = await db.query(Agent).filter(
        Agent.last_heartbeat < threshold,
        Agent.status == 'online'
    ).all()
    
    for agent in offline_agents:
        agent.status = 'offline'
    
    await db.commit()
```

### Как хранить результаты проверок?

**PostgreSQL с JSONB:**
```sql
CREATE TABLE check_results (
    id UUID PRIMARY KEY,
    check_id UUID NOT NULL,
    agent_id UUID NOT NULL,
    check_type VARCHAR(50),
    success BOOLEAN,
    data JSONB,  -- Гибкое хранение любых данных
    duration_ms INTEGER,
    created_at TIMESTAMP
);

-- Пример данных
{
  "check_type": "http",
  "data": {
    "status_code": 200,
    "headers": {
      "content-type": "text/html",
      "server": "nginx"
    },
    "body_size": 12345,
    "ssl_info": {
      "valid": true,
      "expires": "2025-12-31"
    }
  }
}
```

**Преимущества JSONB:**
- ✅ Гибкость (любые поля)
- ✅ Индексы (GIN)
- ✅ Запросы (JSON operators)

```sql
-- Поиск по вложенным полям
SELECT * FROM check_results
WHERE data->>'status_code' = '200';

-- Индекс для производительности
CREATE INDEX idx_results_data ON check_results USING GIN (data);
```

### Нужна ли аутентификация пользователей?

**Для MVP: необязательно** (можно сделать публичный сервис)

**Для production: желательно**

**Простой вариант:**
```python
# API token authentication
async def verify_api_key(
    api_key: str = Header(alias="X-API-Key")
):
    if api_key != VALID_API_KEY:
        raise HTTPException(401, "Invalid API key")
    return api_key

@router.post("/checks", dependencies=[Depends(verify_api_key)])
async def create_check(...):
    pass
```

**Полноценный вариант:**
```bash
# OAuth2 / JWT
pip install python-jose[cryptography] passlib[bcrypt]
```

---

## 🐛 Проблемы и решения

### CORS блокирует frontend

**Проблема:**
```
Access to XMLHttpRequest blocked by CORS policy
```

**Решение:**
```python
# backend/app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Ping не работает в Docker

**Проблема:**
```
Operation not permitted
```

**Решение 1:** Добавить capabilities
```yaml
# docker-compose.yml
services:
  agent:
    cap_add:
      - NET_RAW
      - NET_ADMIN
```

**Решение 2:** Использовать TCP fallback
```python
def ping_fallback(target):
    # Вместо ICMP ping делаем TCP connect
    sock = socket.create_connection((target, 80), timeout=2)
    sock.close()
    return True
```

### Redis connection refused

**Проблема:**
```
ConnectionRefusedError: [Errno 111] Connection refused
```

**Решение:** Проверить networking в Docker Compose
```yaml
services:
  backend:
    depends_on:
      - redis
    environment:
      REDIS_URL: redis://redis:6379  # Не localhost!
```

### Database migrations failing

**Проблема:**
```
alembic.util.exc.CommandError: Target database is not up to date
```

**Решение:**
```bash
# 1. Проверить текущую версию
alembic current

# 2. Сгенерировать миграцию
alembic revision --autogenerate -m "description"

# 3. Применить
alembic upgrade head

# 4. Если нужен rollback
alembic downgrade -1
```

### Frontend не видит backend

**Проблема:**
```
Network Error
```

**Проверки:**
```bash
# 1. Backend запущен?
curl http://localhost:8000/health

# 2. Правильный URL в frontend?
# frontend/.env
VITE_API_URL=http://localhost:8000

# 3. CORS настроен?
# См. выше

# 4. Proxy в Vite (альтернатива)
# vite.config.ts
export default defineConfig({
  server: {
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
})
```

### Агент не получает задачи

**Проблема:** Агент запущен, но ничего не делает

**Debug:**
```python
# agent/main.py
async def main():
    logger.info("Agent started")
    
    while True:
        logger.info("Polling for tasks...")
        
        task = await redis.brpop('tasks:pending', timeout=5)
        
        if task:
            logger.info(f"Got task: {task}")
            # Process...
        else:
            logger.debug("No tasks available")
        
        await asyncio.sleep(1)
```

**Проверки:**
```bash
# 1. Redis доступен?
docker-compose exec agent redis-cli -h redis ping

# 2. Задачи в очереди?
redis-cli LLEN tasks:pending

# 3. Агент зарегистрирован?
curl http://localhost:8000/api/agents
```

---

## ⚡ Оптимизация

### Как ускорить проверки?

**1. Параллельное выполнение**
```python
async def execute_multiple_checks(tasks: List[Task]):
    results = await asyncio.gather(*[
        execute_check(task) for task in tasks
    ], return_exceptions=True)
    return results
```

**2. Timeout для медленных хостов**
```python
try:
    async with asyncio.timeout(5):  # Python 3.11+
        result = await check_http(target)
except asyncio.TimeoutError:
    result = {"error": "Timeout"}
```

**3. Connection pooling**
```python
# Переиспользовать сессии
session = aiohttp.ClientSession()

async def check_http(target):
    async with session.get(target) as resp:
        return await resp.json()

# При завершении
await session.close()
```

### Как масштабировать систему?

**Горизонтальное масштабирование:**

```yaml
# docker-compose.yml
services:
  backend:
    deploy:
      replicas: 3  # 3 инстанса backend
  
  agent:
    deploy:
      replicas: 5  # 5 агентов
  
  nginx:
    # Load balancer
    upstream backend {
      server backend:8000;
    }
```

**Разделение задач:**
```
Redis Queue 1: HTTP checks
Redis Queue 2: Ping checks
Redis Queue 3: DNS checks

Agent 1-5: только HTTP
Agent 6-10: только Ping
Agent 11-15: только DNS
```

**Кэширование:**
```python
@cache(ttl=300)  # 5 минут
async def get_dns_records(domain: str):
    # Дорогой DNS lookup
    pass
```

### Как уменьшить нагрузку на БД?

**1. Batch inserts**
```python
# Плохо: 100 отдельных INSERT
for result in results:
    await db.add(result)
    await db.commit()

# Хорошо: 1 batch INSERT
await db.bulk_insert_mappings(CheckResult, results)
await db.commit()
```

**2. Кэширование в Redis**
```python
# Кэшировать частые запросы
@cache(ttl=60)
async def get_check_results(check_id: UUID):
    return await db.query(CheckResult).filter_by(check_id=check_id).all()
```

**3. Индексы**
```sql
CREATE INDEX idx_results_check_id ON check_results(check_id);
CREATE INDEX idx_results_created_at ON check_results(created_at DESC);
```

**4. Партиционирование (для больших объёмов)**
```sql
-- Разделить по датам
CREATE TABLE check_results_2024_01 PARTITION OF check_results
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

---

## 🚀 Развёртывание

### Как запустить локально для разработки?

```bash
# 1. Клонировать репо
git clone <repo>
cd host-checker

# 2. Запустить инфраструктуру
docker-compose up -d postgres redis

# 3. Backend
cd backend
poetry install
poetry run alembic upgrade head
poetry run uvicorn app.main:app --reload

# 4. Frontend
cd frontend
npm install
npm run dev

# 5. Agent
cd agent
poetry install
export AGENT_TOKEN=xxx
poetry run python -m agent.main
```

### Как задеплоить на production?

**VPS (DigitalOcean, Hetzner, AWS):**

```bash
# 1. Подключиться к серверу
ssh user@server

# 2. Установить Docker
curl -fsSL https://get.docker.com | sh

# 3. Клонировать и настроить
git clone <repo>
cd host-checker
cp .env.example .env
nano .env  # Заполнить переменные

# 4. Запустить
docker-compose -f docker-compose.prod.yml up -d

# 5. Настроить Nginx (опционально)
sudo apt install nginx
sudo nano /etc/nginx/sites-available/hostchecker
sudo ln -s /etc/nginx/sites-available/hostchecker /etc/nginx/sites-enabled/
sudo systemctl reload nginx

# 6. SSL (Let's Encrypt)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d hostchecker.com
```

**Docker Swarm (кластер):**
```bash
# Инициализировать Swarm
docker swarm init

# Деплой
docker stack deploy -c docker-compose.prod.yml hostchecker

# Масштабирование
docker service scale hostchecker_backend=3
docker service scale hostchecker_agent=10
```

**Kubernetes (advanced):**
```bash
# Создать deployment
kubectl apply -f k8s/

# Масштабирование
kubectl scale deployment backend --replicas=5
```

### Как регистрировать агенты в production?

**Шаг 1: Получить токен (админ)**
```bash
curl -X POST http://api.hostchecker.com/api/agents/register \
  -H "X-Registration-Token: master-secret-token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tokyo-Agent-1",
    "location": "Tokyo, Japan"
  }'

# Response:
{
  "agent_id": "uuid",
  "api_token": "generated-token-xyz"
}
```

**Шаг 2: Запустить агента**
```bash
docker run -d \
  --name tokyo-agent-1 \
  --restart always \
  -e API_URL=https://api.hostchecker.com \
  -e AGENT_TOKEN=generated-token-xyz \
  -e AGENT_NAME=Tokyo-Agent-1 \
  -e AGENT_LOCATION="Tokyo, Japan" \
  hostchecker/agent:latest
```

**Шаг 3: Проверить статус**
```bash
curl http://api.hostchecker.com/api/agents
```

### Как мониторить систему?

**Логи:**
```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f backend

# Последние 100 строк
docker-compose logs --tail=100 backend
```

**Health checks:**
```bash
# Backend
curl http://localhost:8000/health

# Database
docker-compose exec postgres pg_isready

# Redis
docker-compose exec redis redis-cli ping
```

**Metrics (Prometheus):**
```yaml
# docker-compose.yml
services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
  
  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
```

---

## 💡 Советы для хакатона

### Приоритизация

**Must Have (делать в первую очередь):**
1. ✅ Backend API (checks + agents)
2. ✅ Agent core + HTTP check
3. ✅ Frontend form + results
4. ✅ Docker Compose
5. ✅ README

**Nice to Have (если останется время):**
1. 🟡 WebSocket real-time
2. 🟡 Ping check
3. 🟡 DNS check
4. 🟡 TCP check

**Optional (бонус):**
1. ⚪ Traceroute
2. ⚪ GeoIP
3. ⚪ Metrics

### Тайм-менеджмент

```
День 1 (8 часов):
  09:00-13:00: Backend + Agent
  13:00-14:00: Обед
  14:00-18:00: Frontend + Docker

День 2 (6 часов):
  09:00-12:00: Polish + Bug fixes
  12:00-13:00: Обед
  13:00-15:00: Документация
  15:00-16:00: Презентация
```

### Чеклист перед сдачей

- [ ] `docker-compose up` запускает всё
- [ ] README с инструкциями
- [ ] Демо работает стабильно
- [ ] Все базовые проверки работают
- [ ] UI интуитивный
- [ ] Код закоммичен
- [ ] Презентация готова

---

## 📞 Помощь

Если застряли:

1. **GitHub Issues** - посмотреть похожие проблемы
2. **Stack Overflow** - поиск по ошибке
3. **ChatGPT / Cursor** - AI помощник
4. **Документация** - FastAPI/React/Redis docs
5. **Куратор** - @daedal_dev (Telegram)

---

**Удачи! Вы справитесь! 💪**

