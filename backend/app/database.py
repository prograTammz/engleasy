import motor.motor_asyncio
from bson.objectid import ObjectId
from datetime import datetime
import os

MONGO_URL = os.getenv("MONGO_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
database = client.chatbot

chat_collection = database.get_collection("chats")

async def add_chat(chat_data: dict) -> dict:
    chat_data["timestamp"] = datetime.utcnow()
    chat = await chat_collection.insert_one(chat_data)
    new_chat = await chat_collection.find_one({"_id": chat.inserted_id})
    return {
        "id": str(new_chat["_id"]),
        "text": new_chat["text"],
        "timestamp": new_chat["timestamp"]
    }