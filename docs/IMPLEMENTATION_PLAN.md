# 📋 Детальный план реализации

## 🎯 Оптимальный стек (Финальное решение)

### ✅ Рекомендуемый стек для быстрой реализации:

```
Backend:    FastAPI (Python 3.11+)
Frontend:   React 18 + TypeScript + Vite
Database:   PostgreSQL 15
Queue:      Redis 7
Agent:      Python 3.11+
Deploy:     Docker + Docker Compose
```

### 🔍 Обоснование выбора:

| Компонент | Альтернативы | Выбрано | Почему? |
|-----------|--------------|---------|---------|
| **Backend** | Django, Express.js, Go | **FastAPI** | • Быстрая разработка<br>• Автодокументация<br>• Async из коробки<br>• WebSocket поддержка |
| **Frontend** | Vue, Svelte, Angular | **React** | • Большое комьюнити<br>• Много готовых библиотек<br>• TypeScript интеграция |
| **Database** | MongoDB, MySQL | **PostgreSQL** | • JSONB для гибкости<br>• Надёжность<br>• UUID поддержка |
| **Queue** | RabbitMQ, Kafka | **Redis** | • Простота настройки<br>• Pub/Sub + Cache<br>• Легковесность |
| **Agent** | Go, Node.js | **Python** | • Много библиотек для сетевых проверок<br>• Быстрая разработка |

---

## ⏱ Детальная оценка времени

### Минимальная рабочая версия (MVP): **12-16 часов**

| Этап | Задачи | Время | Приоритет |
|------|--------|-------|-----------|
| **Backend Core** | FastAPI setup, models, migrations | 2 ч | 🔴 Critical |
| **Backend API** | Endpoints для checks и agents | 3 ч | 🔴 Critical |
| **Redis Queue** | Task queue, pub/sub | 1 ч | 🔴 Critical |
| **Agent Core** | Основной цикл, heartbeat | 2 ч | 🔴 Critical |
| **Checks Implementation** | HTTP, Ping, DNS | 2 ч | 🔴 Critical |
| **Frontend Setup** | React, routing, базовый UI | 2 ч | 🔴 Critical |
| **Frontend Components** | Forms, results, agents list | 3 ч | 🔴 Critical |
| **Docker Setup** | Compose, Dockerfiles | 1 ч | 🔴 Critical |
| **Documentation** | README, инструкции | 1 ч | 🔴 Critical |
| **Testing & Fixes** | Баги, polish | 2 ч | 🔴 Critical |

### С дополнительными фичами: **20-24 часа**

| Фича | Время | ROI | Приоритет |
|------|-------|-----|-----------|
| WebSocket real-time | 2-3 ч | ⭐⭐⭐⭐⭐ | 🟡 High |
| TCP Port check | 0.5 ч | ⭐⭐⭐⭐ | 🟡 High |
| Traceroute | 2 ч | ⭐⭐⭐⭐ | 🟡 High |
| Rate limiting | 1 ч | ⭐⭐⭐ | 🟢 Medium |
| Шаблоны проверок | 1.5 ч | ⭐⭐⭐⭐ | 🟢 Medium |
| GeoIP визуализация | 3 ч | ⭐⭐⭐⭐⭐ | 🟡 High |
| Метрики/статистика | 2 ч | ⭐⭐⭐ | 🟢 Medium |
| Авторизация/auth | 2 ч | ⭐⭐ | ⚪ Low |

---

## 📋 Пошаговый план разработки

### Phase 1: Backend Foundation (4-5 часов)

#### 1.1 Инициализация проекта (30 мин)
```bash
# Создать структуру
mkdir -p backend/app/{models,schemas,api,services,utils}
cd backend

# Poetry setup
poetry init
poetry add fastapi uvicorn sqlalchemy psycopg2-binary alembic redis pydantic-settings
poetry add --group dev pytest black ruff

# Создать базовые файлы
touch app/{__init__,main,config,database}.py
```

**Файлы:**
- [x] `pyproject.toml` - зависимости
- [x] `app/main.py` - FastAPI app
- [x] `app/config.py` - настройки
- [x] `app/database.py` - SQLAlchemy setup

#### 1.2 Модели БД (1 час)
```python
# app/models/check.py
class Check(Base):
    id: UUID
    target: str
    check_types: JSON
    status: str
    created_at: datetime
    completed_at: datetime

# app/models/agent.py
class Agent(Base):
    id: UUID
    name: str
    location: str
    api_token: str
    status: str
    last_heartbeat: datetime

# app/models/result.py
class CheckResult(Base):
    id: UUID
    check_id: UUID
    agent_id: UUID
    check_type: str
    success: bool
    data: JSON
    duration_ms: int
```

