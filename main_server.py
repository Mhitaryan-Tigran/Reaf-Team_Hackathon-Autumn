from fastapi import FastAPI, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import uuid
import json
from pydantic import BaseModel
import requests
import os

app = FastAPI(title="Host Checker", version="1.0.0")
templates = Jinja2Templates(directory="templates")

# CORS для работы с фронтендом
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",") if os.getenv("CORS_ORIGINS") != "*" else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Глобальное подключение к БД
conn = None

@app.on_event("startup")
async def startDBConnection():
    global conn
    # БЕЗОПАСНОСТЬ: используйте DATABASE_URL из переменных окружения!
    database_url = os.getenv("DATABASE_URL")
    
    if database_url:
        # Production: используем DATABASE_URL от Railway
        conn = psycopg2.connect(database_url)
        print("✅ Connected to database via DATABASE_URL")
    else:
        # Development: локальные credentials
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "serverDB")
        db_user = os.getenv("DB_USER", "SERVER")
        db_password = os.getenv("DB_PASSWORD", "hakatonski123")
        
        conn = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        print("⚠️  Using local database credentials - set DATABASE_URL for production!")


@app.on_event("shutdown")
async def stopDBConnection():
    if conn:
        conn.close()
        print("🛑 Database connection closed")

# Static files (если есть директория static)
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception:
    print("⚠️  Static directory not found, skipping static files mount")


@app.get("/", response_class=HTMLResponse)
def IndexPage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/res")
def ResultPage(request: Request):
    return templates.TemplateResponse("result.html", {"request": request})


@app.get("/agent_status")
def AgentStatus(request: Request):
    return templates.TemplateResponse("agent_status.html", {"request": request})

# Api

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # логика: эхо обратно
            
            cursor = conn.cursor()
            cursor.execute("select * from reports where uiid=%s", (data,))
            rows = cursor.fetchall()
            cursor.close()

            await websocket.send_text(rows)
    except WebSocketDisconnect:
        # клиент отключился
        pass

class reportFromAgent(BaseModel):
    country: str
    UIID: str
    taskUIID: str
    result: str

class checkRequest(BaseModel):
    target: str
    task: str

@app.get("/getAgents")
async def getAgents():
    cursor = conn.cursor()
    cursor.execute("select * from agents;")
    rows = cursor.fetchall()
    print(rows)
    cursor.close()
    return rows

@app.post("/getTask")
async def getTask(request: Request):
    rawBody = await request.body()
    clearBody = rawBody.decode("utf-8")
    print(clearBody)
    cursor = conn.cursor()
    cursor.execute("select * from tasks where uiid=%s", (clearBody,))
    rows = cursor.fetchall()
    print(rows)
    cursor.close()
    return rows

@app.post("/getReport")
async def getReport(request: Request):
    rawBody = await request.body()
    clearBody = rawBody.decode("utf-8")
    print(clearBody)
    cursor = conn.cursor()
    cursor.execute("select * from reports where uiid=%s", (clearBody,))
    rows = cursor.fetchall()
    print(rows)
    cursor.close()
    return rows

@app.post("/takeReport")
def getReportFromAgent(report: reportFromAgent):
    # БЕЗОПАСНОСТЬ: ограничение размера данных
    if len(str(report.result)) > 100000:  # 100KB максимум
        return Response(status_code=413, content="Result data too large")
    
    cursor = conn.cursor()
    cursor.execute("SELECT EXISTS(SELECT 1 FROM Agents WHERE uiid = %s)", (report.UIID,))
    rows = cursor.fetchall()
    cursor.close()
    if rows[0][0]:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Reports (country, UIID, result) VALUES (%s, %s, %s);", (report.country, report.taskUIID, report.result))
        conn.commit()
        cursor.close()
        return Response(status_code=200)
    else:
        return Response(status_code=403)

@app.post("/start_check")
def startCheck(req: checkRequest):
    # БЕЗОПАСНОСТЬ: валидация входных данных
    if not req.target or len(req.target) > 500:
        return Response(status_code=400, content="Invalid target")
    
    # Проверка на опасные символы
    dangerous_chars = [';', '&', '|', '$', '`', '\n', '\r']
    if any(char in req.target for char in dangerous_chars):
        return Response(status_code=400, content="Invalid characters in target")
    
    taskUIID = uuid.uuid4()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Agents")
    rows = cursor.fetchall()
    ipAddrs = []
    for row in rows:
        ipAddrs.append(row[0])
        body = {
            "target": req.target,
            "task": req.task,
            "taskUUID": str(taskUIID)
        }
        try:
            requests.post(url=f"{row[0]}/check", data=json.dumps(body), timeout=5)
        except Exception as e:
            print(f"Error sending task to agent {row[0]}: {e}")
    
    print(ipAddrs, taskUIID)

    cursor.execute("INSERT INTO Tasks (UIID, target, task) VALUES (%s, %s, %s);", (str(taskUIID), req.target, req.task))
    conn.commit()
    cursor.close()

    return {"taskUIID": str(taskUIID)}

# Health check endpoint
@app.get("/health")
def health_check():
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
