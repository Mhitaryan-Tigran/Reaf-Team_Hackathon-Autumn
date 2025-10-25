#!/bin/bash
# Скрипт для деплоя агента на VPS Aeza
# Использование: ./deploy-agent-vps.sh

set -e

echo "🚀 Deploying Host Checker Agent to VPS Aeza..."

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
VPS_IP="138.124.14.179"
VPS_USER="root"
DEPLOY_DIR="/opt/hostchecker-agent"

echo -e "${YELLOW}📋 VPS Configuration:${NC}"
echo "   IP: $VPS_IP"
echo "   User: $VPS_USER"
echo "   Deploy directory: $DEPLOY_DIR"
echo ""

# Check if SSH key is configured
echo -e "${YELLOW}🔑 Checking SSH connection...${NC}"
if ! ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no $VPS_USER@$VPS_IP "echo 'SSH OK'" > /dev/null 2>&1; then
    echo -e "${RED}❌ Cannot connect to VPS. Please check:${NC}"
    echo "   1. VPS IP address is correct"
    echo "   2. SSH key is added to VPS"
    echo "   3. VPS is running"
    exit 1
fi
echo -e "${GREEN}✅ SSH connection successful${NC}"
echo ""

# Create deploy directory
echo -e "${YELLOW}📁 Creating deploy directory...${NC}"
ssh $VPS_USER@$VPS_IP "mkdir -p $DEPLOY_DIR"

# Copy files to VPS
echo -e "${YELLOW}📤 Uploading files to VPS...${NC}"
scp -r \
    agent_production.py \
    requirements.txt \
    Dockerfile.agent \
    docker-compose.agent.yml \
    .env.agent.example \
    hostchecker-agent.service \
    $VPS_USER@$VPS_IP:$DEPLOY_DIR/

echo -e "${GREEN}✅ Files uploaded${NC}"
echo ""

# Install dependencies on VPS
echo -e "${YELLOW}🔧 Installing dependencies on VPS...${NC}"
ssh $VPS_USER@$VPS_IP << 'ENDSSH'
cd /opt/hostchecker-agent

# Update system
apt-get update

# Install Docker if not installed
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    systemctl enable docker
    systemctl start docker
    rm get-docker.sh
fi

# Install Docker Compose if not installed
if ! command -v docker-compose &> /dev/null; then
    echo "Installing Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

echo "✅ Dependencies installed"
ENDSSH

echo -e "${GREEN}✅ Dependencies installed${NC}"
echo ""

# Setup environment file
echo -e "${YELLOW}⚙️ Setting up environment...${NC}"
echo -e "${RED}⚠️ ВАЖНО: Вам нужно настроить .env.agent файл!${NC}"
echo ""
echo "Шаги:"
echo "1. Зарегистрируйте агента через API или UI"
echo "2. Получите AGENT_UIID и AGENT_API_TOKEN"
echo "3. SSH на VPS и отредактируйте /opt/hostchecker-agent/.env.agent"
echo ""
echo "Пример команды:"
echo -e "${YELLOW}ssh $VPS_USER@$VPS_IP${NC}"
echo -e "${YELLOW}cd $DEPLOY_DIR${NC}"
echo -e "${YELLOW}cp .env.agent.example .env.agent${NC}"
echo -e "${YELLOW}nano .env.agent${NC}"
echo ""

read -p "Вы настроили .env.agent файл? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}❌ Деплой отменен. Настройте .env.agent и запустите скрипт снова.${NC}"
    exit 1
fi

# Build and start Docker container
echo -e "${YELLOW}🐳 Building and starting Docker container...${NC}"
ssh $VPS_USER@$VPS_IP << 'ENDSSH'
cd /opt/hostchecker-agent

# Stop existing container if running
docker-compose -f docker-compose.agent.yml down || true

# Build and start
docker-compose -f docker-compose.agent.yml build
docker-compose -f docker-compose.agent.yml up -d

echo "✅ Docker container started"
ENDSSH

echo -e "${GREEN}✅ Docker container started${NC}"
echo ""

# Setup systemd service (optional)
echo -e "${YELLOW}🔧 Setup systemd service for auto-start? (y/n)${NC}"
read -p "" -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ssh $VPS_USER@$VPS_IP << 'ENDSSH'
cd /opt/hostchecker-agent

# Copy service file
cp hostchecker-agent.service /etc/systemd/system/

# Reload systemd
systemctl daemon-reload

# Enable service
systemctl enable hostchecker-agent.service

# Start service
systemctl start hostchecker-agent.service

echo "✅ Systemd service configured"
ENDSSH
    echo -e "${GREEN}✅ Systemd service configured${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Deployment complete!${NC}"
echo ""
echo "Полезные команды:"
echo -e "${YELLOW}# Проверить статус агента:${NC}"
echo "ssh $VPS_USER@$VPS_IP 'docker-compose -f $DEPLOY_DIR/docker-compose.agent.yml ps'"
echo ""
echo -e "${YELLOW}# Посмотреть логи:${NC}"
echo "ssh $VPS_USER@$VPS_IP 'docker-compose -f $DEPLOY_DIR/docker-compose.agent.yml logs -f'"
echo ""
echo -e "${YELLOW}# Перезапустить агента:${NC}"
echo "ssh $VPS_USER@$VPS_IP 'docker-compose -f $DEPLOY_DIR/docker-compose.agent.yml restart'"
echo ""
echo -e "${YELLOW}# Проверить health check:${NC}"
echo "curl http://$VPS_IP:8001/"
echo ""

