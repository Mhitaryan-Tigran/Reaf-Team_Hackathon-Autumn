from fastapi import FastAPI, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import psycopg2
import uuid
import json
from pydantic import BaseModel
import requests


# conn = ""
# cursor = conn.cursor()
# cursor.execute("SELECT * FROM my_table")
# rows = cursor.fetchall()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startDBConnection():
    global conn
    conn = psycopg2.connect(database="serverDB", user="SERVER", password="hakatonski123", host="localhost", port="5432")


@app.on_event("shutdown")
async def stopDBConnection():
    conn.close()


app.mount("/static", StaticFiles(directory="static"), name="static")


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

@app.post("/getReports")
async def getReports(request: Request):
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
    taskUIID = uuid.uuid4()
    cursor = conn.cursor()
    cursor.execute("SELECT ip FROM Agents")
    rows = cursor.fetchall()
    ipAddrs = []
    for row in rows:
        ipAddrs.append(row[0])
        body = {
            "target": req.target,
            "task": req.task,
            "taskUUID": str(taskUIID)
        }
        requests.post(url=f"{row[0]}/check", data=json.dumps(body))
    print(ipAddrs, taskUIID)

    cursor.execute("INSERT INTO Tasks (UIID, target, task) VALUES (%s, %s, %s);", (str(taskUIID), req.target, req.task))
    conn.commit()

    
