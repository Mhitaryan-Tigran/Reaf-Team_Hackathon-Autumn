# 🌐 Host Checker & DNS Resolver Service

> Распределённый сервис для проверки доступности хостов и DNS-резолвинга с поддержкой множественных агентов

[![Hackathon](https://img.shields.io/badge/Hackathon-Aeza-blue)](https://aeza.net)
[![Prize](https://img.shields.io/badge/Prize-75%2C000₽-green)](https://aeza.net)
[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://python.org)
[![React](https://img.shields.io/badge/React-18-blue)](https://react.dev)

---

## 📋 О проекте

**Host Checker** - это веб-сервис для проверки доступности сайтов и хостов с множества серверов в разных локациях одновременно.

### 💡 Зачем это нужно?
Когда сайт не работает, непонятно - это только у вас проблема или у всех? Наш сервис проверяет доступность с разных точек мира и показывает, где именно возникают проблемы.

### ✨ Основные возможности
- ✅ **HTTP/HTTPS проверки** - статус, заголовки, время ответа
- ✅ **Ping** - проверка доступности на сетевом уровне
- ✅ **DNS lookup** - резолвинг A, AAAA, MX, NS, TXT записей
- ✅ **TCP Port** - проверка открытых портов
- ✅ **Traceroute** - отслеживание маршрута до хоста
- ✅ **Распределённые агенты** - проверки из разных стран
- ✅ **Real-time обновления** - WebSocket для живых результатов
- ✅ **Красивый UI** - интуитивный веб-интерфейс

---

## 🚀 Быстрый старт за 3 шага

### 1. Клонировать репозиторий
```bash
git clone https://github.com/Mhitaryan-Tigran/Reaf-Team_Hackathon-Autumn.git
cd Reaf-Team_Hackathon-Autumn
```

### 2. Запустить через Docker
```bash
# Скопировать переменные окружения
cp .env.example .env

# Запустить все сервисы
docker-compose up -d

# Проверить статус
docker-compose ps
```

### 3. Открыть приложение
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

**Готово!** 🎉 Можно создавать первую проверку!

---

## 🛠 Стек технологий

```
┌─────────────────────────────────────────┐
│           TECH STACK                    │
├─────────────────────────────────────────┤
│ Backend:    FastAPI (Python 3.11+)     │
│ Frontend:   React 18 + TypeScript       │
│ Database:   PostgreSQL 15               │
│ Queue:      Redis 7                     │
│ Agent:      Python CLI                  │
│ Deploy:     Docker Compose              │
│ Styling:    Tailwind CSS                │
└─────────────────────────────────────────┘
```

### Почему именно этот стек?
- **FastAPI** - быстрая разработка + автоматическая документация + async
- **React** - богатая экосистема + TypeScript для типобезопасности
- **PostgreSQL** - JSONB для гибкого хранения результатов
- **Redis** - универсальное решение: очередь + кэш + pub/sub
- **Docker** - одинаковая работа везде

---

## 🏗 Архитектура

```
┌─────────────────────────────────────────────────────────┐
│                   USER / BROWSER                        │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/WebSocket
                     ↓
┌─────────────────────────────────────────────────────────┐
│               FRONTEND (React SPA)                      │
│  • Dashboard • Results Page • Agents Status             │
└────────────────────┬────────────────────────────────────┘
                     │ REST API
                     ↓
┌─────────────────────────────────────────────────────────┐
│               BACKEND (FastAPI)                         │
│  • API Endpoints • Task Manager • Agent Manager         │
└────────┬─────────────────────┬──────────────────────────┘
         │                     │
         ↓                     ↓
┌──────────────┐      ┌──────────────┐
│ PostgreSQL   │      │    Redis     │
│  • Checks    │      │  • Queue     │
│  • Agents    │      │  • Cache     │
│  • Results   │      │  • Pub/Sub   │
└──────────────┘      └──────┬───────┘
                             │ Poll tasks
                             ↓
                  ┌─────────────────────┐
                  │  AGENTS (Python)    │
                  │  • Agent 1 (Moscow) │
                  │  • Agent 2 (London) │
                  │  • Agent 3 (Tokyo)  │
                  │  ...                │
                  └─────────────────────┘
```

---

## 📚 Полная документация

Все инструкции находятся в папке **[`docs/`](docs/)**:

### 🎯 Для начала работы
- 📖 **[START_HERE.md](docs/START_HERE.md)** - НАЧНИ ЗДЕСЬ! Маршруты обучения
- ⚡ **[QUICKSTART.md](docs/QUICKSTART.md)** - Запуск за 5 минут
- 📑 **[INDEX.md](docs/INDEX.md)** - Навигация по всей документации

### 📋 Планирование
- 📝 **[IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md)** - Детальный план на 16 часов
- 📊 **[SUMMARY.md](docs/SUMMARY.md)** - Краткая сводка проекта
- 🛠 **[STACK_SUMMARY.md](docs/STACK_SUMMARY.md)** - Обоснование стека

### 🏗 Архитектура и структура
- 🏗 **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Полная архитектура системы
- 📁 **[PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)** - Структура + шаблоны кода

### 🚀 Деплой и решения
- ❓ **[FAQ.md](docs/FAQ.md)** - Частые вопросы и решения
- 🚀 **[DEPLOYMENT_STRATEGY.md](docs/DEPLOYMENT_STRATEGY.md)** - Стратегия деплоя

---

## 💻 Разработка

### Структура проекта
```
Reaf-Team_Hackathon-Autumn/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # REST endpoints
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   └── services/    # Business logic
│   ├── Dockerfile
│   └── pyproject.toml
│
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── api/         # API client
│   │   └── hooks/       # Custom hooks
│   ├── Dockerfile
│   └── package.json
│
├── agent/               # Python agent
│   ├── agent/
│   │   ├── checks/      # Check implementations
│   │   ├── main.py      # Agent main loop
│   │   └── client.py    # API client
│   ├── Dockerfile
│   └── pyproject.toml
│
├── docs/                # 📚 Документация
│   ├── START_HERE.md
│   ├── QUICKSTART.md
│   ├── IMPLEMENTATION_PLAN.md
│   ├── ARCHITECTURE.md
│   └── ...
│
├── docker-compose.yml   # Docker Compose config
├── .env.example         # Переменные окружения
└── README.md            # Этот файл
```

### Локальная разработка

#### Backend
```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

#### Agent
```bash
cd agent
poetry install
export AGENT_TOKEN=your-token
poetry run python -m agent.main
```

---

## 🔑 Регистрация агента

### Получить токен
```bash
curl -X POST http://localhost:8000/api/agents/register \
  -H "X-Registration-Token: master-token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Agent",
    "location": "Moscow, Russia"
  }'
```

### Запустить агента
```bash
docker run -d \
  -e API_URL=http://backend:8000 \
  -e AGENT_TOKEN=generated-token \
  -e AGENT_NAME="Moscow-Agent-1" \
  -e AGENT_LOCATION="Moscow, Russia" \
  hostchecker/agent:latest
```

---

## 📊 Примеры использования

### Создать проверку через API
```bash
curl -X POST http://localhost:8000/api/checks \
  -H "Content-Type: application/json" \
  -d '{
    "target": "google.com",
    "checks": ["http", "ping", "dns"],
    "agents": ["all"]
  }'
```

### Получить результаты
```bash
curl http://localhost:8000/api/checks/{check_id}
```

### Список агентов
```bash
curl http://localhost:8000/api/agents
```

---

## 🎯 Критерии оценки (75,000₽)

| Критерий | Вес | Что оценивается |
|----------|-----|-----------------|
| **Функциональность** | 35% | HTTP, Ping, DNS, TCP, Traceroute |
| **Надёжность** | 15% | Очередь, retry, сохранение |
| **Удобство агентов** | 20% | Регистрация, токены, heartbeat |
| **UI/UX** | 15% | Форма проверки, результаты |
| **Документация** | 15% | README, инструкции |

---

## ⏱ Оценка времени

### MVP (Минимальная рабочая версия)
**Время:** 12-16 часов

| Компонент | Время |
|-----------|-------|
| Backend (API + БД) | 5 ч |
| Agent (проверки) | 4 ч |
| Frontend (UI) | 5 ч |
| Docker + Docs | 2 ч |

### С бонусными фичами
**Время:** 20-24 часа
- WebSocket real-time: +2-3 ч
- GeoIP визуализация: +3 ч
- Traceroute: +2 ч

---

## 🐛 Troubleshooting

### Сервисы не запускаются
```bash
docker-compose logs -f
docker-compose restart
```

### CORS ошибки
Проверь `backend/app/main.py` - должен быть настроен CORSMiddleware

### База данных
```bash
docker-compose exec backend alembic upgrade head
```

Больше решений в **[FAQ.md](docs/FAQ.md)**

---

## 🤝 Помощь и поддержка

### Куратор хакатона
**Telegram:** [@daedal_dev](https://t.me/daedal_dev)

### Полезные ссылки
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **React Docs**: https://react.dev
- **PostgreSQL**: https://postgresql.org/docs
- **Redis**: https://redis.io/docs

### Если застрял
1. 📖 Проверь [FAQ.md](docs/FAQ.md)
2. 📚 Изучи [документацию](docs/)
3. 💬 Спроси куратора
4. 🤖 Используй AI помощников (ChatGPT/Cursor)

---

## 📈 Roadmap

- [x] **Phase 0:** Документация
- [ ] **Phase 1:** Backend MVP (5 ч)
- [ ] **Phase 2:** Agent MVP (4 ч)
- [ ] **Phase 3:** Frontend MVP (5 ч)
- [ ] **Phase 4:** Integration (2 ч)
- [ ] **Phase 5:** Bonus Features

Детальный план в **[IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md)**

---

## 📝 Чеклист перед сдачей

### Обязательно
- [ ] `docker-compose up` запускает всё
- [ ] Все базовые проверки работают
- [ ] UI интуитивный и красивый
- [ ] README заполнен
- [ ] Код в SourceCraft
- [ ] Презентация готова

### Бонусы
- [ ] WebSocket real-time
- [ ] Traceroute с визуализацией
- [ ] GeoIP карта
- [ ] Метрики и статистика

---

## 🎓 Для разработчиков

### Начать разработку

#### С нуля (следуй гайду)
```bash
# 1. Прочитай документацию
cat docs/START_HERE.md

# 2. Следуй плану
cat docs/IMPLEMENTATION_PLAN.md

# 3. Используй шаблоны
cat docs/PROJECT_STRUCTURE.md
```

#### Уже есть код
```bash
# 1. Запусти
docker-compose up -d

# 2. Проверь
docker-compose ps
docker-compose logs -f
```

### Полезные команды

```bash
# Логи
docker-compose logs -f backend

# Миграции
docker-compose exec backend alembic upgrade head

# Масштабирование агентов
docker-compose up -d --scale agent=3

# Очистка
docker-compose down -v
```

---

## 🏆 О хакатоне

**Название:** Aeza Hackathon Autumn 2024  
**Кейс:** Сервис проверки хостов и DNS резолвинга  
**Призовой фонд:** 75,000 рублей  
**Команда:** Reaf Team

### Оценка
- ✅ Функциональность базовых проверок (35%)
- ✅ Надёжность выполнения задач (15%)
- ✅ Удобство добавления агентов (20%)
- ✅ UI/UX (15%)
- ✅ Документация (15%)

---

## 📄 Лицензия

MIT License - см. [LICENSE](LICENSE)

---

## 🎊 Acknowledgments

- **Aeza** - за организацию хакатона
- **Куратор** - @daedal_dev
- **Команда** - Reaf Team

---

## 🚀 Начать разработку

**Готов начать?**

1. Прочитай **[docs/START_HERE.md](docs/START_HERE.md)** - выбери свой уровень
2. Запусти через **[docs/QUICKSTART.md](docs/QUICKSTART.md)** - 5 минут
3. Следуй **[docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md)** - 16 часов

**Удачи! Ты справишься! 💪**

---

<p align="center">
  Made with ❤️ for <a href="https://aeza.net">Aeza</a> Hackathon
</p>

<p align="center">
  <strong>Host Checker & DNS Resolver Service</strong>
</p>
