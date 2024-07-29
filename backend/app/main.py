# main.py
from fastapi import FastAPI, HTTPException
from models import ChatMessage
from database import (
    add_chat,
    retrieve_chats,
    retrieve_chat,
    update_chat
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

@app.get("/chats/{id}", response_model=ChatMessage)
async def get_chat(id: str):
    chat = await retrieve_chat(id)
    if chat:
        return chat
    raise HTTPException(status_code=404, detail=f"Chat with ID {id} not found")

@app.put("/chats/{id}")
async def update_chat_data(id: str, chat: ChatMessage):
    chat_data = chat.dict(exclude_unset=True)
    chat_data["timestamp"] = datetime.utcnow()
    updated = await update_chat(id, chat_data)
    if updated:
        return f"Chat with ID {id} updated successfully"
    raise HTTPException(status_code=404, detail=f"Chat with ID {id} not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
