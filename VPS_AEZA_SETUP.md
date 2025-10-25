# 🇷🇺 Подключение к VPS Aeza - Пошаговая инструкция

## 📝 Данные VPS (из вашего скриншота)

```
🖥️  VPS от Aeza
─────────────────────────────────
IP:           138.124.14.179
Пользователь: root
Пароль:       pd91BP0G5b60
URL:          lk.hack-rnd.ru
─────────────────────────────────
```

## 🔐 Шаг 1: Подключение по SSH

### Вариант A: Подключение по паролю

```bash
ssh root@138.124.14.179
# Введите пароль: pd91BP0G5b60
```

### Вариант B: Настройка SSH ключа (рекомендуется)

```bash
# 1. Сгенерировать SSH ключ (если еще нет)
ssh-keygen -t ed25519 -C "hostchecker-aeza"

# 2. Скопировать ключ на VPS
ssh-copy-id root@138.124.14.179
# Введите пароль: pd91BP0G5b60

# 3. Теперь можно подключаться без пароля
ssh root@138.124.14.179
```

## 🚀 Шаг 2: Автоматический деплой агента

У нас есть автоматический скрипт! Просто запустите:

```bash
# На вашей локальной машине
cd /Users/slava/Hack2025/Reaf-Team_Hackathon-Autumn
chmod +x deploy-agent-vps.sh
./deploy-agent-vps.sh
```

Скрипт автоматически:
- ✅ Проверит SSH подключение
- ✅ Создаст директорию на VPS
- ✅ Загрузит файлы агента
- ✅ Установит Docker и Docker Compose
- ✅ Запустит агента в контейнере
- ✅ Настроит systemd для автозапуска

## 🔧 Шаг 3: Ручной деплой (если автоскрипт не работает)

### 3.1 Регистрация агента через API

**ВАЖНО:** Сначала зарегистрируйте агента на backend!

```bash
# Замените YOUR-RAILWAY-URL на ваш реальный URL
curl -X POST https://YOUR-RAILWAY-URL.railway.app/api/agents/register \
  -H "Content-Type: application/json" \
  -H "X-Registration-Token: your-master-token" \
  -d '{
    "name": "Agent-Moscow-Aeza",
    "location": "Russia, Moscow",
    "metadata": {
      "provider": "Aeza",
      "ip": "138.124.14.179",
      "hackathon": "autumn-2025"
    }
  }'
```

**Сохраните ответ:**
```json
{
  "agent_id": "СОХРАНИТЕ-ЭТОТ-ID",
  "api_token": "СОХРАНИТЕ-ЭТОТ-TOKEN",
  "message": "Agent registered successfully"
}
```

### 3.2 Подключение к VPS и установка

```bash
# Подключение
ssh root@138.124.14.179

# Создание директории
mkdir -p /opt/hostchecker-agent
cd /opt/hostchecker-agent
```

### 3.3 Загрузка файлов

**Вариант 1: SCP с локальной машины**

```bash
# На вашей локальной машине (НЕ на VPS!)
cd /Users/slava/Hack2025/Reaf-Team_Hackathon-Autumn

scp agent_production.py root@138.124.14.179:/opt/hostchecker-agent/
scp requirements.txt root@138.124.14.179:/opt/hostchecker-agent/
scp Dockerfile.agent root@138.124.14.179:/opt/hostchecker-agent/
scp docker-compose.agent.yml root@138.124.14.179:/opt/hostchecker-agent/
scp hostchecker-agent.service root@138.124.14.179:/opt/hostchecker-agent/
```

**Вариант 2: Git clone на VPS**

```bash
# На VPS
cd /opt
git clone YOUR-GITHUB-REPO hostchecker-agent
cd hostchecker-agent
```

### 3.4 Установка Docker

```bash
# На VPS
# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Установка Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Проверка
docker --version
docker-compose --version
```

### 3.5 Создание конфигурации агента

```bash
# На VPS
cd /opt/hostchecker-agent

# Создать .env.agent файл
nano .env.agent
```

**Вставьте:**
```env
# Main server URL (замените на ваш Railway URL!)
MAIN_SERVER_URL=https://YOUR-APP.railway.app

# Agent info
AGENT_COUNTRY=Russia
AGENT_NAME=Agent-Moscow-Aeza

# Credentials (из шага 3.1)
AGENT_UIID=paste-agent-id-here
AGENT_API_TOKEN=paste-api-token-here

# Settings
POLL_INTERVAL=5
MAX_CONCURRENT_TASKS=10
PORT=8001
```

Сохраните: `Ctrl+X`, затем `Y`, затем `Enter`

### 3.6 Запуск агента

```bash
# На VPS
cd /opt/hostchecker-agent

# Build образа
docker-compose -f docker-compose.agent.yml build

# Запуск
docker-compose -f docker-compose.agent.yml up -d

# Проверка логов
docker-compose -f docker-compose.agent.yml logs -f
```

