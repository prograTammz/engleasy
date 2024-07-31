import json
import random
from datetime import datetime,timezone
from uuid import uuid4
from typing import Optional

from app.utils.redis_client import redis_client
from app.models.chat import ChatHistory, ChatMessage
from app.services.assessment import generate_questionnaire

# Starts a new chat by generating a questionaire from chatGPT
def start_new_chat(user_id: str):
    questionnaire = generate_questionnaire()
    chat_history = ChatHistory(
        user_id=user_id,
        messages=[],
        current_question_index=0
    )
    redis_client.set(f"chat_{user_id}", chat_history.json_dumb())
    redis_client.set(f"questionnaire_{user_id}", json.dumps(questionnaire))
    return questionnaire

# ----------------------------
# History Service Definitions
# ----------------------------

# Checks the redis if the chat history exust then returns it after parsing it
def get_chat_history(user_id: str) -> Optional[ChatHistory]:
    chat_data = redis_client.get(f"chat_{user_id}")
    if chat_data:
        return ChatHistory.model_validate_json(chat_data)
    return None

# Saves the chathistory as a snapshot
def save_chat_history(chat_history: ChatHistory):
    redis_client.set(f"chat_{chat_history.user_id}", chat_history.model_dump_json())

# ----------------------------
# Messages Service Definitions
# ----------------------------

# Retrieves the history and creates a message then save it back to history
def add_message(user_id: str, text: str, sender: str = "user") -> str:
    chat_history = get_chat_history(user_id)
    if chat_history:
        message_id = uuid4()
        chat_history.messages.append(ChatMessage(
            id=message_id,
            text=text,
            created=datetime.now(timezone.utc),
            sender=sender
        ))
        save_chat_history(chat_history)
        return message_id
    return None

# Retrieves the chat history then searches for the message with it's id and edits it.
def edit_message(user_id: str, message_id: str, new_text: str) -> bool:
    chat_history = get_chat_history(user_id)
    if chat_history:
        for message in chat_history.messages:
            if message.id == message_id:
                message.text = new_text
                message.modified = datetime.now(timezone.utc)
                message.is_modified = True
                save_chat_history(chat_history)
                return True
    return False

# Retrieves the chat history and then remove the message from history by filtering it
# and save the snapshot.
def delete_message(user_id: str, message_id: str) -> bool:
    chat_history = get_chat_history(user_id)
    if chat_history:
        chat_history.messages = [msg for msg in chat_history.messages if msg.id != message_id]
        save_chat_history(chat_history)
        return True
    return False