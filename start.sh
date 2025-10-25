#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║         🚀 Host Checker - Быстрый запуск                 ║"
echo "║         Aeza Hackathon Autumn 2025                       ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Функция для проверки Docker
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker не установлен!${NC}"
        echo "Установите Docker Desktop: https://www.docker.com/products/docker-desktop"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        echo -e "${RED}❌ Docker не запущен!${NC}"
        echo "Запустите Docker Desktop"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Docker готов${NC}"
}

# Функция проверки docker-compose
check_compose() {
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}❌ docker-compose не установлен!${NC}"
        echo "Установите: https://docs.docker.com/compose/install/"
        exit 1
    fi
    echo -e "${GREEN}✅ docker-compose готов${NC}"
}

# Меню выбора
echo -e "${YELLOW}Выберите вариант запуска:${NC}"
echo ""
echo "1. 🐳 Docker - Запустить ВСЁ в контейнерах (рекомендуется)"
echo "2. 💻 Локально - Запустить на вашем компьютере"
echo "3. 🌐 Production - Инструкция для деплоя на Railway/Vercel/VPS"
echo "4. 🆘 Помощь"
echo ""
read -p "Ваш выбор (1-4): " choice

case $choice in
    1)
        echo ""
        echo -e "${BLUE}🐳 Запуск через Docker...${NC}"
        echo ""
        
        check_docker
        check_compose
        
        echo ""
        echo -e "${YELLOW}📋 Что будет запущено:${NC}"
        echo "  - PostgreSQL (порт 5432)"
        echo "  - Redis (порт 6379)"
        echo "  - Backend API (порт 8000)"
        echo "  - Frontend (порт 3000)"
        echo "  - Agent (порт 8001)"
        echo ""
        
        read -p "Продолжить? (y/n) " -n 1 -r
        echo ""
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}🔨 Сборка и запуск контейнеров...${NC}"
            docker-compose -f docker-compose-full.yml up --build -d
            
            echo ""
            echo -e "${GREEN}✅ Всё запущено!${NC}"
            echo ""
            echo -e "${BLUE}📋 Доступ к сервисам:${NC}"
            echo "  🌐 Frontend:  http://localhost:3000"
            echo "  🔧 Backend:   http://localhost:8000"
            echo "  📖 API Docs:  http://localhost:8000/docs"
            echo "  🤖 Agent:     http://localhost:8001"
            echo ""
            echo -e "${YELLOW}📊 Посмотреть логи:${NC}"
            echo "  docker-compose -f docker-compose-full.yml logs -f"
            echo ""
            echo -e "${YELLOW}🛑 Остановить всё:${NC}"
            echo "  docker-compose -f docker-compose-full.yml down"
            echo ""
        else
            echo "Отменено"
        fi
        ;;
        
    2)
        echo ""
        echo -e "${BLUE}💻 Локальный запуск${NC}"
        echo ""
        echo "Смотрите файл: КАК_ЗАПУСТИТЬ.md"
        echo "Или: QUICKSTART.md"
        echo ""
        echo -e "${YELLOW}Краткая инструкция:${NC}"
        echo ""
        echo "1️⃣  Запустите БД в Docker:"
        echo "   docker run -d --name postgres -e POSTGRES_PASSWORD=hakatonski123 -e POSTGRES_USER=SERVER -e POSTGRES_DB=serverDB -p 5432:5432 postgres"
        echo "   docker run -d --name redis -p 6379:6379 redis"
        echo ""
        echo "2️⃣  Установите зависимости:"
        echo "   pip3 install -r requirements.txt"
        echo ""
        echo "3️⃣  Инициализируйте БД:"
        echo "   psql -h localhost -U SERVER -d serverDB -f database_migration.sql"
        echo ""
        echo "4️⃣  Запустите backend:"
        echo "   uvicorn backend_main:app --reload --port 8000"
        echo ""
        echo "5️⃣  Запустите frontend (в новом терминале):"
        echo "   cd frontend && npm install && npm run dev"
        echo ""
        ;;
        
    3)
        echo ""
        echo -e "${BLUE}🌐 Production деплой${NC}"
        echo ""
        echo "Смотрите файлы:"
        echo "  📖 DEPLOYMENT.md - полная инструкция"
        echo "  📝 DEPLOYMENT_MANIFEST.md - шпаргалка"
        echo "  🇷🇺 VPS_AEZA_SETUP.md - настройка VPS Aeza"
        echo ""
        echo -e "${YELLOW}Краткий план:${NC}"
        echo ""
        echo "1️⃣  Railway (Backend):"
        echo "   - Import GitHub repo"
        echo "   - Добавить PostgreSQL + Redis"
        echo "   - Настроить переменные окружения"
        echo "   - Выполнить миграцию БД"
        echo ""
        echo "2️⃣  Vercel (Frontend):"
        echo "   - Import GitHub repo"
        echo "   - Root directory = frontend"
        echo "   - Добавить VITE_API_URL"
        echo ""
        echo "3️⃣  VPS Aeza (Agent):"
        echo "   IP: 138.124.14.179"
        echo "   User: root"
        echo "   Password: pd91BP0G5b60"
        echo ""
        echo "   Запустите: ./deploy-agent-vps.sh"
        echo ""
        ;;
        
    4)
        echo ""
        echo -e "${BLUE}🆘 Помощь${NC}"
        echo ""
        echo "📁 Доступные файлы документации:"
        echo ""
        echo "  🚀 КАК_ЗАПУСТИТЬ.md - этот гайд в файле"
        echo "  ⚡ QUICKSTART.md - быстрый локальный запуск"
        echo "  🌐 DEPLOYMENT.md - production деплой"
        echo "  🇷🇺 VPS_AEZA_SETUP.md - настройка VPS"
        echo "  ✅ HACKATHON_CHECKLIST.md - чек-лист для презентации"
        echo "  📖 README.md - главная документация"
        echo "  🎯 START_HERE_RU.md - с чего начать"
        echo ""
        echo "📞 Контакты:"
        echo "  Telegram куратора: @daedal_dev"
        echo ""
        ;;
        
    *)
        echo -e "${RED}❌ Неверный выбор${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}Удачи! 🚀${NC}"

