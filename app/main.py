from typing import Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient

from dotenv import load_dotenv
import os

load_dotenv()


app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    description: str = None

client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
db = client["test"]
collection = db["items"]


# Create an item
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    result = await collection.insert_one(item_dict)
    return "Item inserted!"

# Update an item
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    item_dict = item.dict()
    result = await collection.update_one({"id": item_id}, {"$set": item_dict})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, **item_dict}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    item = await collection.find_one({"id": item_id}, {"_id":0})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
