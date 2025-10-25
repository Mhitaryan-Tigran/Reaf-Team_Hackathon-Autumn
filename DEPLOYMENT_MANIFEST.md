# 🚀 Deployment Manifest - Все что нужно для деплоя

Этот документ содержит все URL, переменные окружения и команды, которые понадобятся для деплоя.

## 📝 Environment Variables - Полный список

### Railway Backend

```env
# Auto-provided by Railway
DATABASE_URL=postgresql://postgres:password@container:5432/railway
REDIS_URL=redis://default:password@container:6379

# Manual configuration needed
CORS_ORIGINS=https://hostchecker.vercel.app,https://hostchecker-preview.vercel.app
MASTER_REGISTRATION_TOKEN=change-this-to-secure-random-token
PORT=8000
ENVIRONMENT=production
```

**Где взять:**
- `DATABASE_URL` - автоматически при добавлении PostgreSQL service
- `REDIS_URL` - автоматически при добавлении Redis service
- `CORS_ORIGINS` - замените на ваш Vercel URL после деплоя
- `MASTER_REGISTRATION_TOKEN` - сгенерируйте: `openssl rand -hex 32`

### Vercel Frontend

```env
# Production environment
VITE_API_URL=https://your-project.railway.app
```

**Где взять:**
- `VITE_API_URL` - ваш Railway backend URL (появится после деплоя)

### VPS Agent (.env.agent)

```env
# Main server
MAIN_SERVER_URL=https://your-project.railway.app

# Agent identification
AGENT_COUNTRY=Russia
AGENT_NAME=Agent-Moscow-Aeza

# Credentials (получить после регистрации агента)
AGENT_UIID=your-agent-uuid
AGENT_API_TOKEN=your-agent-token

# Performance settings
POLL_INTERVAL=5
MAX_CONCURRENT_TASKS=10
PORT=8001
```

**Где взять:**
- `MAIN_SERVER_URL` - ваш Railway backend URL
- `AGENT_UIID` и `AGENT_API_TOKEN` - из ответа API после регистрации агента

## 🔗 URLs после деплоя

### Production URLs (замените на свои)

| Компонент | URL | Статус |
|-----------|-----|--------|
| Frontend | `https://hostchecker.vercel.app` | 🔄 Заменить |
| Backend API | `https://hostchecker.railway.app` | 🔄 Заменить |
| API Docs | `https://hostchecker.railway.app/docs` | 🔄 Заменить |
| Agent (Moscow) | `http://138.124.14.179:8001` | ✅ Готово |

### GitHub Repository

```
https://github.com/your-username/hostchecker
```

## 📋 Пошаговый чеклист деплоя

### Phase 1: Подготовка (5 минут)

- [ ] Создать GitHub репозиторий
- [ ] Push всех файлов в main ветку
- [ ] Зарегистрироваться на Railway.app
- [ ] Зарегистрироваться на Vercel.com
- [ ] Проверить доступ к VPS Aeza (SSH)

### Phase 2: Railway Backend (15 минут)

- [ ] **1. Import GitHub repo в Railway**
  - New Project → Deploy from GitHub repo
  - Выбрать репозиторий

- [ ] **2. Добавить PostgreSQL**
  - В проекте: New → Database → PostgreSQL
  - Дождаться создания
  - `DATABASE_URL` появится автоматически

- [ ] **3. Добавить Redis**
  - В проекте: New → Database → Redis
  - Дождаться создания
  - `REDIS_URL` появится автоматически

- [ ] **4. Настроить environment variables**
  - Settings → Variables
  - Добавить `CORS_ORIGINS` (пока можно указать `*` для тестирования)
  - Добавить `MASTER_REGISTRATION_TOKEN` (сгенерировать случайный)

- [ ] **5. Generate Domain**
  - Settings → Generate Domain
  - Скопировать URL (например: `hostchecker.railway.app`)

- [ ] **6. Инициализация БД**
  - PostgreSQL → Query
  - Скопировать содержимое `database_migration.sql`
  - Execute

