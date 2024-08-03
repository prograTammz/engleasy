# Packages
from fastapi import APIRouter, WebSocket, Depends
from typing import List, Dict
#Routing
from app.routers.auth import get_current_user
# Models
from app.models.chat import ChatMessage
from app.models.user import User
# Services

# Utilities

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    pass

@router.get("/messages", response_model=List[ChatMessage])
async def get_chat_history(current_user: User = Depends(get_current_user)):
    pass

@router.put("/messages/{message_id}", response_model=ChatMessage)
async def edit_message(message_id: str, text: str, current_user: User = Depends(get_current_user)):
    pass

@router.delete("/messages/{message_id}")
async def delete_message(message_id: str, current_user: User = Depends(get_current_user)):
    pass