**Задачи:**
- [x] Создать модели SQLAlchemy
- [x] Настроить relationships
- [x] Создать схемы Pydantic
- [x] Alembic миграции

#### 1.3 API Endpoints (2 часа)
```python
# app/api/checks.py
@router.post("/checks")
async def create_check(...)

@router.get("/checks/{check_id}")
async def get_check(...)

# app/api/agents.py
@router.post("/agents/register")
async def register_agent(...)

@router.post("/agents/heartbeat")
async def agent_heartbeat(...)

@router.get("/agents")
async def list_agents(...)
```

**Задачи:**
- [x] CRUD для checks
- [x] Agent registration
- [x] Heartbeat endpoint
- [x] List agents с фильтрацией

#### 1.4 Redis Integration (1 час)
```python
# app/services/redis_client.py
class RedisClient:
    async def enqueue_task(task: dict)
    async def get_task() -> dict
    async def set_agent_status(agent_id, status)
    async def get_agent_status(agent_id)
```

**Задачи:**
- [x] Redis connection pool
- [x] Task queue (LPUSH/RPOP)
- [x] Agent status cache
- [x] Pub/Sub для уведомлений

---

### Phase 2: Agent Development (3-4 часа)

#### 2.1 Agent Core (1.5 часа)
```python
# agent/main.py
class Agent:
    def __init__(self, config):
        self.config = config
        self.api_client = APIClient(config.api_url)
        
    async def run(self):
        while True:
            await self.heartbeat()
            task = await self.get_task()
            if task:
                result = await self.execute_check(task)
                await self.send_result(result)
            await asyncio.sleep(5)
```

**Задачи:**
- [x] Main loop
- [x] API client
- [x] Heartbeat механизм
- [x] Task polling
- [x] Error handling

#### 2.2 Check Implementations (2 часа)

**HTTP Check (30 мин)**
```python
# agent/checks/http.py
async def check_http(target: str) -> dict:
    start = time.time()
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://{target}") as resp:
            return {
                "status_code": resp.status,
                "headers": dict(resp.headers),
                "duration_ms": (time.time() - start) * 1000
            }
```

**Ping Check (30 мин)**
```python
# agent/checks/ping.py
def check_ping(target: str) -> dict:
    latency = ping3.ping(target, timeout=2)
    return {
        "success": latency is not None,
        "latency_ms": latency * 1000 if latency else None
    }
```

**DNS Check (30 мин)**
```python
# agent/checks/dns.py
def check_dns(domain: str, record_type: str) -> dict:
    resolver = dns.resolver.Resolver()
    answers = resolver.resolve(domain, record_type)
    return {
        "records": [str(rdata) for rdata in answers]
    }
```

**TCP Port Check (15 мин)**
```python
# agent/checks/tcp.py
async def check_tcp_port(host: str, port: int) -> dict:
    reader, writer = await asyncio.open_connection(host, port)
    writer.close()
    await writer.wait_closed()
    return {"success": True, "port": port}
```

**Traceroute (опционально, 1 час)**
```python
# agent/checks/traceroute.py
def check_traceroute(target: str, max_hops: int = 30):
    # Использовать scapy или системный вызов
    pass
```

---

### Phase 3: Frontend Development (5-6 часов)

