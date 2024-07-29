# models.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChatMessage(BaseModel):
    id: Optional[str] = None
    text: str
    timestamp: Optional[datetime] = None
