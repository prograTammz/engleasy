# app/models.py
from pydantic import BaseModel
from typing import (Optional)
from datetime import datetime


class ChatMessage(BaseModel):
    id: Optional[str] = None
    text: str
    created: Optional[datetime] = None
    modified: Optional[datetime] = None
    is_modified: Optional[bool] = False
    sender: str = "user"
