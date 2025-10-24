# 📚 Документация проекта - Навигация

> Полный набор документации для разработки сервиса проверки хостов и DNS-резолвинга

---

## 🚀 Быстрый старт

**Новичок?** Начни здесь:

1. 📖 **[README.md](README.md)** - главная страница с описанием проекта
2. ⚡ **[QUICKSTART.md](QUICKSTART.md)** - запуск за 5 минут
3. 🛠 **[STACK_SUMMARY.md](STACK_SUMMARY.md)** - краткая сводка по стеку

---

## 📋 Планирование и архитектура

### Перед началом разработки

- 📝 **[IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)**
  - Детальный план реализации
  - Оценка времени для каждого компонента
  - Приоритизация задач
  - Временная шкала разработки

- 🏗 **[ARCHITECTURE.md](ARCHITECTURE.md)**
  - High-level архитектура системы
  - Data flow диаграммы
  - Database schema
  - API endpoints
  - Deployment strategy

- 📁 **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)**
  - Полное дерево проекта
  - Шаблоны ключевых файлов
  - Структура backend/frontend/agent
  - Примеры кода

---

## 🛠 Технический стек

### Оптимальные технологии

**[STACK_SUMMARY.md](STACK_SUMMARY.md)**
- ✅ Рекомендуемый стек
- ⏱ Временные оценки
- 📊 Обоснование выбора
- 📦 Список зависимостей
- 🎯 Приоритизация фич

### Компоненты стека:

```
Backend:    FastAPI (Python 3.11+)
Frontend:   React 18 + TypeScript + Vite
Database:   PostgreSQL 15
Queue:      Redis 7
Agent:      Python CLI
Deploy:     Docker Compose
```

---

## 💻 Практические руководства

### Разработка

**[QUICKSTART.md](QUICKSTART.md)**
- 🚀 Запуск через Docker
- 🛠 Локальная разработка
- 🔑 Регистрация агента
- 📝 Первая проверка
- 🐛 Troubleshooting
- 📦 Полезные команды

### Проблемы и решения

**[FAQ.md](FAQ.md)**
- ❓ Общие вопросы
- 🔧 Технические вопросы
- 🐛 Проблемы и решения
- ⚡ Оптимизация
- 🚀 Развёртывание
- 💡 Советы для хакатона

---

## 📊 Оценка сложности

### Минимальная рабочая версия (MVP)

**Время:** 12-16 часов

| Компонент | Время | Сложность |
|-----------|-------|-----------|
| Backend | 5 ч | ⭐⭐⭐ |
| Agent | 4 ч | ⭐⭐ |
| Frontend | 5 ч | ⭐⭐⭐ |
| Docker + Docs | 2 ч | ⭐⭐ |

### С бонусными фичами

**Время:** 20-24 часа

- WebSocket real-time: +2-3 ч
- GeoIP визуализация: +3 ч
- Traceroute: +2 ч
- Метрики: +2 ч

---

## 🎯 Критерии оценки (75,000₽)

Распределение баллов:

- **35%** - Функциональность базовых проверок
  - HTTP/HTTPS, Ping, DNS, TCP, Traceroute
  
- **15%** - Надёжность выполнения задач
  - Очередь, retry, сохранение результатов
  
- **20%** - Удобство добавления агентов
  - API регистрации, токены, heartbeat
  
- **15%** - UI/UX
  - Удобство запуска и просмотра результатов
  
- **15%** - Документация
  - README, инструкции, демонстрация

---

## 📖 Детальная документация

### По компонентам

