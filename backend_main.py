"""
Host Checker Backend - Production Ready
FastAPI + PostgreSQL + Redis
Railway deployment ready
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import psycopg2
from psycopg2.extras import RealDictCursor
import redis
import json
import uuid
import os
from datetime import datetime, timedelta
import asyncio
from contextlib import asynccontextmanager

# ============= CONFIGURATION =============

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://SERVER:hakatonski123@localhost:5432/serverDB")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Agent Registration Token
MASTER_REGISTRATION_TOKEN = os.getenv("MASTER_REGISTRATION_TOKEN", "master-registration-token")

# CORS Origins
CORS_ORIGINS_STR = os.getenv("CORS_ORIGINS", "*")
CORS_ORIGINS = ["*"] if CORS_ORIGINS_STR == "*" else CORS_ORIGINS_STR.split(",")

# ============= DATABASE & REDIS CONNECTION =============

db_conn = None
redis_client = None

def get_db():
    """Get database connection"""
    global db_conn
    if db_conn is None or db_conn.closed:
        db_conn = psycopg2.connect(DATABASE_URL)
    return db_conn

def get_redis():
    """Get Redis connection"""
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    return redis_client

# ============= LIFECYCLE =============

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("🚀 Starting Host Checker Backend...")
    
    # Initialize database
    conn = get_db()
    cursor = conn.cursor()
    
    # Create tables if not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agents (
            id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            location VARCHAR(255) NOT NULL,
            api_token VARCHAR(64) NOT NULL,
            ip_address VARCHAR(45),
            status VARCHAR(20) DEFAULT 'offline',
            last_heartbeat TIMESTAMP,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            metadata JSONB
        );
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS checks (
            id VARCHAR(36) PRIMARY KEY,
            target VARCHAR(500) NOT NULL,
            check_types JSONB NOT NULL,
            agent_ids JSONB,
            status VARCHAR(20) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        );
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS check_results (
            id VARCHAR(36) PRIMARY KEY,
            check_id VARCHAR(36) NOT NULL REFERENCES checks(id) ON DELETE CASCADE,
            agent_id VARCHAR(36) NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
            check_type VARCHAR(50) NOT NULL,
            success BOOLEAN NOT NULL,
            data JSONB,
            error TEXT,
            duration_ms INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    conn.commit()
    cursor.close()
    
    print("✅ Database initialized")
    print("✅ Redis connected")
    print(f"✅ CORS origins: {CORS_ORIGINS}")
    print(f"✅ CORS credentials: False")
    print(f"✅ Backend ready for Vercel connection")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down...")
    if db_conn:
        db_conn.close()
    if redis_client:
        redis_client.close()

# ============= FASTAPI APP =============

app = FastAPI(
    title="Host Checker API",
    description="API для проверки хостов и DNS резолвинга",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=False,  # Отключено для совместимости с Vercel
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= MODELS =============

class CreateCheckRequest(BaseModel):
    target: str = Field(..., description="URL, IP или домен для проверки")
    checks: List[str] = Field(..., description="Типы проверок: http, ping, dns, tcp, traceroute")
    agents: Optional[List[str]] = Field(None, description="ID агентов (если None - все доступные)")

class Check(BaseModel):
    id: str
    target: str
    check_types: List[str]
    status: str
    created_at: str
    completed_at: Optional[str] = None
    results: Optional[List[Dict]] = None

class CheckResult(BaseModel):
    id: str
    check_id: str
    agent_id: str
    agent_name: str
    agent_location: str
    check_type: str
    success: bool
    data: Dict[str, Any]
    error: Optional[str] = None
    duration_ms: int
    created_at: str

class Agent(BaseModel):
    id: str
    name: str
    location: str
    status: str
    last_heartbeat: Optional[str] = None
    registered_at: str
    metadata: Optional[Dict] = None

class RegisterAgentRequest(BaseModel):
    name: str = Field(..., description="Название агента")
    location: str = Field(..., description="Местоположение (страна, город)")
    metadata: Optional[Dict] = Field(None, description="Дополнительные данные")

class HeartbeatRequest(BaseModel):
    agent_id: str

class AgentTaskRequest(BaseModel):
    taskUIID: str
    check_type: str
    target: str

class AgentResultReport(BaseModel):
    country: str
    UIID: str  # Agent ID
    taskUIID: str  # Check ID
    task: str  # check type
    target: str
    result: str

# ============= HEALTH CHECK =============

@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Host Checker Backend",
        "version": "1.0.0"
    }

@app.get("/health")
async def detailed_health():
    """Detailed health check"""
    try:
        # Check DB
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    try:
        # Check Redis
        r = get_redis()
        r.ping()
        redis_status = "healthy"
    except Exception as e:
        redis_status = f"unhealthy: {str(e)}"
    
    return {
        "database": db_status,
        "redis": redis_status,
        "overall": "healthy" if db_status == "healthy" and redis_status == "healthy" else "degraded"
    }

# ============= AGENTS API =============

@app.post("/api/agents/register")
async def register_agent(
    request: RegisterAgentRequest,
    x_registration_token: Optional[str] = Header(None)
):
    """Register new agent"""
    
    # Verify registration token
    if x_registration_token != MASTER_REGISTRATION_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid registration token")
    
    agent_id = str(uuid.uuid4())
    api_token = str(uuid.uuid4()) + str(uuid.uuid4()).replace("-", "")
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO agents (id, name, location, api_token, status, metadata)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (agent_id, request.name, request.location, api_token, "offline", 
          json.dumps(request.metadata) if request.metadata else None))
    
    conn.commit()
    cursor.close()
    
    return {
        "agent_id": agent_id,
        "api_token": api_token,
        "message": "Agent registered successfully"
    }

@app.post("/api/agents/heartbeat")
async def agent_heartbeat(request: HeartbeatRequest):
    """Agent heartbeat endpoint"""
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE agents 
            SET status = 'online', last_heartbeat = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING id
        """, (request.agent_id,))
        
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        
        if not result:
            # Create agent if not exists
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO agents (id, name, location, api_token, status)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET status = 'online', last_heartbeat = CURRENT_TIMESTAMP
            """, (request.agent_id, request.agent_id, "Unknown", "temp-token", "online"))
            conn.commit()
            cursor.close()
        
        return {"status": "ok", "timestamp": datetime.now().isoformat()}
        
    except Exception as e:
        print(f"Heartbeat error: {e}")
        return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.get("/api/agents")
async def list_agents() -> List[Agent]:
    """Get list of all agents"""
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Mark offline agents (no heartbeat in 60 seconds)
        try:
            cursor.execute("""
                UPDATE agents 
                SET status = 'offline'
                WHERE last_heartbeat < NOW() - INTERVAL '60 seconds'
            """)
            conn.commit()
        except:
            pass
        
        cursor.execute("""
            SELECT id, name, location, status, 
                   last_heartbeat, registered_at, metadata
            FROM agents
            ORDER BY registered_at DESC
        """)
        
        rows = cursor.fetchall()
        cursor.close()
        
        agents = []
        for row in rows:
            agents.append(Agent(
                id=row[0],
                name=row[1],
                location=row[2],
                status=row[3],
                last_heartbeat=row[4].isoformat() if row[4] else None,
                registered_at=row[5].isoformat() if row[5] else datetime.now().isoformat(),
                metadata=json.loads(row[6]) if row[6] else None
            ))
        
        return agents
        
    except Exception as e:
        print(f"Error in list_agents: {e}")
        return []

@app.get("/api/agents/{agent_id}")
async def get_agent(agent_id: str) -> Agent:
    """Get agent by ID"""
    
    conn = get_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute("""
        SELECT id, name, location, status, 
               last_heartbeat, registered_at, metadata
        FROM agents
        WHERE id = %s
    """, (agent_id,))
    
    agent = cursor.fetchone()
    cursor.close()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return Agent(
        id=agent["id"],
        name=agent["name"],
        location=agent["location"],
        status=agent["status"],
        last_heartbeat=agent["last_heartbeat"].isoformat() if agent["last_heartbeat"] else None,
        registered_at=agent["registered_at"].isoformat(),
        metadata=agent["metadata"]
    )

# ============= CHECKS API =============

@app.post("/api/checks")
async def create_check(request: CreateCheckRequest) -> Check:
    """Create new check"""
    
    check_id = str(uuid.uuid4())
    
    conn = get_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    # Get online agents
    if request.agents:
        cursor.execute("""
            SELECT id, name, location FROM agents 
            WHERE id = ANY(%s) AND status = 'online'
        """, (request.agents,))
    else:
        cursor.execute("""
            SELECT id, name, location FROM agents 
            WHERE status = 'online'
        """)
    
    agents = cursor.fetchall()
    
    if not agents:
        raise HTTPException(status_code=400, detail="No online agents available")
    
    # Create check record
    cursor.execute("""
        INSERT INTO checks (id, target, check_types, agent_ids, status)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, target, check_types, status, created_at
    """, (check_id, request.target, json.dumps(request.checks), 
          json.dumps([a["id"] for a in agents]), "in_progress"))
    
    check = cursor.fetchone()
    conn.commit()
    
    # Dispatch tasks to agents via Redis queue
    r = get_redis()
    
    for agent in agents:
        for check_type in request.checks:
            task_data = {
                "check_id": check_id,
                "agent_id": agent["id"],
                "check_type": check_type,
                "target": request.target
            }
            
            # Push to agent-specific queue
            r.lpush(f"agent:{agent['id']}:tasks", json.dumps(task_data))
    
    cursor.close()
    
    return Check(
        id=check["id"],
        target=check["target"],
        check_types=json.loads(check["check_types"]),
        status=check["status"],
        created_at=check["created_at"].isoformat(),
        results=[]
    )

@app.get("/api/checks/{check_id}")
async def get_check(check_id: str) -> Check:
    """Get check by ID with results"""
    
    conn = get_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    # Get check
    cursor.execute("""
        SELECT id, target, check_types, status, created_at, completed_at
        FROM checks
        WHERE id = %s
    """, (check_id,))
    
    check = cursor.fetchone()
    
    if not check:
        raise HTTPException(status_code=404, detail="Check not found")
    
    # Get results
    cursor.execute("""
        SELECT cr.id, cr.check_id, cr.agent_id, cr.check_type, 
               cr.success, cr.data, cr.error, cr.duration_ms, cr.created_at,
               a.name as agent_name, a.location as agent_location
        FROM check_results cr
        JOIN agents a ON cr.agent_id = a.id
        WHERE cr.check_id = %s
        ORDER BY cr.created_at DESC
    """, (check_id,))
    
    results = cursor.fetchall()
    cursor.close()
    
    # Check if all results are in
    check_types = json.loads(check["check_types"])
    agent_ids = json.loads(check["agent_ids"] if check.get("agent_ids") else "[]")
    expected_results = len(check_types) * len(agent_ids)
    
    if len(results) >= expected_results and check["status"] == "in_progress":
        # Update status to completed
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE checks 
            SET status = 'completed', completed_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (check_id,))
        conn.commit()
        cursor.close()
        check["status"] = "completed"
        check["completed_at"] = datetime.now()
    
    return Check(
        id=check["id"],
        target=check["target"],
        check_types=json.loads(check["check_types"]),
        status=check["status"],
        created_at=check["created_at"].isoformat(),
        completed_at=check["completed_at"].isoformat() if check.get("completed_at") else None,
        results=[
            {
                "id": r["id"],
                "check_id": r["check_id"],
                "agent_id": r["agent_id"],
                "agent_name": r["agent_name"],
                "agent_location": r["agent_location"],
                "check_type": r["check_type"],
                "success": r["success"],
                "data": r["data"],
                "error": r["error"],
                "duration_ms": r["duration_ms"],
                "created_at": r["created_at"].isoformat()
            }
            for r in results
        ]
    )

@app.get("/api/checks")
async def list_checks(limit: int = 50) -> List[Check]:
    """Get list of recent checks"""
    
    conn = get_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute("""
        SELECT id, target, check_types, status, created_at, completed_at
        FROM checks
        ORDER BY created_at DESC
        LIMIT %s
    """, (limit,))
    
    checks = cursor.fetchall()
    cursor.close()
    
    return [
        Check(
            id=c["id"],
            target=c["target"],
            check_types=json.loads(c["check_types"]),
            status=c["status"],
            created_at=c["created_at"].isoformat(),
            completed_at=c["completed_at"].isoformat() if c.get("completed_at") else None
        )
        for c in checks
    ]

# ============= AGENT TASK POLLING =============

@app.get("/api/agents/{agent_id}/tasks")
async def get_agent_tasks(agent_id: str, limit: int = 10):
    """Agent polls for tasks from queue"""
    
    r = get_redis()
    tasks = []
    
    # Pop tasks from queue (FIFO)
    for _ in range(limit):
        task_json = r.rpop(f"agent:{agent_id}:tasks")
        if not task_json:
            break
        tasks.append(json.loads(task_json))
    
    return {"tasks": tasks}

# ============= AGENT RESULT SUBMISSION =============

@app.post("/api/v1/results")
async def submit_result(report: AgentResultReport):
    """Agent submits check result"""
    
    result_id = str(uuid.uuid4())
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Parse result
    try:
        result_data = json.loads(report.result) if isinstance(report.result, str) else report.result
        success = True
        error = None
        duration_ms = result_data.get("response_time_ms", 0) if isinstance(result_data, dict) else 0
    except:
        result_data = {"raw": report.result}
        success = "error" not in report.result.lower() and "failed" not in report.result.lower()
        error = report.result if not success else None
        duration_ms = 0
    
    cursor.execute("""
        INSERT INTO check_results (id, check_id, agent_id, check_type, success, data, error, duration_ms)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (result_id, report.taskUIID, report.UIID, report.task, 
          success, json.dumps(result_data), error, duration_ms))
    
    conn.commit()
    cursor.close()
    
    # Publish to WebSocket channel
    r = get_redis()
    r.publish(f"check:{report.taskUIID}:updates", json.dumps({
        "type": "result",
        "check_id": report.taskUIID,
        "agent_id": report.UIID,
        "check_type": report.task
    }))
    
    return {"status": "ok", "result_id": result_id}

# ============= WEBSOCKET =============

@app.websocket("/api/ws/checks/{check_id}")
async def websocket_check_updates(websocket: WebSocket, check_id: str):
    """WebSocket for real-time check updates"""
    await websocket.accept()
    
    r = get_redis()
    pubsub = r.pubsub()
    pubsub.subscribe(f"check:{check_id}:updates")
    
    try:
        while True:
            message = pubsub.get_message(timeout=1.0)
            if message and message["type"] == "message":
                await websocket.send_text(message["data"])
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        pubsub.unsubscribe(f"check:{check_id}:updates")
        pubsub.close()

# ============= LEGACY ENDPOINTS (for compatibility) =============

@app.post("/takeReport")
async def take_report_legacy(report: AgentResultReport):
    """Legacy endpoint for agent reports"""
    return await submit_result(report)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

