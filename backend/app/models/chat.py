from pydantic import BaseModel
from typing import Optional, Literal, List
from datetime import datetime


class ChatMessage(BaseModel):
    id: Optional[str] = None
    content: str
    type: Literal['text', 'audio', 'sheet']
    created: Optional[datetime] = None
    modified: Optional[datetime] = None
    is_modified: Optional[bool] = False
    sender: Literal['user', 'bot'] = 'bot'

class ChatHistory(BaseModel):
    user_id: str
    messages: List[ChatMessage]