from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


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

@app.post("/takeStatus")
def getOtschetFromAgent():
    pass