# 🚀 Стратегия деплоя Host Checker

> План размещения проекта на бесплатных хостингах для демонстрации

---

## 📍 Твой репозиторий

```
GitHub: https://github.com/Mhitaryan-Tigran/Reaf-Team_Hackathon-Autumn
```

---

## 🎯 Оптимальная схема деплоя

### Рекомендуемые хостинги (БЕСПЛАТНО):

```
┌─────────────────────────────────────────┐
│          DEPLOYMENT SCHEMA              │
├─────────────────────────────────────────┤
│                                         │
│  Frontend (React)                       │
│  └─► Vercel ✅                          │
│      • Автодеплой из GitHub             │
│      • CDN из коробки                   │
│      • Custom domain                    │
│      • Instant deploys                  │
│                                         │
│  Backend (FastAPI)                      │
│  └─► Railway / Render ✅                │
│      • Docker support                   │
│      • PostgreSQL included              │
│      • Redis included                   │
│      • Auto-scaling                     │
│                                         │
│  Database (PostgreSQL)                  │
│  └─► Railway / Supabase ✅              │
│      • Managed PostgreSQL               │
│      • Автобэкапы                       │
│      • 500MB free                       │
│                                         │
│  Redis (Queue)                          │
│  └─► Railway / Upstash ✅               │
│      • Managed Redis                    │
│      • 10K commands/day free            │
│                                         │
│  Agent (Python Worker)                  │
│  └─► Railway / Fly.io ✅                │
│      • Background workers               │
│      • Multiple regions                 │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🏆 Рекомендуемый вариант: Railway

### Почему Railway?

✅ **Всё в одном месте:**
- Backend (FastAPI)
- PostgreSQL
- Redis
- Agent workers

✅ **Простота:**
- Deploy из GitHub
- Один клик для сервисов
- Автоматические миграции

✅ **Бесплатно:**
- $5 в месяц credits
- Хватит на демо/хакатон
- No credit card для старта

---

## 📋 План действий (пошагово)

### Phase 1: Подготовка репозитория (30 минут)

#### 1. Структура проекта

```bash
cd /Users/slava/Hack2025/Reaf-Team_Hackathon-Autumn

# Создать структуру
mkdir -p backend frontend agent
mkdir -p backend/app/{api,models,schemas,services}
mkdir -p frontend/src/{components,pages,api}
mkdir -p agent/agent/checks
```

#### 2. Добавить конфиг файлы для деплоя

**railway.json** (в корне)
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**vercel.json** (для frontend)
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

#### 3. Environment variables

**.env.example** (обновить)
```bash
# Backend (Railway)
DATABASE_URL=postgresql://user:pass@host:5432/dbname
REDIS_URL=redis://host:6379
SECRET_KEY=your-secret-key
REGISTRATION_TOKEN=master-token
CORS_ORIGINS=["https://your-frontend.vercel.app"]

