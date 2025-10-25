# 🌐 Host Checker - Сервис проверки хостов и DNS резолвинга

![Status](https://img.shields.io/badge/status-production-success)
![Python](https://img.shields.io/badge/python-3.13-blue)
![License](https://img.shields.io/badge/license-MIT-green)

> **Hackathon Aéza Autumn 2025** - Сервис для проверки доступности хостов и диагностики сетевых проблем из разных регионов мира.

## 📝 Описание

Host Checker - это распределенная система мониторинга и диагностики сетевой доступности, которая позволяет:
- 🌍 Проверять доступность сайтов/сервисов из разных стран
- 🔍 Выполнять DNS lookup с детальной информацией
- 📊 Получать статистику пинга, traceroute и TCP соединений
- 📈 Просматривать историю всех проверок
- 🔗 Делиться результатами через уникальные ссылки

## ✨ Возможности

### Базовые проверки
- ✅ **HTTP/HTTPS** - статус, заголовки, время ответа, редиректы
- ✅ **Ping** - проверка доступности хоста
- ✅ **TCP Port** - проверка открытых портов
- ✅ **Traceroute** - маршрутизация до хоста
- ✅ **DNS Lookup** - A, AAAA, MX, NS, TXT, CNAME записи

### Расширенные функции
- 🔄 **Real-time обновления** - WebSocket для мгновенного отображения результатов
- 🌐 **Geo-распределенные агенты** - проверки из разных стран
- 📊 **История проверок** - все результаты сохраняются в PostgreSQL
- 🔗 **UUID ссылки** - возможность поделиться результатами
- 📈 **Статистика агентов** - производительность и доступность
- 🎨 **Современный UI** - React + Tailwind CSS

## 🏗 Архитектура

```
┌─────────────────────────────────────────────────────────────┐
│                     USER / BROWSER                          │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              Frontend (React + Vite)                        │
│              📦 Vercel                                      │
│              https://hostchecker.vercel.app                 │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API + WebSocket
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              Backend (FastAPI)                              │
│              🚂 Railway                                     │
│              https://hostchecker.railway.app                │
│                                                             │
│  ┌──────────────┐  ┌───────────┐  ┌──────────────┐       │
│  │ PostgreSQL   │  │   Redis   │  │  WebSocket   │       │
│  │ (результаты) │  │ (очереди) │  │ (real-time)  │       │
│  └──────────────┘  └───────────┘  └──────────────┘       │
└────────────────────────┬────────────────────────────────────┘
                         │ Task Polling
                         ↓
          ┌──────────────┴──────────────┐
          ↓                             ↓
┌────────────────────┐       ┌────────────────────┐
│ 🇷🇺 Agent Moscow  │       │ 🇺🇸 Agent USA     │
│ VPS Aeza           │       │ (опционально)     │
│ 138.124.14.179     │       │                    │
└────────────────────┘       └────────────────────┘
```

## 🚀 Быстрый старт

### Локальная разработка

#### Backend

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск PostgreSQL и Redis (Docker)
docker run -d --name postgres \
  -e POSTGRES_PASSWORD=hakatonski123 \
  -e POSTGRES_USER=SERVER \
  -e POSTGRES_DB=serverDB \
  -p 5432:5432 postgres

docker run -d --name redis -p 6379:6379 redis

# Инициализация базы данных
psql -h localhost -U SERVER -d serverDB -f database_migration.sql

# Запуск backend
python -m uvicorn backend_main:app --reload --port 8000
```

Backend доступен по адресу: http://localhost:8000

#### Frontend

```bash
cd frontend

# Установка зависимостей
npm install

# Запуск dev сервера
npm run dev
```

Frontend доступен по адресу: http://localhost:3000

#### Agent

```bash
# Настройте environment variables
export MAIN_SERVER_URL=http://localhost:8000
export AGENT_COUNTRY=Russia
export AGENT_NAME=Agent-Local
export AGENT_UIID=local-agent-001

# Запуск агента
python -m uvicorn agent_production:app --reload --port 8001
```

Agent доступен по адресу: http://localhost:8001

## 🌐 Production Deployment

### Railway (Backend)

1. Подключите GitHub репозиторий к Railway
2. Добавьте PostgreSQL и Redis services
3. Настройте environment variables:
   ```env
   DATABASE_URL=postgresql://...
   REDIS_URL=redis://...
   CORS_ORIGINS=https://hostchecker.vercel.app
   MASTER_REGISTRATION_TOKEN=your-secret-token
   ```
4. Выполните миграцию БД через Railway Query Editor

**Подробная инструкция:** [DEPLOYMENT.md](./DEPLOYMENT.md)

### Vercel (Frontend)

1. Import GitHub репозиторий в Vercel
2. Настройте:
   - Root Directory: `frontend`
   - Framework: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
3. Добавьте environment variable:
   ```env
   VITE_API_URL=https://hostchecker.railway.app
   ```

### VPS Aeza (Agent)

**Быстрый деплой:**
```bash
chmod +x deploy-agent-vps.sh
./deploy-agent-vps.sh
```

**Ручной деплой:**
```bash
# 1. Регистрация агента
curl -X POST https://hostchecker.railway.app/api/agents/register \
  -H "X-Registration-Token: your-token" \
  -H "Content-Type: application/json" \
  -d '{"name":"Agent-Moscow","location":"Russia, Moscow"}'

# 2. Загрузка на VPS
scp -r agent_production.py Dockerfile.agent docker-compose.agent.yml \
  root@138.124.14.179:/opt/hostchecker-agent/

# 3. Настройка .env.agent
ssh root@138.124.14.179
cd /opt/hostchecker-agent
nano .env.agent

# 4. Запуск
docker-compose -f docker-compose.agent.yml up -d
```

## 📚 API Документация

### Endpoints

#### Checks (Проверки)

**Создать проверку**
```http
POST /api/checks
Content-Type: application/json

{
  "target": "google.com",
  "checks": ["http", "ping", "dns"],
  "agents": null  // null = все доступные агенты
}
```

**Получить результаты**
```http
GET /api/checks/{check_id}
```

**Список проверок**
```http
GET /api/checks?limit=50
```

#### Agents (Агенты)

**Регистрация агента**
```http
POST /api/agents/register
X-Registration-Token: master-token
Content-Type: application/json

{
  "name": "Agent-Moscow",
  "location": "Russia, Moscow",
  "metadata": {"provider": "Aeza"}
}
```

**Heartbeat**
```http
POST /api/agents/heartbeat
Content-Type: application/json

{
  "agent_id": "uuid"
}
```

**Список агентов**
```http
GET /api/agents
```

#### WebSocket

**Real-time обновления проверки**
```javascript
const ws = new WebSocket('wss://hostchecker.railway.app/api/ws/checks/{check_id}');
ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  console.log('New result:', update);
};
```

**Полная документация:** http://localhost:8000/docs (Swagger UI)

## 🛠 Технологический стек

### Backend
- **FastAPI** - современный асинхронный веб-фреймворк
- **PostgreSQL** - надежное хранение данных
- **Redis** - очереди задач и pub/sub
- **psycopg2** - PostgreSQL адаптер
- **dnspython** - DNS резолвинг

### Frontend
- **React 18** - UI библиотека
- **TypeScript** - типизированный JavaScript
- **Vite** - быстрый сборщик
- **TanStack Query** - управление серверным состоянием
- **Tailwind CSS** - utility-first CSS
- **Axios** - HTTP клиент

### Agent
- **FastAPI** - легковесный HTTP сервер
- **subprocess** - системные утилиты (ping, traceroute)
- **requests** - HTTP клиент
- **dnspython** - DNS lookup
- **threading** - многопоточная обработка

### Infrastructure
- **Railway** - backend хостинг + PostgreSQL + Redis
- **Vercel** - frontend хостинг с CDN
- **VPS Aeza** - агент в Москве
- **Docker** - контейнеризация агентов
- **systemd** - автозапуск агентов

## 📁 Структура проекта

```
Reaf-Team_Hackathon-Autumn/
├── backend_main.py              # 🚂 Production backend (Railway)
├── agent_production.py          # 🤖 Production agent (VPS)
├── requirements.txt             # 📦 Python зависимости
├── Procfile                     # 🚂 Railway запуск
├── database_migration.sql       # 🗄️ SQL схема
├── Dockerfile.agent            # 🐳 Docker образ агента
├── docker-compose.agent.yml    # 🐳 Docker Compose агента
├── deploy-agent-vps.sh         # 🚀 Скрипт деплоя агента
├── hostchecker-agent.service   # ⚙️ Systemd service
├── DEPLOYMENT.md               # 📖 Инструкция по деплою
├── README.md                   # 📄 Этот файл
│
├── frontend/                   # 🎨 React приложение
│   ├── src/
│   │   ├── api/               # 🌐 API клиент
│   │   ├── components/        # 🧩 React компоненты
│   │   ├── pages/            # 📄 Страницы
│   │   ├── hooks/            # 🪝 Custom hooks
│   │   ├── types/            # 📝 TypeScript типы
│   │   └── utils/            # 🛠️ Утилиты
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── vercel.json           # ⚙️ Vercel конфиг
│
└── docs/                      # 📚 Документация
    ├── ARCHITECTURE.md
    ├── DEPLOYMENT_STRATEGY.md
    ├── IMPLEMENTATION_PLAN.md
    └── ...
```

## 🎯 Roadmap

### MVP (Текущая версия) ✅
- [x] Backend API с полным функционалом
- [x] PostgreSQL для хранения
- [x] Redis для очередей
- [x] WebSocket real-time
- [x] Agent с DNS lookup
- [x] React frontend
- [x] Деплой на Railway/Vercel/Aeza

### v1.1 (Планируется)
- [ ] Визуализация traceroute на карте (GeoIP)
- [ ] Шаблоны проверок ("Full Site Health")
- [ ] Scheduled проверки (cron-подобное)
- [ ] Email/Telegram уведомления
- [ ] Public API с rate limiting
- [ ] Dashboards с метриками

### v2.0 (Будущее)
- [ ] Больше агентов (EU, Asia, Americas)
- [ ] Uptime monitoring (24/7 мониторинг)
- [ ] SLA reports
- [ ] Incident management
- [ ] Интеграции (Slack, Discord, PagerDuty)

## 👥 Команда

- **Никита** - Backend разработка
- **Артем** - Frontend разработка  
- **Андрей** - Agent & DevOps
- **Тигран** - UI/UX дизайн
- **Алексей** - Тестирование & QA

## 📄 Лицензия

MIT License - свободно используйте в своих проектах!

## 🤝 Поддержка

**Hackathon Curator:** [@daedal_dev](https://t.me/daedal_dev)

**Issues:** [GitHub Issues](https://github.com/your-repo/issues)

**Documentation:** [docs/](./docs/)

---

## 🏆 Участие в хакатоне Aéza

Этот проект разработан для **Hackathon Aéza Autumn 2025**.

### Критерии оценки (выполнено)

✅ **Функциональность базовых проверок (35%)**
- HTTP/HTTPS с полной информацией
- Ping с парсингом результатов
- TCP port checking
- Traceroute
- DNS lookup (A, AAAA, MX, NS, TXT, CNAME)

✅ **Надежность выполнения задач (15%)**
- Redis очереди
- Retry механизм в агентах
- PostgreSQL с ACID гарантиями
- Обработка ошибок

✅ **Удобство добавления агентов (20%)**
- REST API для регистрации
- Heartbeat система
- Token-based authentication
- Docker + systemd автозапуск
- Подробная документация

✅ **UI/UX (15%)**
- Современный React интерфейс
- Real-time обновления
- Фильтрация и поиск
- Адаптивный дизайн
- Удобная навигация

✅ **Документация (15%)**
- Подробный README
- Инструкция по деплою (DEPLOYMENT.md)
- API документация (Swagger)
- Комментарии в коде
- Скрипты автоматизации

### Уникальная фишка проекта

🌟 **Geo-распределенные агенты на VPS Aéza** - возможность проверять доступность сервисов из разных стран, что позволяет:
- Обнаруживать региональные блокировки
- Сравнивать скорость доступа из разных локаций
- Диагностировать DNS-проблемы по регионам
- Анализировать маршрутизацию между странами

---

<div align="center">

**Made with ❤️ for Aéza Hackathon Autumn 2025**

[🌐 Live Demo](https://hostchecker.vercel.app) • [📖 Documentation](./docs/) • [🚀 Deploy Guide](./DEPLOYMENT.md)

</div>
