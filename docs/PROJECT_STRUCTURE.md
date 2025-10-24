# 📁 Структура проекта

## 🌳 Полное дерево

```
host-checker/
├── backend/                          # Backend на FastAPI
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # Точка входа FastAPI
│   │   ├── config.py                 # Конфигурация (Settings)
│   │   ├── database.py               # SQLAlchemy setup
│   │   │
│   │   ├── models/                   # SQLAlchemy модели
│   │   │   ├── __init__.py
│   │   │   ├── check.py
│   │   │   ├── agent.py
│   │   │   ├── task.py
│   │   │   └── result.py
│   │   │
│   │   ├── schemas/                  # Pydantic схемы
│   │   │   ├── __init__.py
│   │   │   ├── check.py
│   │   │   ├── agent.py
│   │   │   ├── task.py
│   │   │   └── result.py
│   │   │
│   │   ├── api/                      # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── checks.py
│   │   │   ├── agents.py
│   │   │   ├── tasks.py
│   │   │   └── websocket.py
│   │   │
│   │   ├── services/                 # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── task_manager.py
│   │   │   ├── agent_manager.py
│   │   │   ├── result_aggregator.py
│   │   │   └── redis_client.py
│   │   │
│   │   └── utils/                    # Утилиты
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       └── helpers.py
│   │
│   ├── alembic/                      # Database migrations
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │       └── 001_initial.py
│   │
│   ├── tests/                        # Тесты
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_api/
│   │   │   ├── test_checks.py
│   │   │   └── test_agents.py
│   │   └── test_services/
│   │       └── test_task_manager.py
│   │
│   ├── Dockerfile
│   ├── pyproject.toml                # Poetry dependencies
│   ├── poetry.lock
│   ├── alembic.ini
│   └── .env.example
│
├── frontend/                         # Frontend на React
│   ├── src/
│   │   ├── components/               # React компоненты
│   │   │   ├── layout/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Footer.tsx
│   │   │   │   └── Layout.tsx
│   │   │   │
│   │   │   ├── check/
│   │   │   │   ├── CheckForm.tsx
│   │   │   │   ├── CheckTypeSelector.tsx
│   │   │   │   └── AgentSelector.tsx
│   │   │   │
│   │   │   ├── results/
│   │   │   │   ├── ResultCard.tsx
│   │   │   │   ├── ResultsTable.tsx
│   │   │   │   ├── ResultDetails.tsx
│   │   │   │   └── StatusBadge.tsx
│   │   │   │
│   │   │   ├── agents/
│   │   │   │   ├── AgentCard.tsx
│   │   │   │   ├── AgentsList.tsx
│   │   │   │   ├── AgentStatus.tsx
│   │   │   │   └── AgentStats.tsx
│   │   │   │
│   │   │   └── common/
│   │   │       ├── Button.tsx
│   │   │       ├── Input.tsx
│   │   │       ├── Card.tsx
│   │   │       ├── LoadingSpinner.tsx
│   │   │       └── ErrorBoundary.tsx
│   │   │
│   │   ├── pages/                    # Страницы
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Results.tsx
│   │   │   ├── Agents.tsx
│   │   │   └── NotFound.tsx
│   │   │
│   │   ├── api/                      # API клиент
│   │   │   ├── client.ts
│   │   │   ├── checks.ts
│   │   │   ├── agents.ts
│   │   │   └── websocket.ts
│   │   │
│   │   ├── hooks/                    # Custom hooks
│   │   │   ├── useChecks.ts
│   │   │   ├── useAgents.ts
│   │   │   ├── useWebSocket.ts
│   │   │   └── usePolling.ts
│   │   │
│   │   ├── types/                    # TypeScript types
│   │   │   ├── index.ts
│   │   │   ├── check.ts
│   │   │   ├── agent.ts
│   │   │   └── result.ts
│   │   │
│   │   ├── utils/                    # Утилиты
│   │   │   ├── format.ts
│   │   │   ├── validation.ts
│   │   │   └── constants.ts
│   │   │
│   │   ├── styles/                   # Стили
│   │   │   └── globals.css
│   │   │
│   │   ├── App.tsx                   # Main App
│   │   ├── main.tsx                  # Entry point
│   │   └── vite-env.d.ts
│   │
│   ├── public/
│   │   ├── favicon.ico
│   │   └── logo.png
│   │
│   ├── Dockerfile
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── .env.example
│
├── agent/                            # Agent на Python
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── main.py                   # Основной цикл
│   │   ├── config.py                 # Конфигурация
│   │   ├── client.py                 # API клиент
│   │   │
│   │   └── checks/                   # Реализация проверок
│   │       ├── __init__.py
│   │       ├── base.py               # Базовый класс
│   │       ├── http.py               # HTTP/HTTPS check
│   │       ├── ping.py               # Ping check
│   │       ├── tcp.py                # TCP port check
│   │       ├── dns.py                # DNS lookup
│   │       └── traceroute.py         # Traceroute
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_checks.py
│   │
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── poetry.lock
│   └── README.md
│
├── docs/                             # Документация
│   ├── API.md
│   ├── AGENT_SETUP.md
│   ├── DEPLOYMENT.md
│   └── images/
│       └── architecture.png
│
├── scripts/                          # Утилиты и скрипты
│   ├── init-db.sh
│   ├── create-agent-token.sh
│   ├── backup-db.sh
│   └── migrate.sh
│
├── .github/                          # GitHub Actions (CI/CD)
│   └── workflows/
│       ├── backend-tests.yml
│       ├── frontend-tests.yml
│       └── deploy.yml
│
├── docker-compose.yml                # Dev environment
├── docker-compose.prod.yml           # Production environment
├── docker-compose.dev.yml            # Local dev with hot reload
│
├── .env.example                      # Example environment variables
├── .gitignore
├── .dockerignore
│
├── README.md                         # Главный README
├── ARCHITECTURE.md                   # Архитектура системы
├── IMPLEMENTATION_PLAN.md            # План реализации
├── STACK_SUMMARY.md                  # Сводка по стеку
├── FAQ.md                            # Частые вопросы
├── QUICKSTART.md                     # Быстрый старт
└── LICENSE
```