# Frontend (Vercel)
VITE_API_URL=https://your-backend.railway.app
VITE_WS_URL=wss://your-backend.railway.app
```

---

### Phase 2: Deploy Backend на Railway (15 минут)

#### Шаги:

1. **Зайти на Railway.app**
   ```
   https://railway.app
   → Sign up with GitHub
   ```

2. **Создать новый проект**
   ```
   → New Project
   → Deploy from GitHub repo
   → Выбрать: Reaf-Team_Hackathon-Autumn
   → Root directory: backend/
   ```

3. **Добавить PostgreSQL**
   ```
   → Add Service
   → Database → PostgreSQL
   → Автоматически создаст DATABASE_URL
   ```

4. **Добавить Redis**
   ```
   → Add Service
   → Database → Redis
   → Автоматически создаст REDIS_URL
   ```

5. **Настроить переменные окружения**
   ```
   Backend service → Variables
   → Add:
      SECRET_KEY=random-string-here
      REGISTRATION_TOKEN=your-master-token
      CORS_ORIGINS=["https://your-app.vercel.app"]
   ```

6. **Deploy!**
   ```
   → Railway автоматически деплоит
   → Получишь URL: https://your-backend.railway.app
   ```

---

### Phase 3: Deploy Frontend на Vercel (10 минут)

#### Шаги:

1. **Зайти на Vercel.com**
   ```
   https://vercel.com
   → Sign up with GitHub
   ```

2. **Импортировать проект**
   ```
   → New Project
   → Import Git Repository
   → Выбрать: Reaf-Team_Hackathon-Autumn
   ```

3. **Настроить билд**
   ```
   Framework Preset: Vite
   Root Directory: frontend/
   Build Command: npm run build
   Output Directory: dist
   ```

4. **Добавить Environment Variables**
   ```
   → Environment Variables
   → Add:
      VITE_API_URL=https://your-backend.railway.app
      VITE_WS_URL=wss://your-backend.railway.app
   ```

5. **Deploy!**
   ```
   → Vercel автоматически деплоит
   → Получишь URL: https://your-app.vercel.app
   ```

---

### Phase 4: Deploy Agent на Railway (10 минут)

#### Шаги:

1. **В том же Railway проекте**
   ```
   → Add Service
   → GitHub Repo (тот же)
   → Root directory: agent/
   ```

2. **Настроить переменные**
   ```
   → Variables
   → Add:
      API_URL=https://your-backend.railway.app
      AGENT_TOKEN=generate-this-via-api
      AGENT_NAME=Railway-Agent-1
      AGENT_LOCATION=US-East
   ```

3. **Deploy!**
   ```
   → Агент запустится как worker
   ```

---

### Phase 5: Настроить автодеплой (5 минут)

#### GitHub Actions (опционально)

**.github/workflows/deploy.yml**
```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: vercel/actions/deploy@v2
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
  
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      # Railway деплоит автоматически при push
```

---

## 🎨 Альтернативные варианты

### Вариант 2: Render.com (похож на Railway)

**Pros:**
- ✅ Бесплатный tier
- ✅ PostgreSQL included
- ✅ Auto-deploy from GitHub

**Cons:**
- ⚠️ Холодный старт (15-30 сек)
- ⚠️ Нет Redis на free tier

**Использование:**
```
1. render.com → New Web Service
2. Connect GitHub repo
3. Select backend/ directory
4. Deploy!
```

---

### Вариант 3: Fly.io

**Pros:**
- ✅ Отличная производительность
- ✅ Multiple regions
- ✅ Docker native

**Cons:**
- ⚠️ Нужна кредитка (но не списывают)
- ⚠️ Чуть сложнее setup

**Использование:**
```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Deploy backend
cd backend
flyctl launch

# Deploy agent
cd ../agent
flyctl launch
```

---

### Вариант 4: Полностью Vercel (с Serverless)

**Pros:**
- ✅ Всё в одном месте
- ✅ Очень быстро

**Cons:**
- ⚠️ Нужно адаптировать под serverless
- ⚠️ Сложности с background workers

**НЕ рекомендуется для этого проекта** (нужны long-running workers)

---

## 📊 Сравнение хостингов

| Хостинг | Backend | Frontend | DB | Redis | Workers | FREE Tier | Сложность |
|---------|---------|----------|----|----|---------|-----------|-----------|
| **Railway** | ✅ | ❌ | ✅ | ✅ | ✅ | $5/mo credits | ⭐⭐ |
| **Vercel** | ⚠️ | ✅ | ❌ | ❌ | ❌ | Да | ⭐ |
| **Render** | ✅ | ✅ | ✅ | ❌ | ✅ | Да | ⭐⭐ |
| **Fly.io** | ✅ | ✅ | ✅ | ✅ | ✅ | Да* | ⭐⭐⭐ |
| **Heroku** | ✅ | ✅ | ✅ | ✅ | ✅ | Нет | ⭐⭐ |

**Рекомендация:** Railway (Backend+DB+Redis+Agent) + Vercel (Frontend)

---

## 🔧 Необходимые Dockerfiles

### backend/Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Copy application
COPY . .

# Run migrations and start
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
```

### agent/Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for network tools
RUN apt-get update && apt-get install -y \
    iputils-ping \
    traceroute \
    dnsutils \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# Copy application
COPY . .

CMD ["python", "-m", "agent.main"]
```

### frontend/Dockerfile (опционально, для Railway)

```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## 🎯 Пошаговый план на сегодня

### Сессия 1: Setup (1 час)

