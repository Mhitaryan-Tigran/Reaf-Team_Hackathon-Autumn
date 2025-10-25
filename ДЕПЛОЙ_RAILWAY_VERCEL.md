# 🚀 ДЕПЛОЙ НА RAILWAY + VERCEL - ПРОСТЫЕ ШАГИ

## 🎯 Что мы делаем

Вместо локального запуска (localhost) задеплоим на реальные сервера:
- **Railway** - backend + база данных
- **Vercel** - frontend (сайт)
- **VPS Aeza** - агент в России

**После деплоя:**
- ✅ Сайт будет доступен всем в интернете
- ✅ Можете выключить компьютер - всё продолжит работать
- ✅ Можете показывать жюри на хакатоне

---

## 📦 ЧАСТЬ 1: RAILWAY (Backend) - 15 минут

### Шаг 1.1: Создать аккаунт Railway

1. Откройте https://railway.app
2. Нажмите **"Start a New Project"** или **"Login"**
3. Выберите **"Login with GitHub"**
4. Разрешите доступ
5. ✅ Готово!

### Шаг 1.2: Создать новый проект

1. Нажмите **"New Project"** (большая кнопка)
2. Выберите **"Deploy from GitHub repo"**
3. Найдите ваш репозиторий: `Reaf-Team_Hackathon-Autumn`
4. Нажмите **"Deploy Now"**
5. Railway начнёт деплой...

⏳ Подождите 2-3 минуты. Railway автоматически обнаружит Python + Procfile.

### Шаг 1.3: Добавить PostgreSQL

1. В вашем проекте нажмите **"+ New"** (справа вверху)
2. Выберите **"Database"**
3. Выберите **"Add PostgreSQL"**
4. ✅ PostgreSQL создан!

Railway автоматически добавит переменную `DATABASE_URL` в ваш backend.

### Шаг 1.4: Добавить Redis

1. Снова нажмите **"+ New"**
2. Выберите **"Database"**
3. Выберите **"Add Redis"**
4. ✅ Redis создан!

Railway автоматически добавит переменную `REDIS_URL`.

### Шаг 1.5: Настроить переменные окружения

1. Кликните на ваш **backend service** (не на PostgreSQL или Redis!)
2. Перейдите на вкладку **"Variables"**
3. Нажмите **"+ New Variable"**

Добавьте:

**Переменная 1:**
```
Name:  CORS_ORIGINS
Value: *
```
(Пока `*` для тестирования, потом заменим на Vercel URL)

**Переменная 2:**
```
Name:  MASTER_REGISTRATION_TOKEN
Value: hackathon-aeza-2025
```

4. Нажмите **"Add"** для каждой переменной

### Шаг 1.6: Получить URL backend'а

1. В backend service перейдите в **"Settings"**
2. Найдите секцию **"Networking"**
3. Нажмите **"Generate Domain"**
4. Скопируйте URL! Например: `hostchecker-production-abc123.up.railway.app`

**📝 СОХРАНИТЕ ЭТОТ URL!** Он понадобится для frontend и агента!

### Шаг 1.7: Инициализировать базу данных

1. Кликните на **PostgreSQL** (не backend!)
2. Перейдите на вкладку **"Data"** или **"Query"**
3. Откройте файл `database_migration.sql` на вашем компьютере
4. **Скопируйте ВСЁ** из файла
5. **Вставьте** в Query Editor в Railway
6. Нажмите **"Run"** или **"Execute"**
7. ✅ Таблицы созданы!

### Шаг 1.8: Проверить что работает

Откройте в браузере:
```
https://ваш-url.railway.app/health
```

Должно показать:
```json
{"database":"healthy","redis":"healthy","overall":"healthy"}
```

✅ **Backend на Railway готов!**

---

## 🎨 ЧАСТЬ 2: VERCEL (Frontend) - 10 минут

### Шаг 2.1: Создать аккаунт Vercel

1. Откройте https://vercel.com
2. Нажмите **"Sign Up"**
3. Выберите **"Continue with GitHub"**
4. Разрешите доступ
5. ✅ Готово!

### Шаг 2.2: Import проекта

1. Нажмите **"Add New..."** → **"Project"**
2. Найдите репозиторий `Reaf-Team_Hackathon-Autumn`
3. Нажмите **"Import"**

### Шаг 2.3: Настроить проект

⚠️ **ВАЖНО! Настройте правильно:**

**Framework Preset:** `Vite`

**Root Directory:** Нажмите **"Edit"** → выберите **`frontend`** ← ОБЯЗАТЕЛЬНО!

**Build Command:** `npm run build` (по умолчанию)