#### 3.1 Project Setup (1 час)
```bash
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install axios @tanstack/react-query react-router-dom
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

**Структура:**
```
src/
├── components/
│   ├── CheckForm.tsx
│   ├── ResultCard.tsx
│   ├── AgentStatus.tsx
│   └── LoadingSpinner.tsx
├── pages/
│   ├── Dashboard.tsx
│   ├── Results.tsx
│   └── Agents.tsx
├── api/
│   └── client.ts
├── hooks/
│   └── useChecks.ts
├── types/
│   └── index.ts
└── App.tsx
```

#### 3.2 API Client (30 мин)
```typescript
// src/api/client.ts
export const api = {
  checks: {
    create: (data: CreateCheckRequest) => 
      axios.post('/api/checks', data),
    get: (id: string) => 
      axios.get(`/api/checks/${id}`),
    list: () => 
      axios.get('/api/checks')
  },
  agents: {
    list: () => 
      axios.get('/api/agents'),
    register: (data: RegisterAgentRequest) => 
      axios.post('/api/agents/register', data)
  }
}
```

#### 3.3 Components (3 часа)

**CheckForm (1 час)**
```tsx
// src/components/CheckForm.tsx
export const CheckForm = () => {
  const [target, setTarget] = useState('')
  const [checks, setChecks] = useState<string[]>([])
  
  const handleSubmit = async () => {
    const result = await api.checks.create({ target, checks })
    navigate(`/results/${result.check_id}`)
  }
  
  return (
    <form onSubmit={handleSubmit}>
      <input value={target} onChange={...} />
      <CheckboxGroup options={checkTypes} value={checks} />
      <button type="submit">Run Check</button>
    </form>
  )
}
```

**Results Page (1 час)**
```tsx
// src/pages/Results.tsx
export const Results = () => {
  const { id } = useParams()
  const { data, isLoading } = useQuery({
    queryKey: ['check', id],
    queryFn: () => api.checks.get(id!)
  })
  
  return (
    <div>
      <h1>Results for {data.target}</h1>
      <StatusBadge status={data.status} />
      <ResultsTable results={data.results} />
    </div>
  )
}
```

**Agents Page (1 час)**
```tsx
// src/pages/Agents.tsx
export const Agents = () => {
  const { data: agents } = useQuery({
    queryKey: ['agents'],
    queryFn: api.agents.list
  })
  
  return (
    <div>
      <h1>Agents</h1>
      <AgentsGrid agents={agents} />
    </div>
  )
}
```

#### 3.4 Styling (1 час)
- Tailwind CSS setup
- Responsive layout
- Color scheme
- Animations

---

### Phase 4: Integration & Polish (3-4 часа)

#### 4.1 Docker Setup (1 час)

**backend/Dockerfile**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-dev
COPY . .
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

**docker-compose.yml**
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: hostchecker
  redis:
    image: redis:7-alpine
  backend:
    build: ./backend
    ports: ["8000:8000"]
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
  agent:
    build: ./agent
```

#### 4.2 Testing (1.5 часа)
- [ ] Backend unit tests
- [ ] Agent checks tests
- [ ] Integration tests
- [ ] E2E тест полного flow

#### 4.3 Documentation (1 час)
- [ ] README.md
- [ ] API.md (endpoints)
- [ ] AGENT_SETUP.md (инструкция)
- [ ] ARCHITECTURE.md (диаграммы)

#### 4.4 Bug Fixes & Polish (30 мин)
- [ ] Fix edge cases
- [ ] Improve error messages
- [ ] Add loading states
- [ ] Polish UI

---

## 🎁 Bonus Features (опционально)

### WebSocket Real-time (2-3 часа)

**Backend**
```python
# app/api/websocket.py
@router.websocket("/ws/checks/{check_id}")
async def websocket_endpoint(websocket: WebSocket, check_id: str):
    await websocket.accept()
    async for message in redis.subscribe(f"check:{check_id}"):
        await websocket.send_json(message)
```

**Frontend**
```typescript
// src/hooks/useRealtimeCheck.ts
export const useRealtimeCheck = (checkId: string) => {
  const [data, setData] = useState(null)
  
  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/checks/${checkId}`)
    ws.onmessage = (event) => setData(JSON.parse(event.data))
    return () => ws.close()
  }, [checkId])
  
  return data
}
```

### GeoIP Visualization (3 часа)
```bash
# Добавить зависимости
poetry add geoip2 folium

