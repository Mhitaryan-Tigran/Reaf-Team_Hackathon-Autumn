# 🏗 Архитектура системы Host Checker

## 📐 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                          USER / BROWSER                             │
│                                                                     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ HTTP/HTTPS
                             │ WebSocket (опционально)
                             ↓
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                         FRONTEND (React SPA)                        │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │  Dashboard   │  │   Results    │  │    Agents    │            │
│  │              │  │    Page      │  │    Page      │            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
│                                                                     │
│  • TanStack Query (caching)                                        │
│  • Axios (HTTP client)                                             │
│  • React Router (navigation)                                       │
│  • Tailwind CSS (styling)                                          │
│                                                                     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ REST API
                             │ /api/checks
                             │ /api/agents
                             ↓
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                       BACKEND (FastAPI)                             │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                     API Layer                                 │ │
│  │                                                               │ │
│  │  POST   /api/checks           - создать проверку             │ │
│  │  GET    /api/checks/{uuid}    - получить результат           │ │
│  │  GET    /api/checks           - список проверок              │ │
│  │  POST   /api/agents/register  - регистрация агента           │ │
│  │  POST   /api/agents/heartbeat - heartbeat агента             │ │
│  │  GET    /api/agents           - список агентов               │ │
│  │  WS     /api/ws/checks/{uuid} - real-time обновления         │ │
│  │                                                               │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                   Business Logic                              │ │
│  │                                                               │ │
│  │  • TaskManager        - создание и управление задачами       │ │
│  │  • AgentManager       - управление агентами                  │ │
│  │  • ResultAggregator   - агрегация результатов                │ │
│  │  • QueueService       - работа с очередью                    │ │
│  │                                                               │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
└─────────┬──────────────────────────────────┬────────────────────────┘
          │                                  │
          │                                  │
          ↓                                  ↓
┌─────────────────────────┐       ┌─────────────────────────┐
│                         │       │                         │
│   PostgreSQL Database   │       │      Redis Server       │
│                         │       │                         │
│  ┌────────────────────┐ │       │  ┌────────────────────┐│
│  │ Tables:            │ │       │  │ Structures:        ││
│  │                    │ │       │  │                    ││
│  │ • checks           │ │       │  │ • task_queue       ││
│  │ • agents           │ │       │  │   (List/Stream)    ││
│  │ • check_tasks      │ │       │  │                    ││
│  │ • check_results    │ │       │  │ • agent:{id}:hb    ││
│  │                    │ │       │  │   (Hash)           ││
│  └────────────────────┘ │       │  │                    ││
│                         │       │  │ • check:{id}:stat  ││
│  • Persistent storage   │       │  │   (Hash)           ││
│  • JSONB для гибкости   │       │  │                    ││
│  • UUID primary keys    │       │  │ • pub/sub channels ││
│  • Индексы для поиска   │       │  │                    ││
│                         │       │  └────────────────────┘│
└─────────────────────────┘       │                         │
                                  │  • In-memory queue      │
                                  │  • Caching              │
                                  │  • Pub/Sub              │
                                  │                         │
                                  └────────┬────────────────┘
                                           │
                                           │ Poll tasks
                                           │ (BRPOP/XREAD)
                                           │
                                           ↓
                        ┌──────────────────────────────────┐
                        │                                  │
                        │        AGENTS (Distributed)      │
                        │                                  │
                        │  ┌────────────────────────────┐ │
                        │  │  Agent 1 (Moscow, RU)      │ │
                        │  │  • HTTP Check              │ │
                        │  │  • Ping Check              │ │
                        │  │  • DNS Check               │ │
                        │  │  • TCP Check               │ │
                        │  │  • Traceroute              │ │
                        │  └────────────────────────────┘ │
                        │                                  │
                        │  ┌────────────────────────────┐ │
                        │  │  Agent 2 (London, UK)      │ │
                        │  │  • Same checks             │ │
                        │  └────────────────────────────┘ │
                        │                                  │
                        │  ┌────────────────────────────┐ │
                        │  │  Agent 3 (Tokyo, JP)       │ │
                        │  │  • Same checks             │ │
                        │  └────────────────────────────┘ │
                        │                                  │
                        │  • Poll Redis queue             │
                        │  • Execute checks locally       │
                        │  • Send results to backend      │
                        │  • Heartbeat every 10s          │
                        │                                  │
                        └──────────────────────────────────┘
