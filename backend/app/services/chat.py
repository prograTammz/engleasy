import json
import random
from typing import Optional

from app.utils.redis_client import redis_client
from app.models.chat import ChatHistory
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

# Checks the redis if the chat history exust then returns it after parsing it
def get_chat_history(user_id: str) -> Optional[ChatHistory]:
    chat_data = redis_client.get(f"chat_{user_id}")
    if chat_data:
        return ChatHistory.model_validate_json(chat_data)
    return None

# Saves the chathistory as a snapshot
def save_chat_history(chat_history: ChatHistory):
    redis_client.set(f"chat_{chat_history.user_id}", chat_history.model_dump_json())