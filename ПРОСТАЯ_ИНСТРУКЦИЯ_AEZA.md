# 🇷🇺 Подключение агента на VPS Aeza - ПРОСТЫЕ ШАГИ

## ШАГ 1: Зарегистрировать агента (на вашем компьютере)

```bash
curl -X POST http://localhost:8000/api/agents/register \
  -H "Content-Type: application/json" \
  -H "X-Registration-Token: hackathon-aeza-2025" \
  -d '{
    "name": "Agent-Moscow-Aeza",
    "location": "Russia, Moscow",
    "metadata": {"provider": "Aeza", "ip": "138.124.14.179"}
  }'
```

**СОХРАНИТЕ ОТВЕТ!** Скопируйте `agent_id` и `api_token`

Пример ответа:
```json
{
  "agent_id": "abc-123-def-456",
  "api_token": "xyz-789-token",
  "message": "Agent registered successfully"
}
```

---

## ШАГ 2: Подключиться к VPS Aeza

```bash
ssh root@138.124.14.179
```

**Пароль:** `pd91BP0G5b60`

---

## ШАГ 3: Установить Docker на VPS

```bash
# На VPS выполните:
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Установить Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Проверить
docker --version
docker-compose --version
```

---

## ШАГ 4: Создать директорию для агента

```bash
# На VPS
mkdir -p /opt/hostchecker-agent
cd /opt/hostchecker-agent
```

---

## ШАГ 5: Загрузить файлы на VPS

**Вариант A: Через SCP (с вашего компьютера)**

Откройте **НОВЫЙ ТЕРМИНАЛ** на вашем компьютере:

```bash
cd /Users/slava/Hack2025/Reaf-Team_Hackathon-Autumn

# Создать временную директорию
mkdir -p /tmp/hostchecker-deploy
cp agent_production.py /tmp/hostchecker-deploy/
cp requirements.txt /tmp/hostchecker-deploy/
cp Dockerfile.agent /tmp/hostchecker-deploy/
cp docker-compose.agent.yml /tmp/hostchecker-deploy/

# Загрузить на VPS
scp /tmp/hostchecker-deploy/* root@138.124.14.179:/opt/hostchecker-agent/
```

**Пароль:** `pd91BP0G5b60`

**Вариант B: Через Git (проще)**

На VPS:
```bash
cd /opt/hostchecker-agent

# Если у вас есть GitHub repo
git clone https://github.com/your-username/your-repo.git .

# Или скопируйте файлы вручную
```

---

## ШАГ 6: Создать конфигурацию агента

На VPS выполните:

```bash
cd /opt/hostchecker-agent

# Создать .env.agent файл
cat > .env.agent << 'EOF'
MAIN_SERVER_URL=http://localhost:8000
AGENT_COUNTRY=Russia
AGENT_NAME=Agent-Moscow-Aeza
AGENT_UIID=ВСТАВЬТЕ_agent_id_ИЗ_ШАГА_1
AGENT_API_TOKEN=ВСТАВЬТЕ_api_token_ИЗ_ШАГА_1
POLL_INTERVAL=5
MAX_CONCURRENT_TASKS=10
PORT=8001
EOF

# ⚠️ ВАЖНО: Отредактируйте файл и вставьте ВАШИ значения!
nano .env.agent
```

**Замените:**
- `ВСТАВЬТЕ_agent_id_ИЗ_ШАГА_1` → на ваш `agent_id`
- `ВСТАВЬТЕ_api_token_ИЗ_ШАГА_1` → на ваш `api_token`

**Если backend на вашем компьютере** (не на Railway):
- `MAIN_SERVER_URL=http://ВАШ_ЛОКАЛЬНЫЙ_IP:8000`
  
Узнать ваш IP:
```bash
# На вашем компьютере
ifconfig | grep "inet " | grep -v 127.0.0.1
```

Сохранить файл: `Ctrl+X`, затем `Y`, затем `Enter`

---

## ШАГ 7: Запустить агента

На VPS:

```bash
cd /opt/hostchecker-agent

# Собрать Docker образ
docker-compose -f docker-compose.agent.yml build

# Запустить агента
docker-compose -f docker-compose.agent.yml up -d

# Посмотреть логи
docker-compose -f docker-compose.agent.yml logs -f
```

**Нажмите Ctrl+C чтобы выйти из логов** (агент продолжит работать)

---

## ШАГ 8: Проверить что агент работает

### На VPS:
```bash
curl http://localhost:8001/
```

Должно вернуть:
```json
{
  "status": "healthy",
  "agent": "Agent-Moscow-Aeza",
  "location": "Russia",
  ...
}
```

### С вашего компьютера:
```bash
curl http://138.124.14.179:8001/
```

### В браузере:
Откройте http://localhost:3000 → перейдите в **"Агенты"**

Должен появиться **Agent-Moscow-Aeza** со статусом **🟢 online**

---

## ✅ ГОТОВО!

Теперь можете:
1. Открыть http://localhost:3000
2. Ввести `edu.donstu.ru` или любой другой сайт
3. Выбрать проверки (HTTP, Ping, DNS)
4. Нажать **"Создать проверку"**
5. Увидеть результаты от агента из России! 🇷🇺

---

## 🔧 Полезные команды для VPS

```bash
# Статус контейнера
docker-compose -f /opt/hostchecker-agent/docker-compose.agent.yml ps

# Логи
docker-compose -f /opt/hostchecker-agent/docker-compose.agent.yml logs -f

# Перезапуск
docker-compose -f /opt/hostchecker-agent/docker-compose.agent.yml restart

# Остановка
docker-compose -f /opt/hostchecker-agent/docker-compose.agent.yml stop

# Запуск
docker-compose -f /opt/hostchecker-agent/docker-compose.agent.yml up -d
```

---

## 🆘 Troubleshooting

### Агент показывается offline

Проверьте `.env.agent` файл:
```bash
cat /opt/hostchecker-agent/.env.agent
```

Убедитесь что:
- `MAIN_SERVER_URL` правильный
- `AGENT_UIID` и `AGENT_API_TOKEN` правильные

### Backend недоступен с VPS

Если backend на вашем компьютере (localhost), VPS не сможет к нему подключиться!

**Решение:**
1. Узнайте ваш локальный IP: `ifconfig | grep "inet "`
2. В `.env.agent` замените `localhost` на ваш IP
3. Перезапустите агента: `docker-compose restart`

**Или задеплойте backend на Railway!** (см. DEPLOYMENT.md)

---

## 🎉 Успех!

Когда агент запустится, вы увидите в логах:
```
🚀 Agent starting: Agent-Moscow-Aeza (Russia)
💓 Heartbeat sent
📡 Task poller started
```

И в UI (http://localhost:3000/agents) появится агент!

---

**Следующий шаг:** Создайте проверку для `edu.donstu.ru` и увидите результаты! 🚀

