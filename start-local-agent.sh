#!/bin/bash
export MAIN_SERVER_URL=https://reaf-teamhackathon-autumn-production.up.railway.app
export AGENT_COUNTRY=Russia
export AGENT_NAME=Agent-Local-Test
export AGENT_UIID=local-test-agent-001
export AGENT_API_TOKEN=local-test-token
export POLL_INTERVAL=5
export MAX_CONCURRENT_TASKS=10
export PORT=8001

echo "🚀 Запуск агента..."
echo "📡 Server: $MAIN_SERVER_URL"
echo "🆔 Agent: $AGENT_NAME"
echo ""

uvicorn agent_production:app --host 0.0.0.0 --port 8001