### 3.7 Настройка автозапуска (systemd)

```bash
# На VPS
# Копирование service файла
cp /opt/hostchecker-agent/hostchecker-agent.service /etc/systemd/system/

# Обновление systemd
systemctl daemon-reload

# Включение автозапуска
systemctl enable hostchecker-agent.service

# Запуск сервиса
systemctl start hostchecker-agent.service

# Проверка статуса
systemctl status hostchecker-agent.service
```

## ✅ Шаг 4: Проверка работы

### 4.1 Health check

```bash
# С вашей локальной машины
curl http://138.124.14.179:8001/

# Ожидаемый ответ:
{
  "status": "healthy",
  "agent": "Agent-Moscow-Aeza",
  "location": "Russia",
  "agent_id": "...",
  "active_tasks": 0,
  "max_concurrent_tasks": 10
}
```

### 4.2 Статистика

```bash
curl http://138.124.14.179:8001/stats
```

### 4.3 Логи

```bash
# На VPS
docker-compose -f /opt/hostchecker-agent/docker-compose.agent.yml logs -f

# Или через systemd
journalctl -u hostchecker-agent.service -f
```

### 4.4 Проверка в UI

1. Откройте ваш фронтенд (Vercel URL)
2. Перейдите в раздел **Agents**
3. Агент "Agent-Moscow-Aeza" должен быть **🟢 online**

### 4.5 Тестовая проверка

1. В Dashboard создайте проверку для `google.com`
2. Выберите: HTTP, Ping, DNS
3. Нажмите "Start Check"
4. Перейдите в Results
5. Должны появиться результаты от агента из России

## 🔧 Troubleshooting

### Агент показывается offline

```bash
# Проверить что контейнер запущен
docker ps | grep hostchecker

# Проверить логи
docker-compose -f /opt/hostchecker-agent/docker-compose.agent.yml logs

# Проверить .env.agent файл
cat /opt/hostchecker-agent/.env.agent

# Проверить что MAIN_SERVER_URL правильный
# Проверить что AGENT_UIID и AGENT_API_TOKEN правильные
```

### Агент не получает задачи

```bash
# Проверить что agent зарегистрирован
curl https://YOUR-APP.railway.app/api/agents

# Перезапустить agent
docker-compose -f /opt/hostchecker-agent/docker-compose.agent.yml restart

# Проверить heartbeat
# Агент должен отправлять heartbeat каждые 30 секунд
```

### Ошибки выполнения проверок

```bash
# Войти в контейнер
docker exec -it hostchecker-agent-moscow bash

# Проверить что утилиты установлены
ping -c 1 google.com
traceroute -m 5 google.com
dig google.com
```

## 📊 Полезные команды

```bash
# Статус контейнера
docker-compose -f /opt/hostchecker-agent/docker-compose.agent.yml ps

# Логи
docker-compose -f /opt/hostchecker-agent/docker-compose.agent.yml logs -f

# Рестарт
docker-compose -f /opt/hostchecker-agent/docker-compose.agent.yml restart

# Остановка
docker-compose -f /opt/hostchecker-agent/docker-compose.agent.yml stop

# Удаление и пересоздание
docker-compose -f /opt/hostchecker-agent/docker-compose.agent.yml down
docker-compose -f /opt/hostchecker-agent/docker-compose.agent.yml up -d

# Просмотр ресурсов
docker stats hostchecker-agent-moscow

# Systemd статус
systemctl status hostchecker-agent.service

# Systemd логи
journalctl -u hostchecker-agent.service -f
```

## 🎯 Итоговый чеклист

- [ ] Подключился к VPS по SSH
- [ ] Зарегистрировал агента через API
- [ ] Сохранил `agent_id` и `api_token`
- [ ] Создал `.env.agent` с правильными credentials
- [ ] Установил Docker и Docker Compose
- [ ] Запустил агента через docker-compose
- [ ] Настроил systemd автозапуск
- [ ] Проверил health check (`http://138.124.14.179:8001/`)
- [ ] Агент показывается online в UI
- [ ] Создал тестовую проверку и получил результаты

## 🎉 Готово!

Ваш агент на VPS Aeza запущен и работает!

**IP:** 138.124.14.179  
**Локация:** Москва, Россия 🇷🇺  
**Статус:** 🟢 Online

---

**Следующие шаги:**
- Задеплойте backend на Railway (см. `DEPLOYMENT.md`)
- Задеплойте frontend на Vercel (см. `DEPLOYMENT.md`)
- Проведите полное тестирование системы

**Полезные ссылки:**
- [DEPLOYMENT.md](./DEPLOYMENT.md) - полная инструкция деплоя
- [HACKATHON_CHECKLIST.md](./HACKATHON_CHECKLIST.md) - чек-лист для презентации
- [README.md](./README.md) - главная документация