```bash
# 1. Перейти в репозиторий
cd /Users/slava/Hack2025/Reaf-Team_Hackathon-Autumn

# 2. Создать структуру (я помогу)
mkdir -p backend/app frontend/src agent/agent

# 3. Копировать шаблоны из PROJECT_STRUCTURE.md
# (я создам файлы)

# 4. Commit и push
git add .
git commit -m "Initial project structure"
git push origin main
```

### Сессия 2: Backend MVP (4 часа)

```bash
# 1. Создать FastAPI app (я помогу)
# 2. Модели БД
# 3. API endpoints
# 4. Redis queue
# 5. Test locally
# 6. Push to GitHub → Railway auto-deploy
```

### Сессия 3: Agent MVP (3 часа)

```bash
# 1. Agent core loop
# 2. HTTP check
# 3. Ping check
# 4. DNS check
# 5. Test locally
# 6. Push to GitHub → Railway auto-deploy
```

### Сессия 4: Frontend MVP (4 часа)

```bash
# 1. React setup
# 2. CheckForm component
# 3. Results page
# 4. Agents page
# 5. Test locally
# 6. Push to GitHub → Vercel auto-deploy
```

### Сессия 5: Integration & Polish (2 часа)

```bash
# 1. Проверить весь flow
# 2. Исправить баги
# 3. Улучшить UI
# 4. Написать README
# 5. Записать демо
```

---

## 💡 Pro Tips

### 1. Используй Railway CLI (опционально)

```bash
# Install
npm i -g @railway/cli

# Login
railway login

# Link project
railway link

# Check logs
railway logs

# Run locally with cloud DB
railway run python app/main.py
```

### 2. Environment Variables Best Practices

```bash
# Локальная разработка
.env                    # Никогда не коммитить!

# Production
Railway Dashboard       # Там настраивай переменные
Vercel Dashboard        # Там настраивай переменные
```

### 3. Мониторинг

**Railway:**
- Встроенные логи
- Metrics dashboard
- Alerts

**Vercel:**
- Analytics
- Real-time logs
- Performance insights

---

## 🚨 Частые проблемы при деплое

### 1. CORS ошибки

**Проблема:**
```
Access to XMLHttpRequest blocked by CORS
```

**Решение:**
```python
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-app.vercel.app"],  # Твой frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Database connection fails

**Проблема:**
```
Connection refused to postgres
```

**Решение:**
```bash
# Railway автоматически инжектит DATABASE_URL
# Убедись что используешь правильно:
DATABASE_URL = os.getenv("DATABASE_URL")
```

### 3. Port binding

**Проблема:**
```
Address already in use
```

**Решение:**
```python
# Используй переменную PORT от Railway
port = int(os.getenv("PORT", 8000))
uvicorn.run(app, host="0.0.0.0", port=port)
```

---

## 📝 Checklist перед деплоем

### Backend
- [ ] Dockerfile создан
- [ ] Requirements/pyproject.toml актуальный
- [ ] Environment variables в .env.example
- [ ] Database migrations работают
- [ ] Health endpoint есть (/health)
- [ ] CORS настроен

### Frontend
- [ ] Build проходит локально
- [ ] Environment variables настроены
- [ ] API URL указан правильно
- [ ] Routes работают
- [ ] Production build оптимизирован

### Agent
- [ ] Dockerfile создан
- [ ] Dependencies установлены
- [ ] Может подключиться к API
- [ ] Проверки работают

---

## 🎊 Готово к деплою!

После выполнения всех шагов у тебя будет:

```
✅ Frontend: https://host-checker.vercel.app
✅ Backend:  https://host-checker.railway.app
✅ Agent:    Running on Railway
✅ Database: PostgreSQL on Railway
✅ Redis:    Redis on Railway

→ Полностью рабочий проект в продакшене!
→ Автодеплой при каждом push
→ Логи и мониторинг
→ Готов к презентации
```

---

## 🚀 Начнём?

**Готов помочь тебе:**
1. ✅ Создать структуру проекта
2. ✅ Написать код (Backend, Frontend, Agent)
3. ✅ Настроить Dockerfiles
4. ✅ Помочь с деплоем
5. ✅ Исправить баги
6. ✅ Подготовить к презентации

**Скажи "поехали" и начнём с создания структуры проекта!** 🔥

---

_Railway + Vercel = Идеальная комбинация для хакатона! 💪_

