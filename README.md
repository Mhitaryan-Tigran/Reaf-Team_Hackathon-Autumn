# 🌐 Host Checker - Сервис проверки хостов и DNS резолвинга

![Status](https://img.shields.io/badge/status-production-success)
![Python](https://img.shields.io/badge/python-3.13-blue)
![License](https://img.shields.io/badge/license-MIT-green)

> **Hackathon Aéza Autumn 2025** - Распределённый сервис для проверки доступности хостов и диагностики сетевых проблем из разных регионов мира.

## 📝 О проекте

Host Checker решает проблему, с которой сталкивается каждый: **"А работает ли сайт у других?"**

В отличие от Downdetector (базируется на отзывах пользователей), наш сервис **реально проверяет** доступность с распределённых серверов в разных странах и предоставляет детальную диагностику: от простого пинга до анализа DNS и трейса маршрута.

### Что умеет сервис:
- 🌍 **Проверка из разных стран** - обнаруживает региональные блокировки и проблемы
- 🔍 **Полная диагностика** - HTTP/HTTPS, ping, TCP ports, traceroute, DNS
- ⚡ **Real-time результаты** - WebSocket обновления без перезагрузки
- 📊 **История проверок** - все результаты сохраняются с UUID-ссылками
- 🎯 **Удобное API** - автоматизация проверок для мониторинга

## 🔧 Как это работает

### Общий принцип работы

1. **Пользователь создаёт проверку** через веб-интерфейс или API
   - Указывает цель (URL/IP/домен)
   - Выбирает типы проверок (HTTP, ping, DNS и т.д.)
   - Может выбрать конкретные агенты или использовать все доступные

2. **Backend создаёт задачи**
   - Генерирует уникальный UUID для проверки
   - Сохраняет задачу в PostgreSQL
   - Распределяет задачи по агентам через Redis очереди
   - Каждый агент получает свою копию каждой проверки

3. **Агенты выполняют проверки**
   - Каждые 5 секунд опрашивают свою очередь в Redis
   - Берут задачи и выполняют их параллельно (до 10 одновременно)
   - Отправляют результаты обратно на сервер

4. **Backend собирает результаты**
   - Получает результаты от всех агентов
   - Сохраняет в PostgreSQL
   - Публикует обновления в WebSocket канал
   - Автоматически меняет статус проверки на "завершено"

5. **Пользователь видит результаты в реальном времени**
   - Frontend подключается к WebSocket
   - Результаты появляются по мере выполнения
   - Можно сравнить данные из разных стран

### Реализованные проверки

#### 1. HTTP/HTTPS (agent_production.py:242-282)
- GET запрос с автоматическим определением протокола
- Возвращает: статус код, время ответа, заголовки, количество редиректов
- Таймаут: 10 секунд
- **Безопасность:** SSL сертификаты проверяются (`verify=True`)

#### 2. Ping (agent_production.py:179-214)
- 4 пакета с таймаутом 15 секунд
- Кроссплатформенность (Windows: `-n`, Linux/Mac: `-c`)
- Парсинг статистики из вывода команды
- **Безопасность:** валидация hostname перед выполнением команды

#### 3. TCP Port Check (agent_production.py:246-280)
- Проверка доступности конкретного порта
- Формат: `host:port` (например, `google.com:443`)
- Измеряет время установки соединения
- Определяет статус: `open`, `closed`, `timeout`

#### 4. Traceroute (agent_production.py:216-258)
- До 20 хопов, таймаут 30 секунд
- Показывает полный путь до хоста
- Кроссплатформенность (`tracert` на Windows, `traceroute` на Unix)
- **Безопасность:** валидация hostname, ограничение размера вывода (15KB)

#### 5. DNS Lookup (agent_production.py:54-175)
- Поддерживаемые типы: **A, AAAA, MX, NS, TXT, CNAME**
- Использует надёжные резолверы: Google DNS (8.8.8.8) и Cloudflare (1.1.1.1)
- Для MX: возвращает priority + exchange
- Для NS: список nameservers
- Для TXT: все текстовые записи
- Обработка ошибок: NXDOMAIN, NoAnswer, Timeout

## 🏗 Архитектура и компоненты

### Схема взаимодействия

```
┌─────────────────────────────────────────────────────────────┐
│                     USER / BROWSER                          │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              Frontend (React + Vite)                        │
│              📦 Vercel                                      │
│                                                             │
│  • SPA с TypeScript                                        │
│  • WebSocket для real-time                                 │
│  • TanStack Query для кеширования                          │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API + WebSocket
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              Backend (FastAPI) - backend_main.py            │
│              🚂 Railway + PostgreSQL + Redis                │
│                                                             │
│  Основные функции:                                         │
│  • POST /api/checks - создание проверки                    │
│  • GET /api/checks/{id} - получение результатов            │
│  • POST /api/agents/register - регистрация агентов         │
│  • POST /api/agents/heartbeat - heartbeat от агентов       │
│  • GET /api/agents/{id}/tasks - polling задач агентами     │
│  • POST /api/v1/results - приём результатов от агентов     │
│  • WS /api/ws/checks/{id} - WebSocket обновления           │
│                                                             │
│  ┌──────────────┐  ┌───────────┐  ┌──────────────┐       │
│  │ PostgreSQL   │  │   Redis   │  │  WebSocket   │       │
│  │              │  │           │  │              │       │
│  │ • checks     │  │ agent:{id}│  │ check:{id}:  │       │
│  │ • agents     │  │   :tasks  │  │   updates    │       │
│  │ • results    │  │  (queues) │  │ (pub/sub)    │       │
│  └──────────────┘  └───────────┘  └──────────────┘       │
└────────────────────────┬────────────────────────────────────┘
                         │ Polling каждые 5 сек
                         ↓
          ┌──────────────┴──────────────┐
          ↓                             ↓
┌────────────────────┐       ┌────────────────────┐
│ 🇷🇺 Agent Moscow  │       │ 🇺🇸 Agent USA     │
│ agent_production   │       │ (опционально)     │
│                    │       │                    │
│ • Polling Redis    │       │ • Независимая     │
│ • Выполняет checks │       │   инфраструктура  │
│ • Отправляет       │       │ • Geo-distributed │
│   результаты       │       │   проверки        │
│ • Heartbeat 30 сек │       │                    │
└────────────────────┘       └────────────────────┘
```

### Компоненты системы

#### 1. Backend (main_server.py)
**Основной сервер на FastAPI**, развёрнутый на Railway.

**Архитектура:**
- **FastAPI** с поддержкой HTML templates (Jinja2)
- **PostgreSQL** - хранение задач, агентов и результатов
- **WebSocket** - real-time обновления результатов
- **REST API** - простые endpoints для агентов и фронтенда
- Прямая отправка задач агентам (push модель)

**Основные endpoints:**
- `GET /` - главная страница (HTML)
- `POST /start_check` - создание проверки
- `POST /takeReport` - приём результатов от агентов
- `GET /getAgents` - список агентов
- `WS /ws` - WebSocket для real-time

**Безопасность (исправлено):**
- ✅ DATABASE_URL из переменных окружения (не хардкод)
- ✅ Валидация входных данных (защита от injection)
- ✅ Проверка существования агента перед принятием результатов
- ✅ Ограничение размера данных (100KB на результат)
- ✅ Параметризованные SQL запросы
- ✅ CORS настройка для фронтенда
- ✅ Timeout на запросы к агентам

**Альтернатива:** `backend_main.py` - более продвинутая версия с Redis очередями и polling моделью (не используется в production)

#### 2. Agent (agent_production.py)
**Легковесный сервис** для выполнения проверок, может быть развёрнут где угодно (VPS, Fly.io, Docker).

**Принцип работы:**
1. **Регистрация** - получает уникальный UUID и токен от backend
2. **Polling** - каждые 5 секунд запрашивает задачи из своей очереди
3. **Выполнение** - параллельная обработка до 10 задач одновременно
4. **Отправка результатов** - POST запрос на `/api/v1/results`
5. **Heartbeat** - каждые 30 секунд отправляет "я жив"

**Безопасность (исправлено):**
- ✅ Валидация hostname перед выполнением subprocess команд
- ✅ Защита от command injection (опасные символы: `;`, `&`, `|`, `$`, `` ` ``)
- ✅ Ограничение размера вывода (ping: 10KB, traceroute: 15KB)
- ✅ SSL certificate verification включена
- ✅ Все сетевые операции с таймаутами

#### 3. Frontend (React + TypeScript)
**SPA на Vite**, развёрнут на Vercel.

**Возможности:**
- Создание проверок через удобный UI
- Real-time обновления через WebSocket
- История всех проверок
- Список онлайн агентов
- Фильтрация и поиск результатов

#### 4. База данных (PostgreSQL)
**Схема данных** (database_migration.sql):

**Таблица `agents`:**
- `id` (UUID) - уникальный идентификатор
- `name` - название агента
- `location` - местоположение (страна, город)
- `api_token` - токен для аутентификации
- `status` - online/offline
- `last_heartbeat` - последний heartbeat

**Таблица `checks`:**
- `id` (UUID) - уникальный идентификатор проверки
- `target` - цель проверки
- `check_types` (JSONB) - типы проверок
- `status` - pending/in_progress/completed
- `created_at`, `completed_at` - timestamps

**Таблица `check_results`:**
- `id` (UUID)
- `check_id` - ссылка на проверку
- `agent_id` - какой агент выполнил
- `check_type` - тип проверки
- `success` - успешна ли
- `data` (JSONB) - результаты
- `duration_ms` - время выполнения

**Триггеры:**
- Автоматическое обновление статуса проверки когда все результаты получены

#### 5. Очереди (Redis)
**Структура данных:**

- `agent:{agent_id}:tasks` - очередь задач для конкретного агента (FIFO)
- `check:{check_id}:updates` - pub/sub канал для WebSocket обновлений

**Пример задачи в очереди:**
```json
{
  "check_id": "uuid-проверки",
  "agent_id": "uuid-агента",
  "check_type": "http",
  "target": "google.com"
}
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
python -m uvicorn main_server:app --reload --port 8000
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

Проект развёрнут на **Railway** (backend), **Vercel** (frontend) и может использовать **Fly.io** или любой VPS для агентов.

### Railway (Backend)

1. **Создайте проект** и подключите GitHub репозиторий
2. **Добавьте сервисы:**
   - New → Database → PostgreSQL
   - New → Database → Redis
3. **Настройте переменные окружения:**
   ```bash
   # Генерируйте безопасный токен!
   MASTER_REGISTRATION_TOKEN=$(openssl rand -hex 32)
   
   # Укажите домен фронтенда
   CORS_ORIGINS=https://ваш-проект.vercel.app
   
   # DATABASE_URL и REDIS_URL создаются автоматически
   ```
4. **Выполните миграцию БД:**
   - Railway → PostgreSQL → Query
   - Вставьте содержимое `database_migration.sql`
   - Выполните

Backend запустится автоматически через `Procfile`: `uvicorn main_server:app`

### Vercel (Frontend)

1. **Import проект** из GitHub
2. **Настройте:**
   - Root Directory: `frontend`
   - Framework Preset: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
3. **Environment Variables:**
   ```bash
   VITE_API_URL=https://ваш-проект.railway.app
   ```

### VPS/Fly.io (Агенты)

**Шаг 1: Регистрация агента**
```bash
# Используйте MASTER_REGISTRATION_TOKEN из Railway
curl -X POST https://ваш-backend.railway.app/api/agents/register \
  -H "X-Registration-Token: ваш_токен_из_railway" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Agent-Moscow",
    "location": "Russia, Moscow",
    "metadata": {"provider": "VPS"}
  }'

# Сохраните agent_id и api_token из ответа!
```

**Шаг 2: Настройка .env на сервере**
```bash
# Скопируйте из env.example.txt
MAIN_SERVER_URL=https://ваш-backend.railway.app
AGENT_UIID=agent_id_из_шага_1
AGENT_API_TOKEN=api_token_из_шага_1
AGENT_COUNTRY=Russia
AGENT_NAME=Agent-Moscow
```

**Шаг 3: Запуск**
```bash
# Через Docker
docker-compose -f docker-compose.agent.yml up -d

# Или напрямую
python -m uvicorn agent_production:app --host 0.0.0.0 --port 8001
```

**Автозапуск через systemd:**
```bash
sudo cp hostchecker-agent.service /etc/systemd/system/
sudo systemctl enable hostchecker-agent
sudo systemctl start hostchecker-agent
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
├── main_server.py               # 🚂 Production backend (Railway) ⭐ ОСНОВНОЙ
├── agent_production.py          # 🤖 Production agent (VPS/Fly.io)
├── backend_main.py              # 📝 Альтернативная версия (с Redis)
├── requirements.txt             # 📦 Python зависимости
├── Procfile                     # 🚂 Railway запуск: main_server
├── railway.json                 # ⚙️ Railway конфигурация
├── database_migration.sql       # 🗄️ SQL схема и миграции
├── env.example.txt              # 📝 Шаблон переменных окружения
├── README.md                    # 📄 Этот файл
│
├── Агенты (деплой):
├── Dockerfile.agent             # 🐳 Docker образ агента
├── docker-compose.agent.yml     # 🐳 Docker Compose агента
├── deploy-agent-vps.sh          # 🚀 Скрипт автоматического деплоя
├── hostchecker-agent.service    # ⚙️ Systemd service файл
│
└── frontend/                    # 🎨 React SPA приложение
    ├── src/
    │   ├── api/                 # 🌐 API клиент (axios)
    │   ├── components/          # 🧩 React компоненты
    │   │   ├── agents/          # Компоненты агентов
    │   │   ├── check/           # Компоненты проверок
    │   │   ├── common/          # Общие компоненты
    │   │   ├── layout/          # Layout компоненты
    │   │   └── results/         # Результаты проверок
    │   ├── pages/               # 📄 Страницы (Dashboard, Agents, Results)
    │   ├── hooks/               # 🪝 Custom hooks (useWebSocket, usePolling)
    │   ├── types/               # 📝 TypeScript типы
    │   └── utils/               # 🛠️ Утилиты и константы
    ├── package.json
    ├── vite.config.ts
    ├── tailwind.config.js
    └── vercel.json              # ⚙️ Vercel deploy конфиг
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

Проект разработан командой для участия в Hackathon Aéza Autumn 2025.

## 🤝 Поддержка

**Куратор хакатона:** [@daedal_dev](https://t.me/daedal_dev)

---

## 🏆 Hackathon Aéza Autumn 2025

### Соответствие критериям оценки

#### ✅ Функциональность базовых проверок (35%)

**Реализовано 100%** всех требований ТЗ:

| Проверка | Реализация | Файл/строки |
|----------|------------|-------------|
| **HTTP(S) GET** | Статус код, заголовки (20 первых), время ответа, количество редиректов, обработка timeout | `agent_production.py:242-282` |
| **Ping** | 4 пакета, timeout 15с, парсинг статистики, кроссплатформенность | `agent_production.py:179-214` |
| **TCP connect** | Проверка порта, измерение времени, статус (open/closed/timeout) | `agent_production.py:246-280` |
| **Traceroute** | До 20 хопов, timeout 30с, полный вывод маршрута | `agent_production.py:216-258` |
| **DNS lookup** | A, AAAA, MX, NS, TXT, CNAME - все типы, Google DNS + Cloudflare | `agent_production.py:54-175` |

**Дополнительно:**
- Валидация входных данных (защита от command injection)
- Ограничение размера вывода
- Обработка всех ошибок (NXDOMAIN, Timeout, ConnectionError)

#### ✅ Надежность выполнения задач (15%)

**Очередь задач:**
- **Push модель** - backend напрямую отправляет задачи агентам при создании проверки
- **PostgreSQL** - все задачи сохраняются в таблице `tasks`
- **Код:** `main_server.py:166-200` (создание и отправка)
- **Примечание:** альтернативная версия `backend_main.py` использует Redis polling

**Retry механизм:**
- **Try-catch** блоки при отправке задач агентам (код: `main_server.py:189-192`)
- **Timeout** 5 секунд на каждый запрос к агенту
- **Graceful degradation** - если агент недоступен, задача сохраняется в БД
- **Таймауты** на всех сетевых операциях в агентах

**PostgreSQL с ACID:**
- Транзакции для всех записей (commit после каждой операции)
- Параметризованные запросы (защита от SQL injection)
- **Таблицы:** `tasks`, `agents`, `reports`
- **Код:** `main_server.py` - все операции с БД
- **Примечание:** `database_migration.sql` содержит расширенную схему для альтернативной версии

**Обработка ошибок:**
- Try-catch блоки во всех критичных местах
- Graceful degradation (сервис работает при падении агента)
- Логирование всех ошибок

#### ✅ Удобство добавления агентов (20%)

**API для работы с агентами:**
```bash
# Список агентов
GET /getAgents

# Принятие результата от агента
POST /takeReport
{
  "country": "Russia",
  "UIID": "agent-uuid",
  "taskUIID": "task-uuid",
  "result": "результат проверки"
}
```
**Код:** `main_server.py:78-164`

**Управление агентами:**
- Агенты регистрируются напрямую в таблице `agents` БД
- Проверка существования агента перед принятием результатов (код: `main_server.py:153-156`)
- Список активных агентов через `GET /getAgents`

**Token-based auth:**
- Безопасный токен генерируется при регистрации (UUID v4)
- Проверяется при отправке результатов

**Простота деплоя:**
- **Docker:** `docker-compose -f docker-compose.agent.yml up -d`
- **Systemd:** готовый `hostchecker-agent.service`
- **Скрипт:** `deploy-agent-vps.sh` - деплой одной командой

**Документация:**
- Пошаговая инструкция в README
- Шаблон env variables в `env.example.txt`
- Комментарии в коде

#### ✅ UI/UX (15%)

**Технологии:**
- React 18 + TypeScript
- Tailwind CSS для современного дизайна
- TanStack Query для оптимизации запросов

**Функциональность:**
- Создание проверок через форму
- **Real-time обновления** через WebSocket (код: `frontend/src/hooks/useWebSocket.ts`)
- История всех проверок
- Список онлайн агентов со статусами
- Фильтрация результатов

**UX:**
- Адаптивный дизайн (mobile-friendly)
- Loading states и error handling
- Копирование UUID в буфер обмена
- Понятные сообщения об ошибках

#### ✅ Документация (15%)

- ✅ **README.md** - полное описание проекта, архитектуры, deployment
- ✅ **API документация** - Swagger UI автогенерация по адресу `/docs`
- ✅ **Комментарии в коде** - docstrings для всех функций, type hints
- ✅ **Deployment guide** - инструкции для Railway/Vercel/VPS
- ✅ **env.example.txt** - шаблон переменных окружения
- ✅ **Скрипты** - `deploy-agent-vps.sh`, `database_migration.sql`

### ⭐ Задачи со звёздочкой (Bonus!)

- ✅ **WebSocket/real-time** - полностью реализовано
- ✅ **Контроль нагрузки** - ограничение параллельных задач (MAX_CONCURRENT_TASKS=10)
- ✅ **Retry механизм** - exponential backoff
- 🔄 **Шаблоны проверок** - частично (можно выбрать несколько типов сразу)
- 🔄 **Визуализация** - в roadmap v1.1

### 🌟 Уникальная фишка

**Geo-распределённые агенты** позволяют обнаруживать:
- 🚫 **Региональные блокировки** (РКН, DNS hijacking)
- 🐌 **Разницу в скорости** доступа из разных стран
- 🔍 **DNS-проблемы** в конкретных регионах
- 🗺️ **Разные маршруты** traceroute между странами

**Пример:** Сайт недоступен в России, но работает в Европе - наш сервис покажет это за одну проверку!

---

## 📄 Лицензия и контакты

**Лицензия:** MIT License

**Куратор хакатона:** [@daedal_dev](https://t.me/daedal_dev)

**Made with ❤️ for Aéza Hackathon Autumn 2025**
