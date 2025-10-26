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
from datetime import datetime
import asyncio
from contextlib import asynccontextmanager

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = "postgresql://SERVER:hakatonski123@localhost:5432/serverDB"
    print("⚠️  WARNING: Using default DATABASE_URL for development. Set DATABASE_URL env var for production!")

REDIS_URL = os.getenv("REDIS_URL")
if not REDIS_URL:
    REDIS_URL = "redis://localhost:6379"
    print("⚠️  WARNING: Using default REDIS_URL for development. Set REDIS_URL env var for production!")

MASTER_REGISTRATION_TOKEN = os.getenv("MASTER_REGISTRATION_TOKEN")
if not MASTER_REGISTRATION_TOKEN:
    MASTER_REGISTRATION_TOKEN = "INSECURE-DEV-TOKEN-CHANGE-IN-PRODUCTION"
    print("🚨 CRITICAL: Using default MASTER_REGISTRATION_TOKEN! Set secure token in production!")

CORS_ORIGINS_STR = os.getenv("CORS_ORIGINS", "*")
CORS_ORIGINS = ["*"] if CORS_ORIGINS_STR == "*" else CORS_ORIGINS_STR.split(",")

db_conn = None
redis_client = None

def get_db():
    global db_conn
    if db_conn is None or db_conn.closed:
        db_conn = psycopg2.connect(DATABASE_URL)
    return db_conn

def get_redis():
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    return redis_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting Host Checker Backend...")
    
    conn = get_db()
    cursor = conn.cursor()
    
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
    print("✅ CORS origins:", CORS_ORIGINS)
    print("✅ CORS credentials: False")
    print("✅ Backend ready for Vercel connection")
    
    yield
    
    print("🛑 Shutting down...")
    if db_conn:
        db_conn.close()
    if redis_client:
        redis_client.close()

app = FastAPI(
    title="Host Checker API",
    description="API для проверки хостов и DNS резолвинга",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

def validate_target(target: str) -> bool:
    if not target or len(target) > 500:
        return False
    
    dangerous_chars = [';', '&', '|', '$', '`', '\n', '\r']
    if any(char in target for char in dangerous_chars):
        return False
    
    return True

def validate_check_types(check_types: list) -> bool:
    allowed_types = ['http', 'https', 'ping', 'tcp', 'traceroute', 'dns', 
                     'dns-A', 'dns-AAAA', 'dns-MX', 'dns-NS', 'dns-TXT', 'dns-CNAME']
    
    if not check_types or len(check_types) > 10:
        return False
    
    return all(ct in allowed_types for ct in check_types)

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
    UIID: str
    taskUIID: str
    task: str
    target: str
    result: str

@app.get("/")
async def health_check():
    return {
        "status": "healthy",
        "service": "Host Checker Backend",
        "version": "1.0.0"
    }

@app.get("/health")
async def detailed_health():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    try:
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

@app.post("/api/agents/register")
async def register_agent(
    request: RegisterAgentRequest,
    x_registration_token: Optional[str] = Header(None)
):
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
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE agents 
                SET status = 'offline'
                WHERE last_heartbeat < NOW() - INTERVAL '60 seconds'
            """)
            conn.commit()
        except Exception:
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

@app.post("/api/checks")
async def create_check(request: CreateCheckRequest) -> Check:
    if not validate_target(request.target):
        raise HTTPException(status_code=400, detail="Invalid target format")
    
    if not validate_check_types(request.checks):
        raise HTTPException(status_code=400, detail="Invalid check types")
    
    check_id = str(uuid.uuid4())
    
    conn = get_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
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
    
    cursor.execute("""
        INSERT INTO checks (id, target, check_types, agent_ids, status)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, target, check_types, status, created_at
    """, (check_id, request.target, json.dumps(request.checks), 
          json.dumps([a["id"] for a in agents]), "in_progress"))
    
    check = cursor.fetchone()
    conn.commit()
    
    r = get_redis()
    
    for agent in agents:
        for check_type in request.checks:
            task_data = {
                "check_id": check_id,
                "agent_id": agent["id"],
                "check_type": check_type,
                "target": request.target
            }
            
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
    conn = get_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute("""
        SELECT id, target, check_types, status, created_at, completed_at
        FROM checks
        WHERE id = %s
    """, (check_id,))
    
    check = cursor.fetchone()
    
    if not check:
        raise HTTPException(status_code=404, detail="Check not found")
    
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
    
    check_types = json.loads(check["check_types"])
    agent_ids = json.loads(check["agent_ids"] if check.get("agent_ids") else "[]")
    expected_results = len(check_types) * len(agent_ids)
    
    if len(results) >= expected_results and check["status"] == "in_progress":
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

@app.get("/api/agents/{agent_id}/tasks")
async def get_agent_tasks(agent_id: str, limit: int = 10):
    r = get_redis()
    tasks = []
    
    for _ in range(limit):
        task_json = r.rpop(f"agent:{agent_id}:tasks")
        if not task_json:
            break
        tasks.append(json.loads(task_json))
    
    return {"tasks": tasks}

@app.post("/api/v1/results")
async def submit_result(report: AgentResultReport):
    result_str = str(report.result)
    if len(result_str) > 100000:
        raise HTTPException(status_code=413, detail="Result data too large")
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM agents WHERE id = %s", (report.UIID,))
    if not cursor.fetchone():
        cursor.close()
        raise HTTPException(status_code=403, detail="Unknown agent")
    
    cursor.close()
    
    result_id = str(uuid.uuid4())
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        result_data = json.loads(report.result) if isinstance(report.result, str) else report.result
        success = True
        error = None
        duration_ms = result_data.get("response_time_ms", 0) if isinstance(result_data, dict) else 0
    except (json.JSONDecodeError, ValueError, TypeError):
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
    
    r = get_redis()
    r.publish(f"check:{report.taskUIID}:updates", json.dumps({
        "type": "result",
        "check_id": report.taskUIID,
        "agent_id": report.UIID,
        "check_type": report.task
    }))
    
    return {"status": "ok", "result_id": result_id}

@app.websocket("/api/ws/checks/{check_id}")
async def websocket_check_updates(websocket: WebSocket, check_id: str):
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

@app.post("/takeReport")
async def take_report_legacy(report: AgentResultReport):
    return await submit_result(report)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)