---

## 📄 Шаблоны ключевых файлов

### backend/app/main.py

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import checks, agents, websocket
from app.config import settings

app = FastAPI(
    title="Host Checker API",
    description="Distributed host checking service",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(checks.router, prefix="/api/checks", tags=["checks"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(websocket.router, prefix="/api/ws", tags=["websocket"])

@app.get("/health")
async def health():
    return {"status": "ok"}
```

### backend/app/config.py

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str
    
    # Security
    SECRET_KEY: str
    REGISTRATION_TOKEN: str
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### backend/app/models/check.py

```python
from sqlalchemy import Column, String, TIMESTAMP, JSON
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from app.database import Base

class Check(Base):
    __tablename__ = "checks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    target = Column(String(255), nullable=False)
    check_types = Column(JSON, nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    completed_at = Column(TIMESTAMP, nullable=True)
```

### backend/app/schemas/check.py

```python
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import List, Optional

class CheckCreate(BaseModel):
    target: str = Field(..., min_length=1, max_length=255)
    checks: List[str] = Field(..., min_items=1)
    agents: List[str] = Field(default=["all"])

class CheckResponse(BaseModel):
    id: UUID
    target: str
    check_types: List[str]
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
```

### backend/app/api/checks.py

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.check import CheckCreate, CheckResponse
from app.services.task_manager import TaskManager
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=CheckResponse)
async def create_check(
    check_data: CheckCreate,
    db: AsyncSession = Depends(get_db)
):
    task_manager = TaskManager(db)
    check = await task_manager.create_check(check_data)
    return check

@router.get("/{check_id}", response_model=CheckResponse)
async def get_check(
    check_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    # Implementation
    pass
```

### frontend/src/App.tsx

```tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import Results from './pages/Results';
import Agents from './pages/Agents';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/results/:checkId" element={<Results />} />
            <Route path="/agents" element={<Agents />} />
          </Routes>
        </Layout>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
```

### frontend/src/api/client.ts

```typescript
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const checksAPI = {
  create: (data: CreateCheckRequest) => 
    api.post('/checks', data),
  get: (id: string) => 
    api.get(`/checks/${id}`),
  list: () => 
    api.get('/checks'),
};

export const agentsAPI = {
  list: () => 
    api.get('/agents'),
  register: (data: RegisterAgentRequest) => 
    api.post('/agents/register', data),
};
```

### frontend/src/types/index.ts

```typescript
export interface Check {
  id: string;
  target: string;
  check_types: string[];
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  created_at: string;
  completed_at?: string;
  results?: CheckResult[];
}

export interface CheckResult {
  id: string;
  check_id: string;
  agent_id: string;
  agent_name: string;
  check_type: string;
  success: boolean;
  data: Record<string, any>;
  duration_ms: number;
  created_at: string;
}

export interface Agent {
  id: string;
  name: string;
  location: string;
  status: 'online' | 'offline';
  last_heartbeat: string;
  registered_at: string;
}
```

### agent/agent/main.py

```python
import asyncio
import logging
from agent.config import settings
from agent.client import APIClient
from agent.checks import HTTPCheck, PingCheck, DNSCheck

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Agent:
    def __init__(self):
        self.api_client = APIClient(settings.API_URL, settings.AGENT_TOKEN)
        self.checks = {
            'http': HTTPCheck(),
            'ping': PingCheck(),
            'dns': DNSCheck(),
        }
    
    async def heartbeat(self):
        try:
            await self.api_client.heartbeat()
            logger.info("Heartbeat sent")
        except Exception as e:
            logger.error(f"Heartbeat failed: {e}")
    
    async def get_task(self):
        return await self.api_client.get_task()
    
    async def execute_check(self, task):
        check_type = task['check_type']
        target = task['target']
        
        checker = self.checks.get(check_type)
        if not checker:
            return {"error": f"Unknown check type: {check_type}"}
        
        return await checker.check(target)
    
    async def send_result(self, task_id, result):
        await self.api_client.send_result(task_id, result)
    
    async def run(self):
        logger.info(f"Agent started: {settings.AGENT_NAME}")
        
        while True:
            try:
                # Heartbeat
                await self.heartbeat()
                
                # Get task
                task = await self.get_task()
                
                if task:
                    logger.info(f"Processing task: {task['task_id']}")
                    result = await self.execute_check(task)
                    await self.send_result(task['task_id'], result)
                    logger.info(f"Task completed: {task['task_id']}")
                
                await asyncio.sleep(5)
                
            except Exception as e:
                logger.error(f"Error: {e}")
                await asyncio.sleep(10)

if __name__ == "__main__":
    agent = Agent()
    asyncio.run(agent.run())
```

### agent/agent/checks/http.py

```python
import aiohttp
import time
from typing import Dict, Any

class HTTPCheck:
    async def check(self, target: str) -> Dict[str, Any]:
        url = target if target.startswith('http') else f'http://{target}'
        
        start = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    duration_ms = (time.time() - start) * 1000
                    
                    return {
                        "success": True,
                        "status_code": response.status,
                        "headers": dict(response.headers),
                        "duration_ms": round(duration_ms, 2),
                        "body_size": len(await response.read())
                    }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "duration_ms": round((time.time() - start) * 1000, 2)
            }
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: hostchecker
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://postgres:postgres@postgres:5432/hostchecker
      REDIS_URL: redis://redis:6379
      SECRET_KEY: dev-secret-key
      REGISTRATION_TOKEN: dev-registration-token
      CORS_ORIGINS: '["http://localhost:3000"]'
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --reload

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      VITE_API_URL: http://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev -- --host

  agent:
    build: ./agent
    environment:
      API_URL: http://backend:8000
      AGENT_TOKEN: ${AGENT_TOKEN:-}
      AGENT_NAME: ${AGENT_NAME:-Local-Agent-1}
      AGENT_LOCATION: ${AGENT_LOCATION:-Local}
    depends_on:
      - backend
    volumes:
      - ./agent:/app

volumes:
  postgres_data:
  redis_data:
```

### .env.example

```bash
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/hostchecker

# Redis
REDIS_URL=redis://redis:6379

# Backend
SECRET_KEY=change-this-in-production
REGISTRATION_TOKEN=master-registration-token
CORS_ORIGINS=["http://localhost:3000"]

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

## 📝 Комментарии к структуре

### Backend

- **app/models/** - SQLAlchemy ORM модели (таблицы БД)
- **app/schemas/** - Pydantic схемы (валидация, serialization)
- **app/api/** - API endpoints (роутеры FastAPI)
- **app/services/** - бизнес-логика (не зависит от HTTP)
- **alembic/** - миграции базы данных

### Frontend

- **components/** - переиспользуемые компоненты
- **pages/** - страницы приложения (routes)
- **api/** - HTTP клиент для backend API
- **hooks/** - custom React hooks
- **types/** - TypeScript типы

### Agent

- **checks/** - реализация различных типов проверок
- **client.py** - клиент для общения с backend API
- **main.py** - основной цикл агента

---

**Готово! Структура проекта готова к реализации! 🚀**