```

---

## 🔄 Data Flow

### 1. Создание проверки (Check Creation)

```
User Input (Frontend)
    │
    │ 1. Заполняет форму
    │    { target: "google.com", checks: ["http", "ping"] }
    │
    ↓
POST /api/checks (Backend)
    │
    │ 2. Создаёт запись в БД
    │    check_id = UUID
    │    status = "pending"
    │
    ↓
Database (PostgreSQL)
    │
    │ 3. Сохраняет check
    │
    ↓
Task Creation Logic
    │
    │ 4. Для каждого агента и каждого типа проверки
    │    создаёт задачу:
    │    {
    │      task_id: UUID,
    │      check_id: UUID,
    │      agent_id: UUID,
    │      check_type: "http",
    │      target: "google.com"
    │    }
    │
    ↓
Redis Queue (LPUSH)
    │
    │ 5. Добавляет задачи в очередь
    │    tasks:pending
    │
    ↓
Response to Frontend
    │
    │ 6. Возвращает check_id
    │    { check_id: "550e8400-..." }
    │
    ↓
Frontend
    │
    │ 7. Редирект на /results/{check_id}
    │
    ✓
```

### 2. Выполнение проверки (Check Execution)

```
Agent (Polling Loop)
    │
    │ 1. BRPOP tasks:pending (blocking)
    │
    ↓
Get Task from Redis
    │
    │ 2. Получает задачу
    │    {
    │      task_id: UUID,
    │      check_type: "http",
    │      target: "google.com"
    │    }
    │
    ↓
Update Task Status
    │
    │ 3. POST /api/tasks/{task_id}/start
    │    status = "in_progress"
    │
    ↓
Execute Check
    │
    │ 4. В зависимости от check_type:
    │    
    │    if check_type == "http":
    │      response = requests.get(target)
    │      result = {
    │        status_code: 200,
    │        duration_ms: 45,
    │        headers: {...}
    │      }
    │    
    │    elif check_type == "ping":
    │      latency = ping3.ping(target)
    │      result = {
    │        latency_ms: 23.5,
    │        success: true
    │      }
    │
    ↓
Send Result
    │
    │ 5. POST /api/tasks/{task_id}/result
    │    {
    │      task_id: UUID,
    │      success: true,
    │      data: {...},
    │      duration_ms: 45
    │    }
    │
    ↓
Backend Processing
    │
    │ 6. Сохраняет результат в БД
    │    Обновляет статус задачи
    │    Проверяет, все ли задачи выполнены
    │
    ↓
Check Completion
    │
    │ 7. Если все задачи готовы:
    │    check.status = "completed"
    │    check.completed_at = NOW()
    │
    ↓
Notification (Optional)
    │
    │ 8. Если WebSocket активен:
    │    redis.publish(f"check:{check_id}", result)
    │    → WebSocket → Frontend
    │
    ✓
```

### 3. Просмотр результатов (View Results)

```
Frontend
    │
    │ 1. GET /api/checks/{check_id}
    │    (каждые 2 секунды или через WebSocket)
    │
    ↓
Backend
    │
    │ 2. SELECT * FROM checks
    │    JOIN check_results ON ...
    │    WHERE check_id = {check_id}
    │
    ↓
Database
    │
    │ 3. Возвращает check с results
    │
    ↓
Response
    │
    │ 4. {
    │      check_id: UUID,
    │      target: "google.com",
    │      status: "completed",
    │      results: [
    │        {
    │          agent: "Moscow",
    │          check_type: "http",
    │          success: true,
    │          data: {...}
    │        },
    │        ...
    │      ]
    │    }
    │
    ↓
Frontend
    │
    │ 5. Отображает результаты в таблице
    │
    ✓
```

### 4. Heartbeat агента (Agent Heartbeat)

```
Agent (Every 10 seconds)
    │
    │ 1. POST /api/agents/heartbeat
    │    {
    │      agent_id: UUID,
    │      token: "xxx",
    │      current_tasks: 2
    │    }
    │
    ↓
