from fastapi import FastAPI, Response, Request
from pydantic import BaseModel
import json
import asyncio

app = FastAPI()

tasks = []

async def async_worker():
    while True:
        print("async worker tick")
        await asyncio.sleep(5)

@app.on_event("startup")
async def start_async_worker():
    app.state.worker_task = asyncio.create_task(async_worker())

@app.on_event("shutdown")
async def stop_async_worker():
    app.state.worker_task.cancel()
    try:
        await app.state.worker_task
    except asyncio.CancelledError:
        pass

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