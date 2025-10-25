# 🚀 Руководство по деплою Host Checker

Полное пошаговое руководство по развертыванию системы проверки хостов на Railway (backend), Vercel (frontend) и VPS Aeza (agent).

## 📋 Оглавление

1. [Обзор архитектуры](#обзор-архитектуры)
2. [Деплой Backend на Railway](#деплой-backend-на-railway)
3. [Деплой Frontend на Vercel](#деплой-frontend-на-vercel)
4. [Деплой Agent на VPS Aeza](#деплой-agent-на-vps-aeza)
5. [Настройка и тестирование](#настройка-и-тестирование)
6. [Troubleshooting](#troubleshooting)

---

## 🏗 Обзор архитектуры

```
┌────────────────────────────────────────────┐
│ Frontend (React + Vite)                    │
│ Vercel - автодеплой из GitHub             │
│ https://hostchecker.vercel.app             │
└────────────────┬───────────────────────────┘
                 │ HTTPS REST API
                 ↓
┌────────────────────────────────────────────┐
│ Backend (FastAPI)                          │
│ Railway - $5 free credits                 │
│ https://hostchecker.railway.app            │
│                                            │
│ ✅ PostgreSQL - хранение результатов     │
│ ✅ Redis - очереди задач                 │
│ ✅ WebSocket - real-time обновления      │
└────────────────┬───────────────────────────┘
                 │ Task Polling
                 ↓
┌────────────────────────────────────────────┐
│ 🇷🇺 Agent на VPS Aeza (Москва)          │
│ IP: 138.124.14.179                         │
│ Docker + systemd                           │
└────────────────────────────────────────────┘
```

---

## 🚂 Деплой Backend на Railway

### Шаг 1: Подготовка проекта

Railway автоматически определяет Python приложения и использует Procfile.

**Файлы уже созданы:**
- ✅ `backend_main.py` - основной сервер
- ✅ `requirements.txt` - зависимости
- ✅ `Procfile` - команда запуска
- ✅ `railway.json` - конфигурация Railway
- ✅ `database_migration.sql` - SQL схема

### Шаг 2: Создание проекта в Railway

1. **Зайдите на https://railway.app** и создайте аккаунт
2. **Создайте новый проект**: "New Project"
3. **Deploy from GitHub repo** - подключите ваш репозиторий
4. Railway автоматически обнаружит Python приложение

### Шаг 3: Добавление PostgreSQL

1. В вашем проекте нажмите **"+ New"**
2. Выберите **"Database" → "PostgreSQL"**
3. Railway автоматически создаст базу и добавит переменную `DATABASE_URL`

### Шаг 4: Добавление Redis

1. Нажмите **"+ New"** → **"Database" → "Redis"**
2. Railway создаст Redis instance и добавит переменную `REDIS_URL`

### Шаг 5: Настройка переменных окружения

В разделе **"Variables"** вашего backend сервиса добавьте:

```env
# Database (автоматически добавлено Railway)
DATABASE_URL=postgresql://...

# Redis (автоматически добавлено Railway)
REDIS_URL=redis://...

# CORS (замените на ваш Vercel домен)
CORS_ORIGINS=http://localhost:3000,https://hostchecker.vercel.app,https://your-app.vercel.app

# Agent Registration Token
MASTER_REGISTRATION_TOKEN=your-secure-token-here

# Port (опционально, Railway использует $PORT)
PORT=8000
```

### Шаг 6: Инициализация базы данных

1. **Откройте Railway PostgreSQL Query Editor:**
   - Перейдите в PostgreSQL service
   - Нажмите "Query"

2. **Выполните миграцию:**
   - Скопируйте содержимое `database_migration.sql`
   - Вставьте в Query Editor
   - Нажмите "Run"

3. **Проверьте таблицы:**
```sql
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
```

### Шаг 7: Деплой

1. Railway автоматически задеплоит приложение
2. Получите публичный URL: **Settings → Generate Domain**
3. Ваш backend будет доступен по адресу: `https://hostchecker.railway.app`

### Шаг 8: Проверка

Проверьте health check:
```bash
curl https://hostchecker.railway.app/health
```

Ожидаемый ответ:
```json
{
  "database": "healthy",
  "redis": "healthy",
  "overall": "healthy"
}
```

---

## 🎨 Деплой Frontend на Vercel

### Шаг 1: Подготовка

**Файлы уже созданы:**
- ✅ `frontend/vercel.json` - конфигурация
- ✅ `vercel.json` - root конфигурация
- ✅ `.vercelignore` - игнорируемые файлы

### Шаг 2: Подключение к Vercel

1. **Зайдите на https://vercel.com** и создайте аккаунт
2. **Import Git Repository:**
   - Нажмите "New Project"
   - Выберите ваш GitHub репозиторий
   - Нажмите "Import"

### Шаг 3: Настройка проекта

**Framework Preset:** Vite

**Root Directory:** `frontend`

**Build Command:**
```bash
npm run build
```

**Output Directory:**
```
dist
```

### Шаг 4: Environment Variables

Добавьте переменные окружения в **Settings → Environment Variables:**

```env
VITE_API_URL=https://hostchecker.railway.app
```

⚠️ **ВАЖНО:** Замените URL на ваш реальный Railway backend URL!

### Шаг 5: Деплой

1. Нажмите **"Deploy"**
2. Vercel автоматически соберет и задеплоит фронтенд
3. Получите публичный URL: `https://hostchecker.vercel.app`

### Шаг 6: Настройка автодеплоя

Vercel автоматически деплоит при каждом push в main ветку:
- ✅ Pull Request = Preview deployment
- ✅ Push to main = Production deployment

### Шаг 7: Обновление CORS на Backend

Вернитесь в Railway и обновите `CORS_ORIGINS`:
```env
CORS_ORIGINS=https://hostchecker.vercel.app,https://your-app.vercel.app
```

---

## 🖥 Деплой Agent на VPS Aeza

### Шаг 1: Доступ к VPS

**Данные VPS:**
- IP: `138.124.14.179`
- User: `root`
- Password: `pd91BP0G5b60`

Подключитесь по SSH:
```bash
ssh root@138.124.14.179
```

### Шаг 2: Регистрация агента

Сначала зарегистрируйте агента через API:

```bash
curl -X POST https://hostchecker.railway.app/api/agents/register \
  -H "Content-Type: application/json" \
  -H "X-Registration-Token: your-secure-token-here" \
  -d '{
    "name": "Agent-Moscow-Aeza",
    "location": "Russia, Moscow",
    "metadata": {
      "provider": "Aeza",
      "ip": "138.124.14.179"
    }
  }'
```

**Сохраните ответ:**
```json
{
  "agent_id": "uuid-here",
  "api_token": "token-here",
  "message": "Agent registered successfully"
}
```

### Шаг 3: Автоматический деплой (рекомендуется)

Используйте скрипт автоматического деплоя:

```bash
# На вашей локальной машине
chmod +x deploy-agent-vps.sh
./deploy-agent-vps.sh
```

Скрипт автоматически:
1. ✅ Проверит SSH подключение
2. ✅ Загрузит файлы на VPS
3. ✅ Установит Docker и Docker Compose
4. ✅ Настроит environment variables
5. ✅ Запустит агента в Docker контейнере
6. ✅ Настроит systemd service для автозапуска

### Шаг 4: Ручной деплой (альтернатива)

Если предпочитаете ручную настройку:

**4.1. Загрузите файлы на VPS:**
```bash
scp agent_production.py root@138.124.14.179:/opt/hostchecker-agent/
scp requirements.txt root@138.124.14.179:/opt/hostchecker-agent/
scp Dockerfile.agent root@138.124.14.179:/opt/hostchecker-agent/
scp docker-compose.agent.yml root@138.124.14.179:/opt/hostchecker-agent/
```

**4.2. На VPS установите Docker:**
```bash
ssh root@138.124.14.179

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

**4.3. Создайте .env.agent файл:**
```bash
cd /opt/hostchecker-agent
cat > .env.agent << EOF
MAIN_SERVER_URL=https://hostchecker.railway.app
AGENT_COUNTRY=Russia
AGENT_NAME=Agent-Moscow-Aeza
AGENT_UIID=your-agent-uuid-from-registration
AGENT_API_TOKEN=your-api-token-from-registration
POLL_INTERVAL=5
MAX_CONCURRENT_TASKS=10
PORT=8001
EOF
```

**4.4. Запустите агента:**
```bash
docker-compose -f docker-compose.agent.yml up -d
```

**4.5. Проверьте статус:**
```bash
docker-compose -f docker-compose.agent.yml ps
docker-compose -f docker-compose.agent.yml logs -f
```

### Шаг 5: Настройка автозапуска (systemd)

**5.1. Создайте systemd service:**
```bash
cp hostchecker-agent.service /etc/systemd/system/
```

**5.2. Активируйте service:**
```bash
systemctl daemon-reload
systemctl enable hostchecker-agent.service
systemctl start hostchecker-agent.service
```

**5.3. Проверьте статус:**
```bash
systemctl status hostchecker-agent.service
```

### Шаг 6: Проверка работы агента

**Health check:**
```bash
curl http://138.124.14.179:8001/
```

**Статистика:**
```bash
curl http://138.124.14.179:8001/stats
```

**Логи:**
```bash
docker-compose -f /opt/hostchecker-agent/docker-compose.agent.yml logs -f
```

---

## ✅ Настройка и тестирование

### Проверка интеграции

1. **Откройте фронтенд:** https://hostchecker.vercel.app

2. **Проверьте список агентов:**
   - Перейдите в раздел "Agents"
   - Агент должен быть в статусе "online" (зеленый)

3. **Создайте тестовую проверку:**
   - Перейдите в "Dashboard"
   - Введите: `google.com`
   - Выберите проверки: HTTP, Ping, DNS
   - Нажмите "Start Check"

4. **Просмотрите результаты:**
   - Перейдите в "Results"
   - Результаты должны появиться в течение 5-10 секунд
   - Для каждого агента должны быть результаты всех проверок

### Проверка API endpoints

**Список агентов:**
```bash
curl https://hostchecker.railway.app/api/agents
```

**Создать проверку:**
```bash
curl -X POST https://hostchecker.railway.app/api/checks \
  -H "Content-Type: application/json" \
  -d '{
    "target": "google.com",
    "checks": ["http", "ping", "dns"],
    "agents": null
  }'
```

**Получить результаты:**
```bash
curl https://hostchecker.railway.app/api/checks/{check_id}
```

---

## 🔧 Troubleshooting

### Backend проблемы

**Ошибка подключения к PostgreSQL:**
```bash
# Проверьте переменную DATABASE_URL в Railway
# Убедитесь, что PostgreSQL service запущен
```

**Ошибка подключения к Redis:**
```bash
# Проверьте переменную REDIS_URL
# Убедитесь, что Redis service запущен
```

**CORS ошибки:**
```bash
# Проверьте CORS_ORIGINS в Railway
# Добавьте все домены фронтенда (включая preview)
```

### Frontend проблемы

**API не отвечает:**
```bash
# Проверьте VITE_API_URL в Vercel
# Убедитесь, что backend доступен
curl https://hostchecker.railway.app/health
```

**Build ошибки:**
```bash
# Проверьте Node.js версию (должна быть 18+)
# Очистите cache и пересоберите
```

### Agent проблемы

**Агент offline:**
```bash
# Проверьте логи
docker-compose -f /opt/hostchecker-agent/docker-compose.agent.yml logs

# Проверьте .env.agent файл
cat /opt/hostchecker-agent/.env.agent

# Перезапустите агента
docker-compose -f /opt/hostchecker-agent/docker-compose.agent.yml restart
```

**Агент не получает задачи:**
```bash
# Проверьте AGENT_UIID и AGENT_API_TOKEN
# Убедитесь, что агент зарегистрирован:
curl https://hostchecker.railway.app/api/agents
```

**Ошибки выполнения проверок:**
```bash
# Проверьте, установлены ли утилиты
docker exec hostchecker-agent-moscow ping -c 1 google.com
docker exec hostchecker-agent-moscow traceroute -m 5 google.com
```

---

## 📊 Мониторинг

### Railway

- **Logs:** Railway Dashboard → Service → Logs
- **Metrics:** Railway Dashboard → Service → Metrics
- **Database:** Railway Dashboard → PostgreSQL → Query

### Vercel

- **Deployments:** Vercel Dashboard → Deployments
- **Analytics:** Vercel Dashboard → Analytics
- **Logs:** Vercel Dashboard → Logs

### VPS Agent

**Логи агента:**
```bash
docker-compose -f /opt/hostchecker-agent/docker-compose.agent.yml logs -f
```

**Системные логи:**
```bash
journalctl -u hostchecker-agent.service -f
```

**Статистика:**
```bash
curl http://localhost:8001/stats
```

---

## 🎉 Готово!

Ваша система Host Checker полностью развернута!

**Доступ:**
- 🌐 Frontend: https://hostchecker.vercel.app
- 🔧 Backend API: https://hostchecker.railway.app
- 🇷🇺 Agent (Moscow): http://138.124.14.179:8001

**Полезные ссылки:**
- [Railway Dashboard](https://railway.app/dashboard)
- [Vercel Dashboard](https://vercel.com/dashboard)
- [GitHub Repository](https://github.com/your-repo)

**Поддержка:**
- Telegram: @daedal_dev
- Email: support@hostchecker.app

