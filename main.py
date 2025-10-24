from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"id": item_id, "name": f"item-{item_id}"}

@app.post("/items", status_code=201)
async def create_item(item: Item):
    return item
