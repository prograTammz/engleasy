from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal, List
from datetime import datetime, timezone
from uuid import uuid4

class ChatMessage(BaseModel):
    """
    Represents a single chat message in the chat history.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="The unique identifier for the chat message.")
    content: str = Field(..., description="The content of the message.")
    type: Literal['text', 'audio', 'sheet'] = Field(..., description="The type of the message content.")
    created: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc), description="The timestamp when the message was created.")
    modified: Optional[datetime] = Field(None, description="The timestamp when the message was last modified.")
    is_modified: Optional[bool] = Field(False, description="Flag indicating whether the message has been modified.")
    sender: Literal['user', 'bot'] = Field('bot', description="The sender of the message, either 'user' or 'bot'.")

    @model_validator(mode="before")
    def validate_fields(cls, values):
        # Ensure 'created' is set
        if 'created' not in values or values['created'] is None:
            values['created'] = datetime.now(timezone.utc)

        # Ensure 'modified' is set if 'is_modified' is True
        if values.get('is_modified') and not values.get('modified'):
            raise ValueError("'modified' must be set if 'is_modified' is True")

        return values

class ChatHistory(BaseModel):
    """
    Represents the chat history, containing a list of chat messages.
    """
    messages: List[ChatMessage] = Field(..., description="The list of messages in the chat history.")
