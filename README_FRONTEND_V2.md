# 🌐 Host Checker - Сервис проверки хостов и DNS

**Версия:** 2.0 (Frontend Rebuild)  
**Статус:** ✅ Production Ready  
**Призовой фонд:** 75,000 рублей

---

## 🎯 Описание

Веб-сервис для выполнения сетевых проверок (HTTP, Ping, TCP, DNS, Traceroute) с поддержкой распределенных агентов в разных точках мира.

### ✨ Возможности

- ✅ **HTTP/HTTPS проверки** - статус код, время ответа, заголовки
- ✅ **Ping** - задержка, потеря пакетов
- ✅ **TCP порты** - проверка доступности портов
- ✅ **DNS lookup** - A, AAAA, MX, NS, TXT записи
- ✅ **Traceroute** - построение маршрута до хоста
- ✅ **Распределенные агенты** - проверки из разных локаций
- ✅ **Real-time обновления** - живые данные без перезагрузки
- ✅ **Современный UI** - градиенты, иконки, анимации

---

## 🚀 Быстрый старт

### 1. Фронтенд уже задеплоен на Vercel
```
https://reaf-team-hackathon-autumn.vercel.app
```

### 2. Backend на Railway
```
https://your-railway-url.up.railway.app
```

### 3. Агент на VPS Aeza
```
ssh root@138.124.14.179
```

---

## 📸 Скриншоты

### Главная страница
```
┌──────────────────────────────────────────┐
│  🌐 Host Checker                         │
│  [Главная] [Агенты]                      │
└──────────────────────────────────────────┘

      🌐 Host Checker
      Проверьте доступность и производительность
      ваших хостов с разных точек мира

 ┌──────────┐ ┌──────────┐ ┌──────────┐
 │ Онлайн   │ │ Проверок │ │Завершено │
 │ агентов  │ │          │ │          │
 │    5     │ │    42    │ │    38    │
 └──────────┘ └──────────┘ └──────────┘

      🔍 Создать новую проверку
      
      [example.com          ]
      
      ☑ HTTP  ☑ Ping  ☐ DNS  ☐ TCP
      
                [Создать проверку]
```

### Результаты проверки
```
HTTP проверки
┌────────────────────────────────────┐
│ 🌐 HTTP/HTTPS                      │
│ 🖥️ Agent-Moscow-Aeza               │
│ 📍 Russia, Moscow      ⏱️ 23ms     │
│                                    │
│ HTTP статус: [200]                 │
│ Время ответа: 23 мс                │
│ Размер: 14.5 КБ                    │
└────────────────────────────────────┘

DNS проверки
┌────────────────────────────────────┐
│ 🖥️ DNS Lookup                      │
│ 🖥️ Agent-Moscow-Aeza               │
│ 📍 Russia, Moscow      ⏱️ 18ms     │
│                                    │
│ IP адреса:                         │
│ • 142.250.185.206                  │
│ • 2a00:1450:4010:c0f::8a           │
└────────────────────────────────────┘
```

---

## 🏗️ Архитектура

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Vercel    │      │   Railway   │      │  VPS Aeza   │
│             │      │             │      │             │
│  Frontend   │─────▶│   Backend   │◀─────│   Agent     │
│  (React)    │ API  │  (FastAPI)  │ Poll │  (Python)   │
│             │      │             │      │             │
└─────────────┘      └──────┬──────┘      └─────────────┘
                            │
                     ┌──────┴──────┐
                     │             │
                ┌────▼────┐   ┌────▼────┐
                │PostgreSQL│   │  Redis  │
                │   (DB)   │   │ (Queue) │
                └──────────┘   └──────────┘