- [ ] **7. Проверка**
  ```bash
  curl https://your-project.railway.app/health
  ```
  Ожидаемый ответ: `{"database": "healthy", "redis": "healthy", "overall": "healthy"}`

**Railway URL:** `___________________________` (заполнить после деплоя)

### Phase 3: Vercel Frontend (10 минут)

- [ ] **1. Import GitHub repo в Vercel**
  - Add New → Project
  - Import Git Repository
  - Выбрать репозиторий

- [ ] **2. Configure Project**
  - Framework Preset: `Vite`
  - Root Directory: `frontend`
  - Build Command: `npm run build`
  - Output Directory: `dist`

- [ ] **3. Environment Variables**
  - Settings → Environment Variables
  - Добавить `VITE_API_URL` = ваш Railway URL
  - Для всех environments (Production, Preview, Development)

- [ ] **4. Deploy**
  - Deploy
  - Дождаться завершения (2-3 минуты)

- [ ] **5. Получить URL**
  - Скопировать production URL (например: `hostchecker.vercel.app`)

- [ ] **6. Обновить CORS на Railway**
  - Вернуться в Railway
  - Settings → Variables
  - Обновить `CORS_ORIGINS` на реальный Vercel URL
  - Redeploy backend

- [ ] **7. Проверка**
  - Открыть Vercel URL в браузере
  - Должна загрузиться главная страница

**Vercel URL:** `___________________________` (заполнить после деплоя)

### Phase 4: Agent на VPS Aeza (20 минут)

- [ ] **1. Регистрация агента через API**
  
  ```bash
  curl -X POST https://your-railway-url.railway.app/api/agents/register \
    -H "Content-Type: application/json" \
    -H "X-Registration-Token: your-master-token" \
    -d '{
      "name": "Agent-Moscow-Aeza",
      "location": "Russia, Moscow",
      "metadata": {
        "provider": "Aeza",
        "ip": "138.124.14.179"
      }
    }'
  ```
  
  **Сохранить ответ:**
  ```
  agent_id: ______________________________
  api_token: _____________________________
  ```

- [ ] **2. Деплой агента (автоматический способ)**
  
  ```bash
  chmod +x deploy-agent-vps.sh
  ./deploy-agent-vps.sh
  ```
  
  Скрипт спросит о настройке `.env.agent` - следуйте инструкциям

- [ ] **3. Или ручной деплой:**
  
  ```bash
  # A. Загрузить файлы на VPS
  scp agent_production.py root@138.124.14.179:/opt/hostchecker-agent/
  scp requirements.txt root@138.124.14.179:/opt/hostchecker-agent/
  scp Dockerfile.agent root@138.124.14.179:/opt/hostchecker-agent/
  scp docker-compose.agent.yml root@138.124.14.179:/opt/hostchecker-agent/
  
  # B. SSH на VPS
  ssh root@138.124.14.179
  
  # C. Установить Docker (если нужно)
  curl -fsSL https://get.docker.com -o get-docker.sh
  sh get-docker.sh
  
  # D. Установить Docker Compose (если нужно)
  curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  chmod +x /usr/local/bin/docker-compose
  
  # E. Создать .env.agent
  cd /opt/hostchecker-agent
  nano .env.agent
  # Вставить конфигурацию из секции "VPS Agent" выше
  
  # F. Запустить
  docker-compose -f docker-compose.agent.yml build
  docker-compose -f docker-compose.agent.yml up -d
  ```

- [ ] **4. Настроить systemd (опционально, для автозапуска)**
  
  ```bash
  cp hostchecker-agent.service /etc/systemd/system/
  systemctl daemon-reload
  systemctl enable hostchecker-agent.service
  systemctl start hostchecker-agent.service
  ```

- [ ] **5. Проверка**
  
  ```bash
  # Health check
  curl http://138.124.14.179:8001/
  
  # Статистика
  curl http://138.124.14.179:8001/stats
  
  # Логи
  docker-compose -f /opt/hostchecker-agent/docker-compose.agent.yml logs -f
  ```

