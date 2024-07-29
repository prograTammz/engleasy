# main.py
from fastapi import FastAPI, HTTPException
from models import ChatMessage
from database import (
    add_chat,
    retrieve_chats
)
from datetime import datetime

app = FastAPI()

@app.get("/chats", response_model=list[ChatMessage])
async def get_chats():
    chats = await retrieve_chats()
    return chats

@app.post("/chats", response_model=ChatMessage)
async def create_chat(chat: ChatMessage):
    chat.timestamp = datetime.utcnow()
    new_chat = await add_chat(chat.dict())
    return new_chat


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