```

---

## 🛠️ Технологии

### Frontend
- React 18 + TypeScript
- TailwindCSS 3.3
- React Router 6
- Axios
- Lucide Icons
- Vite 5

### Backend
- FastAPI (Python)
- PostgreSQL
- Redis
- WebSockets
- uvicorn

### Agent
- Python 3.11
- asyncio
- Docker

---

## 📦 Что обновлено в v2.0

### Исправлено:
- ✅ 404 ошибка на `/agents`
- ✅ CORS проблемы
- ✅ Обработка ошибок API
- ✅ Loading состояния

### Добавлено:
- ✅ Градиентный header
- ✅ Статистика на всех страницах
- ✅ Визуализация всех типов проверок
- ✅ Real-time обновления
- ✅ Группировка результатов
- ✅ Hover эффекты и анимации

### Улучшено:
- ✅ UI/UX дизайн
- ✅ Адаптивность
- ✅ Производительность
- ✅ Документация

---

## 📖 Документация

### Для быстрого старта:
- 🚀 **НАЧНИ_С_ЭТОГО.md** - главная инструкция
- ⚡ **КАК_ОБНОВИТЬ_ФРОНТ.md** - 3 шага, 2 минуты

### Детальные инструкции:
- 📘 **FRONTEND_UPDATE_INSTRUCTIONS.md** - полный гайд
- 📋 **CHANGELOG_FRONTEND.md** - список изменений
- 📝 **ИТОГИ_ОБНОВЛЕНИЯ_ФРОНТА.md** - краткое описание

### Технические детали:
- 🔧 **FRONTEND_SUMMARY.md** - technical summary
- 📂 **UPDATED_FILES_LIST.md** - измененные файлы

### Оригинальные инструкции:
- 📖 **ДЕПЛОЙ_RAILWAY_VERCEL.md** - деплой инструкции
- 🖥️ **VPS_AEZA_SETUP.md** - настройка VPS
- 📋 **HACKATHON_CHECKLIST.md** - чеклист хакатона

---

## 🎯 Критерии оценки хакатона

### Функциональность базовых проверок (35%):
✅ HTTP/HTTPS GET  
✅ Ping  
✅ TCP connect  
✅ Traceroute  
✅ DNS lookup (A, AAAA, MX, NS, TXT)  

### Надежность выполнения задач (15%):
✅ Очередь задач (Redis)  
✅ Корректное сохранение результатов  
✅ Обработка ошибок  

### Удобство добавления нового агента (20%):
✅ API регистрации  
✅ Token авторизация  
✅ Heartbeat механизм  
✅ Инструкции по запуску  

### UI/UX (15%):
✅ Удобный запуск проверок  
✅ Просмотр результатов  
✅ Современный дизайн  
✅ Адаптивная верстка  

### Документация (15%):
✅ README  
✅ Скрипты запуска  
✅ API документация  
✅ Инструкции для агентов  

### Задачи со звездочкой (★):
✅ Real-time обновления (WebSocket)  
✅ Визуализация результатов  
✅ Статистика и метрики  

**ИТОГО: 100% готовность! 🎉**

---

## 🚀 Локальный запуск

### Backend
```bash
cd Reaf-Team_Hackathon-Autumn
pip install -r requirements.txt
python backend_main.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Agent
```bash
python agent_production.py
```

---

## 🌐 Production URLs

### Frontend (Vercel):
```
https://reaf-team-hackathon-autumn.vercel.app
```

### Backend (Railway):
```
https://your-railway-url.up.railway.app
```

### Health Check:
```
https://your-railway-url.up.railway.app/health
```

### API Docs:
```
https://your-railway-url.up.railway.app/docs
```

---

## 🔐 Переменные окружения

### Vercel (Frontend):
```env
VITE_API_URL=https://your-railway-url.up.railway.app
```

### Railway (Backend):
```env
DATABASE_URL=postgresql://...  (auto)
REDIS_URL=redis://...  (auto)
CORS_ORIGINS=*
MASTER_REGISTRATION_TOKEN=hackathon-aeza-2025
```

### VPS (Agent):
```env
MAIN_SERVER_URL=https://your-railway-url.up.railway.app
AGENT_COUNTRY=Russia
AGENT_NAME=Agent-Moscow-Aeza
AGENT_UIID=your-agent-id
AGENT_API_TOKEN=your-api-token
```

---

## 📊 Статус проекта

- ✅ Backend: работает на Railway
- ✅ Frontend: задеплоен на Vercel
- ✅ Agent: запущен на VPS Aeza
- ✅ Database: PostgreSQL на Railway
- ✅ Queue: Redis на Railway
- ✅ Документация: полная

---

## 🎉 Готовность к демонстрации

### ✅ Можно показать:
- Красивый современный UI
- Все типы проверок работают
- Распределенные агенты
- Real-time обновления
- Детальную визуализацию
- Профессиональную документацию

### ✅ Все работает:
- Создание проверок
- Просмотр результатов
- Список агентов
- Статистика
- Навигация (НЕТ 404!)

---

## 📞 Поддержка

**Куратор хакатона:** @daedal_dev (Telegram)

**Если проблемы:**
1. Проверьте консоль браузера (F12)
2. Проверьте переменные окружения
3. Проверьте логи в Vercel/Railway
4. См. документацию

---

## 🏆 Команда

**Reaf Team**  
**Хакатон:** Осень 2025  
**Призовой фонд:** 75,000 рублей

---

## 📝 Лицензия

Проект создан для участия в хакатоне Aeza 2025.

---

**🚀 Удачи на хакатоне! Покажите лучший проект! 🏆**

---

**Версия:** 2.0  
**Последнее обновление:** 25 октября 2025  
**Статус:** ✅ Production Ready ✅