- [ ] **6. Проверить в UI**
  - Открыть Vercel URL
  - Перейти в Agents
  - Агент должен быть "online" (зеленый)

### Phase 5: Финальное тестирование (10 минут)

- [ ] **1. Тест через UI**
  - Открыть фронтенд
  - Dashboard → Создать проверку для `google.com`
  - Выбрать: HTTP, Ping, DNS
  - Нажать "Start Check"
  - Перейти в Results
  - Убедиться что результаты появились

- [ ] **2. Тест через API**
  
  ```bash
  # Создать проверку
  curl -X POST https://your-railway-url.railway.app/api/checks \
    -H "Content-Type: application/json" \
    -d '{
      "target": "google.com",
      "checks": ["http", "ping", "dns"]
    }'
  
  # Получить результаты (использовать id из ответа выше)
  curl https://your-railway-url.railway.app/api/checks/{check-id}
  ```

- [ ] **3. Проверить все endpoints**
  - Health: `/health`
  - API Docs: `/docs`
  - Agents list: `/api/agents`
  - Checks list: `/api/checks`

## 🔑 Credentials Template

### Railway
```
Account Email: _________________________
Project Name: __________________________
Backend URL: ___________________________
PostgreSQL URL: ________________________
Redis URL: _____________________________
```

### Vercel
```
Account Email: _________________________
Project Name: __________________________
Frontend URL: __________________________
```

### VPS Aeza
```
IP: 138.124.14.179
User: root
Password: pd91BP0G5b60
SSH Key: _______________________________
```

### Tokens
```
MASTER_REGISTRATION_TOKEN: _____________
Agent-Moscow-Aeza ID: __________________
Agent-Moscow-Aeza Token: _______________
```

## 🆘 Quick Fixes

### Backend не запускается

```bash
# Railway Logs
railway logs

# Проверить переменные окружения
railway variables

# Redeploy
railway up
```

### Frontend показывает ошибки API

```bash
# Проверить VITE_API_URL
vercel env ls

# Добавить/обновить переменную
vercel env add VITE_API_URL

# Redeploy
vercel --prod
```

### Agent offline

```bash
# На VPS проверить статус
docker-compose -f /opt/hostchecker-agent/docker-compose.agent.yml ps

# Логи
docker-compose -f /opt/hostchecker-agent/docker-compose.agent.yml logs

# Restart
docker-compose -f /opt/hostchecker-agent/docker-compose.agent.yml restart

# Проверить .env.agent
cat /opt/hostchecker-agent/.env.agent
```

### База данных пустая

```bash
# Railway PostgreSQL → Query
# Выполнить database_migration.sql снова
```

## 📊 Monitoring URLs

После деплоя:

- Railway Dashboard: https://railway.app/dashboard
- Vercel Dashboard: https://vercel.com/dashboard
- Backend Health: https://your-project.railway.app/health
- Backend API Docs: https://your-project.railway.app/docs
- Frontend: https://your-app.vercel.app
- Agent Health: http://138.124.14.179:8001/

## ✅ Success Criteria

Все должно быть ✅:

- [ ] Backend health возвращает "healthy"
- [ ] Frontend загружается без ошибок
- [ ] Agent показывается как "online" в UI
- [ ] Можно создать проверку через UI
- [ ] Результаты появляются в течение 10 секунд
- [ ] API docs доступны
- [ ] Все endpoints отвечают

## 🎉 Готово!

Когда все пункты выше выполнены, проект полностью задеплоен и готов к презентации!

**Финальный чеклист:**
- [ ] Заполнены все URL в этом документе
- [ ] Заполнены все credentials
- [ ] Все компоненты работают
- [ ] Проведено полное тестирование
- [ ] Screenshots для презентации готовы
- [ ] Репозиторий актуален

---

**Команда Reaf Team**
**Aéza Hackathon Autumn 2025**

