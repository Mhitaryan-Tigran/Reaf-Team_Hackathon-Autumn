from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import psycopg2

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
@app.post("/takeStatus")
def getReportFromAgent():
    pass