Backend
    │
    │ 2. Проверяет токен
    │    Обновляет last_heartbeat
    │    Устанавливает status = "online"
    │
    ↓
Redis (Cache)
    │
    │ 3. SETEX agent:{agent_id}:heartbeat
    │    { timestamp: NOW(), status: "online" }
    │    TTL = 30 seconds
    │
    ↓
Database
    │
    │ 4. UPDATE agents
    │    SET last_heartbeat = NOW()
    │    WHERE id = {agent_id}
    │
    ↓
Background Job (каждые 30 секунд)
    │
    │ 5. Проверяет все агенты:
    │    IF NOW() - last_heartbeat > 30s:
    │      agent.status = "offline"
    │
    ✓
```

---

## 🗄️ Database Schema

### Tables

```sql
-- Checks (проверки)
CREATE TABLE checks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    target VARCHAR(255) NOT NULL,
    check_types JSONB NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('pending', 'in_progress', 'completed', 'failed')),
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    created_by_user_id UUID REFERENCES users(id),
    
    INDEX idx_checks_status (status),
    INDEX idx_checks_created_at (created_at DESC)
);

-- Agents (агенты проверки)
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    api_token VARCHAR(255) UNIQUE NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('online', 'offline')),
    last_heartbeat TIMESTAMP,
    registered_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB DEFAULT '{}',
    
    INDEX idx_agents_status (status),
    INDEX idx_agents_token (api_token)
);

-- Check Tasks (задачи для агентов)
CREATE TABLE check_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    check_id UUID NOT NULL REFERENCES checks(id) ON DELETE CASCADE,
    agent_id UUID NOT NULL REFERENCES agents(id),
    check_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('pending', 'in_progress', 'completed', 'failed')),
    created_at TIMESTAMP DEFAULT NOW(),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    
    INDEX idx_tasks_check_id (check_id),
    INDEX idx_tasks_agent_id (agent_id),
    INDEX idx_tasks_status (status)
);

-- Check Results (результаты проверок)
CREATE TABLE check_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID NOT NULL REFERENCES check_tasks(id) ON DELETE CASCADE,
    check_id UUID NOT NULL REFERENCES checks(id) ON DELETE CASCADE,
    agent_id UUID NOT NULL REFERENCES agents(id),
    check_type VARCHAR(50) NOT NULL,
    success BOOLEAN NOT NULL,
    data JSONB NOT NULL,
    error TEXT,
    duration_ms INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_results_check_id (check_id),
    INDEX idx_results_agent_id (agent_id),
    INDEX idx_results_success (success)
);
```

### Sample Data

**checks**
| id | target | check_types | status | created_at |
|----|--------|-------------|--------|------------|
| 550e8400... | google.com | ["http","ping"] | completed | 2024-01-15 10:00:00 |

**agents**
| id | name | location | status | last_heartbeat |
|----|------|----------|--------|----------------|
| 660f9511... | Moscow-1 | Moscow, Russia | online | 2024-01-15 10:05:00 |
| 770a0622... | London-1 | London, UK | online | 2024-01-15 10:05:02 |

**check_results**
| id | check_id | agent_id | check_type | success | data | duration_ms |
|----|----------|----------|------------|---------|------|-------------|
| 880b1733... | 550e8400... | 660f9511... | http | true | {"status_code": 200} | 45 |
| 990c2844... | 550e8400... | 770a0622... | http | true | {"status_code": 200} | 120 |

---

## 🔌 API Endpoints

### Checks

```
POST   /api/checks
GET    /api/checks
GET    /api/checks/{check_id}
DELETE /api/checks/{check_id}
```

### Agents

```
GET    /api/agents
POST   /api/agents/register
POST   /api/agents/heartbeat
GET    /api/agents/{agent_id}
GET    /api/agents/{agent_id}/stats
```

### Tasks (Internal)

```
POST   /api/tasks/{task_id}/start
POST   /api/tasks/{task_id}/result
GET    /api/tasks/{task_id}
```

### WebSocket

```
WS     /api/ws/checks/{check_id}
```

---

## 🔐 Security

### Agent Authentication

```python
# Registration
POST /api/agents/register
Headers:
  X-Registration-Token: secret-master-token
