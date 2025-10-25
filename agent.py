from fastapi import FastAPI, Response, Request
from pydantic import BaseModel
import threading
import json
import asyncio
import time
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

agentUIID = os.getenv("agentUIID")
tasks = []
stopper = True

def tasker():
    while stopper:
        print("async worker tick")
        time.sleep(5)

@app.on_event("startup")
async def start_async_worker():
    backgroundTask = threading.Thread(target=tasker, daemon=True)
    backgroundTask.start()

@app.on_event("shutdown")
async def stop_async_worker():
    stopper = False

@app.get("/")
async def live():
    return Response(status_code=200)

@app.post("/check")
async def check(request: Request):
    rawBody = await request.body()
    body = rawBody.decode("utf-8")
    jsonAsObj = json.loads(body)
    # print(body)
    print(jsonAsObj)
    return Response(status_code=200)