**Output Directory:** `dist` (по умолчанию)

### Шаг 2.4: Добавить переменную окружения

Прокрутите вниз до **"Environment Variables"**

Нажмите **"Add"**:

```
Name:  VITE_API_URL
Value: https://ваш-railway-url.railway.app
```

⚠️ **Вставьте ВАШЕ Railway URL из Части 1, Шаг 1.6!**

Примените для: **Production, Preview, Development** (все галочки)

### Шаг 2.5: Deploy!

1. Нажмите **"Deploy"**
2. Подождите 2-3 минуты (Vercel соберёт и задеплоит)
3. ✅ Готово!

### Шаг 2.6: Получить URL сайта

После деплоя вы увидите URL, например:
```
https://reaf-team-hackathon-autumn.vercel.app
```

Или:
```
https://hostchecker.vercel.app
```

**📝 СОХРАНИТЕ ЭТОТ URL!**

### Шаг 2.7: Обновить CORS на Railway

1. Вернитесь в **Railway**
2. Откройте ваш **backend service**
3. Перейдите в **"Variables"**
4. Найдите `CORS_ORIGINS`
5. Измените на: `https://ваш-vercel-url.vercel.app`
6. Сохраните

Backend автоматически перезапустится.

### Шаг 2.8: Проверить сайт

Откройте ваш Vercel URL в браузере!

Сайт должен работать! ✅

---

## 🇷🇺 ЧАСТЬ 3: AGENT НА VPS AEZA - 20 минут

Теперь подключим агента на VPS Aeza к Railway backend.

### Шаг 3.1: Зарегистрировать агента

На вашем компьютере выполните (замените YOUR-RAILWAY-URL!):

```bash
curl -X POST https://YOUR-RAILWAY-URL.railway.app/api/agents/register \
  -H "Content-Type: application/json" \
  -H "X-Registration-Token: hackathon-aeza-2025" \
  -d '{
    "name": "Agent-Moscow-Aeza",
    "location": "Russia, Moscow",
    "metadata": {"provider": "Aeza", "ip": "138.124.14.179"}
  }'
```

**📝 СОХРАНИТЕ agent_id и api_token из ответа!**

### Шаг 3.2: Подключиться к VPS

```bash
ssh root@138.124.14.179
```

**Пароль:** `pd91BP0G5b60`

### Шаг 3.3: Установить Docker (на VPS)

```bash
# Обновить систему
apt update

# Установить Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Установить Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Проверить
docker --version
docker-compose --version
```

### Шаг 3.4: Создать директорию

```bash
mkdir -p /opt/hostchecker-agent
cd /opt/hostchecker-agent
```

### Шаг 3.5: Загрузить файлы

**НОВЫЙ ТЕРМИНАЛ на вашем компьютере:**

```bash
cd /Users/slava/Hack2025/Reaf-Team_Hackathon-Autumn

scp agent_production.py root@138.124.14.179:/opt/hostchecker-agent/
scp requirements.txt root@138.124.14.179:/opt/hostchecker-agent/
scp Dockerfile.agent root@138.124.14.179:/opt/hostchecker-agent/
scp docker-compose.agent.yml root@138.124.14.179:/opt/hostchecker-agent/
```

**Пароль (4 раза):** `pd91BP0G5b60`

### Шаг 3.6: Создать конфигурацию (на VPS)

```bash
cd /opt/hostchecker-agent
nano .env.agent
```

**Вставьте (замените на ВАШИ значения!):**

```env
MAIN_SERVER_URL=https://ваш-railway-url.railway.app
AGENT_COUNTRY=Russia
AGENT_NAME=Agent-Moscow-Aeza
AGENT_UIID=ваш_agent_id_из_шага_3.1
AGENT_API_TOKEN=ваш_api_token_из_шага_3.1
POLL_INTERVAL=5
MAX_CONCURRENT_TASKS=10
PORT=8001
```

**Сохранить:** `Ctrl+X` → `Y` → `Enter`

### Шаг 3.7: Запустить агента (на VPS)

```bash
cd /opt/hostchecker-agent

docker-compose -f docker-compose.agent.yml build
docker-compose -f docker-compose.agent.yml up -d

# Посмотреть логи
docker-compose -f docker-compose.agent.yml logs -f
```

В логах должно быть:
```
🚀 Agent starting: Agent-Moscow-Aeza (Russia)
💓 Heartbeat sent
📡 Task poller started
```

**Ctrl+C** для выхода из логов (агент продолжит работать)

### Шаг 3.8: Проверить

На VPS:
```bash
curl http://localhost:8001/
```

С вашего компьютера:
```bash
curl http://138.124.14.179:8001/
```

---

