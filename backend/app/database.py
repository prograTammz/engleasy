import motor.motor_asyncio
from bson.objectid import ObjectId
from datetime import datetime
import os

MONGO_URL = os.getenv("MONGO_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
database = client.chatbot

chat_collection = database.get_collection("chats")

def chat_helper(chat) -> dict:
    return {
        "id": str(chat["_id"]),
        "text": chat["text"],
        "timestamp": chat["timestamp"]
    }

async def retrieve_chats():
    chats = []
    async for chat in chat_collection.find():
        chats.append(chat_helper(chat))
    return chats

async def add_chat(chat_data: dict) -> dict:
    chat_data["timestamp"] = datetime.utcnow()
    chat = await chat_collection.insert_one(chat_data)
    new_chat = await chat_collection.find_one({"_id": chat.inserted_id})
    return chat_helper(new_chat)

async def retrieve_chat(id: str) -> dict:
    chat = await chat_collection.find_one({"_id": ObjectId(id)})
    if chat:
        return chat_helper(chat)