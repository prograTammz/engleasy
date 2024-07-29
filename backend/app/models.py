# app/models.py
from pydantic import BaseModel
from typing import (Optional, List)
from datetime import datetime


class ChatMessage(BaseModel):
    id: Optional[str] = None
    text: str
    created: Optional[datetime] = None
    modified: Optional[datetime] = None
    sender: str = "user"

class ChatResponse(BaseModel):
    chats: List[ChatMessage]
