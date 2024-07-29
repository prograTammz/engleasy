# app/models.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class SenderType(str, Enum):
    user = "user"
    bot = "bot"

class ChatMessage(BaseModel):
    id: Optional[str] = None
    text: str
    timestamp: Optional[datetime] = None
    modified: Optional[datetime] = None
    sender: SenderType