Body:
  {
    "name": "Moscow-1",
    "location": "Moscow, Russia"
  }
Response:
  {
    "agent_id": "uuid",
    "api_token": "generated-unique-token"
  }

# All subsequent requests
Headers:
  X-Agent-Token: generated-unique-token
```

### Rate Limiting

```python
# Redis-based rate limiting
# Max 100 checks per IP per hour

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    ip = request.client.host
    key = f"rate_limit:{ip}"
    
    current = await redis.incr(key)
    if current == 1:
        await redis.expire(key, 3600)
    
    if current > 100:
        raise HTTPException(status_code=429, detail="Too many requests")
    
    return await call_next(request)
```

---

## 📦 Deployment

### Docker Compose (Production)

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: hostchecker
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    restart: always

  backend:
    image: hostchecker/backend:latest
    environment:
      DATABASE_URL: postgresql://postgres:${DB_PASSWORD}@postgres/hostchecker
      REDIS_URL: redis://:${REDIS_PASSWORD}@redis:6379
      SECRET_KEY: ${SECRET_KEY}
      REGISTRATION_TOKEN: ${REGISTRATION_TOKEN}
    depends_on:
      - postgres
      - redis
    restart: always
    deploy:
      replicas: 2

  frontend:
    image: hostchecker/frontend:latest
    environment:
      VITE_API_URL: ${API_URL}
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend
    restart: always

volumes:
  postgres_data:
  redis_data:
```

### Scaling Agents

```bash
# Запустить 3 агента в разных локациях

# Agent 1 (Moscow)
docker run -d \
  -e API_URL=https://api.hostchecker.com \
  -e AGENT_TOKEN=${MOSCOW_TOKEN} \
  -e AGENT_NAME="Moscow-1" \
  -e AGENT_LOCATION="Moscow, Russia" \
  hostchecker/agent:latest

# Agent 2 (London)
docker run -d \
  -e API_URL=https://api.hostchecker.com \
  -e AGENT_TOKEN=${LONDON_TOKEN} \
  -e AGENT_NAME="London-1" \
  -e AGENT_LOCATION="London, UK" \
  hostchecker/agent:latest

# Agent 3 (Tokyo)
docker run -d \
  -e API_URL=https://api.hostchecker.com \
  -e AGENT_TOKEN=${TOKYO_TOKEN} \
  -e AGENT_NAME="Tokyo-1" \
  -e AGENT_LOCATION="Tokyo, Japan" \
  hostchecker/agent:latest
```

---

## 🚀 Performance Considerations

### Backend Optimization

```python
# 1. Connection pooling
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True
)

# 2. Caching с Redis
@cache(ttl=60)
async def get_agent_stats(agent_id: UUID):
    # Expensive query
    pass

# 3. Async everywhere
async def execute_checks_parallel(tasks: List[Task]):
    results = await asyncio.gather(*[
        execute_check(task) for task in tasks
    ])
    return results
```

### Database Optimization

```sql
-- Indexes для быстрых запросов
CREATE INDEX idx_checks_status ON checks(status);
CREATE INDEX idx_results_check_id ON check_results(check_id);
CREATE INDEX idx_agents_status ON agents(status);

-- Partitioning для старых данных (optional)
CREATE TABLE check_results_2024_01 PARTITION OF check_results
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

### Redis Optimization

```python
# Использовать pipelines для bulk операций
async with redis.pipeline() as pipe:
    for task in tasks:
        pipe.lpush('tasks:pending', json.dumps(task))
    await pipe.execute()

# Streams вместо Lists для масштабируемости
await redis.xadd('tasks:stream', {
    'task_id': task_id,
    'data': json.dumps(task_data)
})
```

---

## 📊 Monitoring

### Health Checks

```python
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "database": await check_db_connection(),
        "redis": await check_redis_connection(),
        "active_agents": await count_online_agents()
    }
```

### Metrics (Prometheus)

```python
from prometheus_client import Counter, Histogram

checks_total = Counter('checks_total', 'Total checks created')
check_duration = Histogram('check_duration_seconds', 'Check duration')
agent_heartbeats = Counter('agent_heartbeats_total', 'Agent heartbeats')
```

---

**Это полная архитектура системы! 🎯**

