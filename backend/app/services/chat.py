import json
import random

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