#### Backend (FastAPI)
- Структура: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md#backend)
- API: [ARCHITECTURE.md](ARCHITECTURE.md#api-endpoints)
- Миграции: [QUICKSTART.md](QUICKSTART.md#backend-fastapi)

#### Frontend (React)
- Структура: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md#frontend)
- Компоненты: [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md#phase-3-frontend-development)
- Hooks: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md#frontendappts)

#### Agent (Python)
- Структура: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md#agent)
- Проверки: [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md#phase-2-agent-development)
- Запуск: [QUICKSTART.md](QUICKSTART.md#регистрация-агента)

#### Infrastructure
- Docker: [QUICKSTART.md](QUICKSTART.md#запуск-через-docker)
- Database: [ARCHITECTURE.md](ARCHITECTURE.md#database-schema)
- Redis: [ARCHITECTURE.md](ARCHITECTURE.md#redis-queue)

---

## 🔍 Поиск по темам

### По функциональности

**Проверки хостов:**
- HTTP/HTTPS: [FAQ.md](FAQ.md#как-реализовать-ping-без-sudo) → `agent/checks/http.py`
- Ping: [FAQ.md](FAQ.md#как-реализовать-ping-без-sudo) → `agent/checks/ping.py`
- DNS: [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md#check-implementations) → `agent/checks/dns.py`
- TCP: [STACK_SUMMARY.md](STACK_SUMMARY.md#приоритет-1-easy-wins) → `agent/checks/tcp.py`
- Traceroute: [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md#traceroute-опционально-1-час) → `agent/checks/traceroute.py`

**Агенты:**
- Регистрация: [QUICKSTART.md](QUICKSTART.md#регистрация-агента)
- Heartbeat: [FAQ.md](FAQ.md#как-реализовать-heartbeat)
- Масштабирование: [ARCHITECTURE.md](ARCHITECTURE.md#scaling-agents)

**UI/UX:**
- Форма проверки: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md#frontendsrcappps)
- Результаты: [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md#results-page-1-час)
- Агенты: [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md#agents-page-1-час)

### По проблемам

**Ошибки:**
- CORS: [FAQ.md](FAQ.md#cors-блокирует-frontend)
- Ping в Docker: [FAQ.md](FAQ.md#ping-не-работает-в-docker)
- Redis connection: [FAQ.md](FAQ.md#redis-connection-refused)
- DB migrations: [FAQ.md](FAQ.md#database-migrations-failing)

**Оптимизация:**
- Скорость: [FAQ.md](FAQ.md#как-ускорить-проверки)
- Масштабирование: [FAQ.md](FAQ.md#как-масштабировать-систему)
- БД нагрузка: [FAQ.md](FAQ.md#как-уменьшить-нагрузку-на-бд)

**Deployment:**
- Локальный: [QUICKSTART.md](QUICKSTART.md#локальная-разработка-без-docker)
- Production: [FAQ.md](FAQ.md#как-задеплоить-на-production)
- Мониторинг: [ARCHITECTURE.md](ARCHITECTURE.md#monitoring)

---

## 📚 Рекомендуемый порядок чтения

### Для новичков

1. **[README.md](README.md)** - общий обзор
2. **[STACK_SUMMARY.md](STACK_SUMMARY.md)** - понять технологии
3. **[QUICKSTART.md](QUICKSTART.md)** - запустить проект
4. **[FAQ.md](FAQ.md)** - решить первые проблемы

### Для разработки

1. **[IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)** - план работы
2. **[ARCHITECTURE.md](ARCHITECTURE.md)** - понять архитектуру
3. **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - структура кода
4. **[FAQ.md](FAQ.md)** - решение проблем

### Для презентации

1. **[STACK_SUMMARY.md](STACK_SUMMARY.md)** - elevator pitch
2. **[ARCHITECTURE.md](ARCHITECTURE.md)** - архитектурные диаграммы
3. **[README.md](README.md)** - демонстрация возможностей

---

## 🎓 Дополнительные ресурсы

### Официальная документация

- **FastAPI**: https://fastapi.tiangolo.com
- **React**: https://react.dev
- **PostgreSQL**: https://postgresql.org/docs
- **Redis**: https://redis.io/docs
- **Docker**: https://docs.docker.com

### Полезные библиотеки

**Backend:**
- SQLAlchemy: https://sqlalchemy.org
- Alembic: https://alembic.sqlalchemy.org
- Pydantic: https://docs.pydantic.dev

**Frontend:**
- TanStack Query: https://tanstack.com/query
- React Router: https://reactrouter.com
- Tailwind CSS: https://tailwindcss.com

**Agent:**
- aiohttp: https://docs.aiohttp.org
- dnspython: https://dnspython.readthedocs.io
- ping3: https://github.com/kyan001/ping3

---

## ✅ Чеклисты

### Перед началом работы

- [ ] Прочитал [README.md](README.md)
- [ ] Изучил [STACK_SUMMARY.md](STACK_SUMMARY.md)
- [ ] Понял [ARCHITECTURE.md](ARCHITECTURE.md)
- [ ] Запустил проект через [QUICKSTART.md](QUICKSTART.md)
- [ ] Составил план по [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)

### Разработка MVP

- [ ] Backend API работает
- [ ] Agent выполняет проверки
- [ ] Frontend отображает результаты
- [ ] Docker Compose запускает всё
- [ ] Базовая документация написана

### Перед сдачей

- [ ] Все базовые проверки работают
- [ ] Агенты регистрируются и отправляют heartbeat
- [ ] UI интуитивный и красивый
- [ ] Docker запускается одной командой
- [ ] README с инструкциями готов
- [ ] Презентация подготовлена
- [ ] Код в SourceCraft

---

## 🎯 Контакты

**Куратор:** @daedal_dev (Telegram)

**Призовой фонд:** 75,000₽

**Deadline:** указан в условиях хакатона

---

## 📊 Статус документации

| Документ | Статус | Описание |
|----------|--------|----------|
| README.md | ✅ | Главная страница |
| QUICKSTART.md | ✅ | Быстрый старт |
| IMPLEMENTATION_PLAN.md | ✅ | План реализации |
| ARCHITECTURE.md | ✅ | Архитектура |
| STACK_SUMMARY.md | ✅ | Сводка по стеку |
| FAQ.md | ✅ | Частые вопросы |
| PROJECT_STRUCTURE.md | ✅ | Структура проекта |
| INDEX.md | ✅ | Навигация (этот файл) |

---

## 🔄 Обновления

**Версия:** 1.0.0  
**Дата:** 2024  
**Статус:** Готово к использованию

---

## 💡 Совет

> Не пытайся прочитать всё сразу!  
> Начни с [README.md](README.md) и [QUICKSTART.md](QUICKSTART.md),  
> остальное используй как справочник.

---

**Удачи в хакатоне! 🚀**

---

## 📌 Quick Links

- [🏠 Главная](README.md)
- [⚡ Быстрый старт](QUICKSTART.md)
- [📋 План реализации](IMPLEMENTATION_PLAN.md)
- [🏗 Архитектура](ARCHITECTURE.md)
- [🛠 Стек технологий](STACK_SUMMARY.md)
- [❓ FAQ](FAQ.md)
- [📁 Структура проекта](PROJECT_STRUCTURE.md)

