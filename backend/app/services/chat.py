# Packages
from fastapi import Message
from typing import Literal
# Models
# Services
from app.models.assessment import Questionnaire, Question
from app.models.chat import ChatMessage, ChatHistory
from app.models.score import EnglishScoreSheet
# Utilities
from app.utils import redis_client

class ChatService:
    # Takes the user_id after openning connection and authenticating
    # the user, it starts the assesment session
    async def __init__(self, user_id):
        self.user_id = user_id
        self.questionaire = await self.__start_assessment()
        self.chat_history = await self.get_chat_history()
        pass

    # Processes Every message user sends
    async def handle_message(self, msg: Message) -> ChatMessage:
        pass

    # Saves the answer to questionaire
    async def handle_text_message(self, msg: str) -> ChatMessage:
        pass

    # Will convert the audio to transcript to save answer as text while
    #  Scoring the prouncation with separate service
    async def handle_blob_message(self, msg: bytes) -> ChatMessage:
        pass

    # Comepletes the assessment by scoring and saving the score
    # and deleting the questionaire & chat history
    async def complete_assessment(self) -> EnglishScoreSheet:
        pass

    # Retrieves the ChatHistory from redis if exit, it not it creates new one
    def get_chat_history(self) -> ChatHistory:
        chat_data = redis_client.get(f"chat_{self.user_id}")
        if chat_data:
            return ChatHistory.model_validate_json(chat_data)
        else:
            self.chat_history = ChatHistory(
                user_id=self.user_id,
                messages=[]
            )
            self.save_chat_history()
        return None

    #  Saves the chatHistory to Redis
    def save_chat_history(self) -> ChatHistory:
        chat_data = self.chat_history.model_dump_json()
        redis_client.set(f"chat_{self.user_id}", chat_data)
        pass

    # Edits the message (Only User Message)
    # Since user messages are usually answers, it will search for releated
    # message to the question and modifies it.
    async def edit_message(self, msg_id:str) -> bool:
        pass

    # Deletes the message (Only User Message)
    # Since user messages are usually answers, it will search for releated
    # message to the question and deletes it, the question will be repeated.
    async def delete_message(self, msg_id: str) -> bool:
        pass

    # Check the message type if it's text or blob to process the message
    # accordingly
    async def __check_message_type(self, msg: Message) -> Literal['text', 'blob']:
        pass

    # Starts assessment session either by creating a questionnaire through
    # ChatGPT or retrieving existing one from redis
    async def __start_assessment(self) -> Questionnaire:
        pass

    # Goes through all the questions of the Questionaire and return the
    # unanswered question for the user to answer
    def __get_next_question(self) -> Question:
        pass

    # Creates a ChatMessage Object
    def __create_message(self, msg_text:str, sender: Literal['bot', 'user']) -> ChatMessage:
        pass

    # Searches for a ChatMessage through the ChatHistory
    def __retrieve_message(self, msg_id: str) -> ChatMessage:
        pass

    # Will search in questionaire similar text in anser and replace it.
    async def __set_existing_answer(self, msg_text: str) -> bool:
        pass
