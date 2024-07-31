# app/database.py
import motor.motor_asyncio
from bson.objectid import ObjectId
from datetime import datetime,timezone
import os
MONGO_URL = os.getenv("MONGO_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
database = client.chatbot

chat_collection = database.get_collection("chats")

def chat_helper(chat) -> dict:
    return {
        "id": str(chat["_id"]),
        "text": chat["text"],
        "created": chat.get("created"),
        "modified": chat.get("modified"),
        "sender": chat.get("sender")
    }

# CRUD operations
async def retrieve_chats():
    chats = []
    async for chat in chat_collection.find():
        chats.append(chat_helper(chat))
    return chats

async def add_chat(chat_data: dict) -> dict:
    chat_data["created"] = datetime.now(timezone.utc)
    chat_data["modified"] = datetime.now(timezone.utc)
    chat = await chat_collection.insert_one(chat_data)
    new_chat = await chat_collection.find_one({"_id": chat.inserted_id})
    return chat_helper(new_chat)

async def retrieve_chat(id: str) -> dict:
    chat = await chat_collection.find_one({"_id": ObjectId(id)})
    if chat:
        return chat_helper(chat)

async def update_chat(id: str, data: dict):
    if len(data) < 1:
        return False
    chat = await chat_collection.find_one({"_id": ObjectId(id)})
    if chat:
        data["modified"] = datetime.now(timezone.utc)
        updated_chat = await chat_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_chat:
            return True
    return False

async def delete_chat(id: str):
    chat = await chat_collection.find_one({"_id": ObjectId(id)})
    if chat:
        await chat_collection.delete_one({"_id": ObjectId(id)})
        return True