## 🎉 ГОТОВО!

Теперь у вас:
- ✅ **Frontend:** https://ваш-сайт.vercel.app
- ✅ **Backend:** https://ваш-api.railway.app  
- ✅ **Agent:** 138.124.14.179 (VPS Aeza, Москва 🇷🇺)

**Всё работает в интернете!** Можно показывать жюри!

---

## 🧪 ТЕСТИРОВАНИЕ

1. Откройте **ваш Vercel URL** в любом браузере
2. Перейдите в "Агенты" - должен быть Agent-Moscow-Aeza 🟢
3. Dashboard → введите `edu.donstu.ru`
4. Выберите: HTTP, Ping, DNS
5. Нажмите "Создать проверку"
6. Смотрите результаты от агента из России!

---

## 📝 КРАТКАЯ ИНСТРУКЦИЯ

### Railway (Backend):
1. https://railway.app → Sign up with GitHub
2. New Project → Deploy from GitHub repo
3. Добавить PostgreSQL (+ New → Database → PostgreSQL)
4. Добавить Redis (+ New → Database → Redis)
5. Variables: CORS_ORIGINS=*, MASTER_REGISTRATION_TOKEN=hackathon-aeza-2025
6. Settings → Generate Domain → **СОХРАНИТЕ URL**
7. PostgreSQL → Query → вставьте `database_migration.sql`

### Vercel (Frontend):
1. https://vercel.com → Sign up with GitHub
2. Add New → Project → Import вашего репо
3. **Root Directory: `frontend`** ← ОБЯЗАТЕЛЬНО!
4. Environment Variable: `VITE_API_URL` = ваш Railway URL
5. Deploy!

### VPS Aeza (Agent):
1. Зарегистрировать через API (curl команда)
2. `ssh root@138.124.14.179` (пароль: pd91BP0G5b60)
3. Установить Docker
4. Загрузить файлы (scp команды)
5. Создать `.env.agent` с вашими credentials
6. `docker-compose up -d`

---

## 🆘 Если что-то не работает

### Railway

**Deployment failed:**
- Проверьте что `Procfile` и `requirements.txt` в корне проекта
- Посмотрите логи деплоя

**Database не подключается:**
- PostgreSQL → Variables → проверьте `DATABASE_URL`
- Убедитесь что миграция выполнена

### Vercel

**Build failed:**
- Проверьте что Root Directory = `frontend`
- Проверьте логи билда

**API не отвечает:**
- Проверьте `VITE_API_URL` в Variables
- Убедитесь что Railway backend работает (откройте /health)

### Agent

**Offline:**
- Проверьте `.env.agent` на VPS
- Убедитесь что `MAIN_SERVER_URL` указывает на Railway (не localhost!)
- Посмотрите логи: `docker-compose logs`

---

## ✅ ИТОГОВЫЙ ЧЕКЛИСТ

### Railway
- [ ] Аккаунт создан
- [ ] Проект задеплоен
- [ ] PostgreSQL добавлен
- [ ] Redis добавлен
- [ ] Environment variables настроены
- [ ] Domain сгенерирован
- [ ] База данных инициализирована
- [ ] Health check работает (/health)

### Vercel
- [ ] Аккаунт создан
- [ ] Репозиторий импортирован
- [ ] Root Directory = frontend
- [ ] VITE_API_URL настроен
- [ ] Deploy успешен
- [ ] Сайт открывается

### VPS Aeza
- [ ] Агент зарегистрирован через API
- [ ] SSH подключение работает
- [ ] Docker установлен
- [ ] Файлы загружены
- [ ] .env.agent создан с правильными данными
- [ ] Docker compose up выполнен
- [ ] Агент online в UI

---

## 🎬 ЧТО ПОЛУЧИТСЯ

После всех шагов:

**Адреса (замените на ваши):**
- 🌐 Сайт: https://hostchecker.vercel.app
- 🔧 API: https://hostchecker.railway.app
- 🇷🇺 Agent: http://138.124.14.179:8001

**Можете:**
- Открыть сайт с любого устройства
- Выключить компьютер - всё работает
- Поделиться ссылкой
- Показать жюри на хакатоне

---

## 📞 Помощь

**Детальные инструкции:**
- `DEPLOYMENT.md` - полное руководство (800+ строк)
- `VPS_AEZA_SETUP.md` - детали про VPS
- `КОМАНДЫ_ДЛЯ_AEZA.txt` - готовые команды

**Куратор хакатона:** @daedal_dev

---

<div align="center">

# 🚀 УДАЧИ С ДЕПЛОЕМ! 🚀

**Призовой фонд: 75,000 рублей**

</div>