# Интеграция с картой
npm install react-leaflet leaflet
```

---

## 📊 Чеклист готовности к презентации

### Функциональность
- [ ] Создание проверки через UI работает
- [ ] Все типы проверок выполняются (HTTP, Ping, DNS минимум)
- [ ] Результаты отображаются корректно
- [ ] Агенты регистрируются и отправляют heartbeat
- [ ] Статус агентов отображается

### UI/UX
- [ ] Форма проверки интуитивная
- [ ] Результаты читаемые и понятные
- [ ] Список агентов информативный
- [ ] Дизайн приятный глазу
- [ ] Responsive на мобильных

### Техническая часть
- [ ] Docker Compose запускает всё одной командой
- [ ] БД миграции применяются автоматически
- [ ] Логи информативные
- [ ] Ошибки обрабатываются gracefully

### Документация
- [ ] README с инструкцией запуска
- [ ] Инструкция по регистрации агента
- [ ] API документация доступна
- [ ] Архитектурная диаграмма есть

### Демо
- [ ] Подготовлен демо-сценарий
- [ ] Тестовые данные готовы
- [ ] Скриншоты/видео записаны
- [ ] Презентация готова (5-7 мин)

---

## 🎤 Сценарий презентации (5-7 мин)

### 1. Введение (1 мин)
> "Представляем Host Checker - распределённый сервис для проверки доступности хостов и DNS резолвинга с поддержкой множества агентов в разных локациях"

### 2. Демо (3 мин)

**Шаг 1: Создание проверки**
- Открыть UI
- Ввести google.com
- Выбрать проверки: HTTP, Ping, DNS
- Нажать "Run Check"

**Шаг 2: Просмотр результатов**
- Перейти на страницу результатов
- Показать real-time обновления (если есть WebSocket)
- Показать результаты от разных агентов
- Объяснить метрики (latency, status codes, DNS records)

**Шаг 3: Агенты**
- Показать список агентов
- Статусы (online/offline)
- Локации
- Статистику

### 3. Архитектура (2 мин)

Показать диаграмму:
```
Frontend (React) 
    ↓
Backend (FastAPI)
    ↓
PostgreSQL + Redis
    ↓
Agents (Python)
```

Объяснить:
- REST API для взаимодействия
- Redis как очередь задач
- Агенты poll'ят задачи и выполняют проверки
- Результаты сохраняются в PostgreSQL

### 4. Регистрация агента (1 мин)

Показать README:
```bash
docker run -e AGENT_TOKEN=xxx \
           -e AGENT_NAME="My Agent" \
           hostchecker/agent:latest
```

### 5. Заключение (30 сек)
> "Полностью рабочий MVP с возможностью масштабирования. Можно добавлять неограниченное количество агентов в разных странах."

---

## 💡 Советы по реализации

### 1. Начните с MVP
Не пытайтесь сделать всё сразу. Сначала сделайте базовую версию, которая работает end-to-end.

### 2. Используйте готовые решения
- FastAPI автодокументация
- TanStack Query для кеширования
- Tailwind для UI
- Docker Compose для инфраструктуры

### 3. Тестируйте постоянно
После каждой фичи проверяйте, что всё работает. Не накапливайте баги.

### 4. Документируйте по ходу
Пишите README параллельно с кодом, пока всё свежо в памяти.

### 5. Коммитьте часто
```bash
git commit -m "feat: add HTTP check"
git commit -m "feat: add agent registration"
git commit -m "feat: add results page"
```

### 6. Используйте AI помощников
- GitHub Copilot для бойлерплейта
- ChatGPT для сложных алгоритмов
- Cursor для рефакторинга

---

## 🚨 Возможные проблемы и решения

| Проблема | Решение |
|----------|---------|
| Ping требует sudo | Использовать `ping3` с fallback на системный ping |
| Traceroute сложный | Начать с простой версии через `subprocess` |
| WebSocket не работает | Fallback на polling каждые 2 секунды |
| Docker не запускается | Проверить `docker-compose.yml` синтаксис |
| БД миграции падают | Использовать `alembic revision --autogenerate` |
| Frontend не подключается | Проверить CORS в FastAPI |

---

## 📈 Приоритизация фич

### Must Have (обязательно для MVP)
1. ✅ HTTP check
2. ✅ Ping check
3. ✅ DNS check (хотя бы A-записи)
4. ✅ Agent registration
5. ✅ Heartbeat mechanism
6. ✅ Results display
7. ✅ Basic UI

### Should Have (очень желательно)
1. 🟡 TCP port check
2. 🟡 WebSocket real-time
3. 🟡 Multiple DNS record types
4. 🟡 Agent status monitoring
5. 🟡 Rate limiting

### Nice to Have (если останется время)
1. ⚪ Traceroute
2. ⚪ GeoIP visualization
3. ⚪ Check templates
4. ⚪ Metrics dashboard
5. ⚪ Agent rating

---

## 🏁 Финальный чеклист перед сдачей

- [ ] Код закоммичен в SourceCraft
- [ ] README.md заполнен полностью
- [ ] `docker-compose up` запускает всё
- [ ] Демо работает стабильно
- [ ] Презентация отрепетирована
- [ ] Скриншоты/видео готовы
- [ ] Контакты указаны
- [ ] Всё протестировано

---

**Удачи! Это реально выполнимо! 💪**

