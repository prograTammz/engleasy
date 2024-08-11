# Packages
from fastapi import WebSocket
from typing import Any, Literal, List, MutableMapping
from uuid import uuid4
from datetime import datetime, timezone
import asyncio
import logging

# Models
from app.models.assessment import Questionnaire, Question
from app.models.chat import ChatMessage, ChatHistory
from app.models.score import EnglishScoreSheet

# Services
from app.services.scores import save_score
from app.services.assessment import generate_score_sheet, generate_questionnaire
from app.services.openai import text_to_speech, speech_to_text

# Utilities
from app.utils.redis_client import redis_client
from app.utils.bucket_storage import upload_audio_s3
from app.utils.openai import base64_to_bytesio

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ChatService:
    # Takes the user_id after opening connection and authenticating
    # the user, it starts the assessment session
    def __init__(self, user_id: str, websocket: WebSocket = None):
        self.user_id = user_id
        self.websocket = websocket

    # Sets up the ChatService MUST BE CALLED BEFORE DOING ANYTHING
    async def setup(self):
        await self.__start_assessment()

    async def get_opening_message(self) -> List[ChatMessage]:
        next_question = self.__get_next_question()
        chat_history = self.get_chat_history()

        if not next_question:
            await self.__handle_final_question()

        if not chat_history.messages:
            welcome_message = self.__create_message(
                """
                Let's start your English assessment. It will be 4 questions only.

                The questions will be Listening, Speaking, Writing & Reading.
                Each response will be considered an answer,
                so be careful with your responses.

                You can answer with text or voice message.

                It's a must to answer with a voice message in speaking,
                and preferable in the reading & listening as well.

                Your answer for the writing question must be a text message!
                """, 'bot'
            )
            question_one = await self.__handle_question_response()
            return [welcome_message, *question_one]

        return []

    # Processes Every message user sends
    async def handle_message(self, msg: MutableMapping[str, Any]) -> List[ChatMessage]:
        next_question = self.__get_next_question()
        chat_history = self.get_chat_history()

        if not chat_history:
            return []
        # If there are questions not answered
        if next_question:
            msg_type = self.__check_message_type(msg)
            if msg_type == 'text':
                return await self.__handle_text_message(msg)
            else:
                return await self.__handle_blob_message(msg)

        return [self.__create_message(msg_type, 'bot')]

    # Retrieves the ChatHistory from redis if it exists, if not it creates a new one
    def get_chat_history(self) -> ChatHistory:
        try:
            chat_data = redis_client.get(f"chat_history_{self.user_id}")
            if chat_data:
                chat_history = ChatHistory.model_validate_json(chat_data)
            else:
                chat_history = ChatHistory(messages=[])
                self.__save_chat_history(chat_history)

            return chat_history
        except Exception as e:
            logger.error(f"Failed to retrieve chat history: {str(e)}")
            return ChatHistory(messages=[])

    # Edits the message (Only User Message)
    # Since user messages are usually answers, it will search for related
    # message to the question and modifies it.
    def edit_message(self, msg_id: str, new_text: str) -> ChatMessage:
        try:
            message = self.__retrieve_message(msg_id)
            if not message:
                return False
            # Update message
            old_text = message.content
            message.content = new_text
            message.is_modified = True
            message.modified = datetime.now(timezone.utc)
            # Save new History
            self.__set_existing_message(msg_id, message)
            # Update Questionnaire
            self.__set_existing_answer(old_text, new_text)
            return message
        except Exception as e:
            logger.error(f"Failed to edit message: {str(e)}")
            return False

    # Deletes the message (Only User Message)
    # Since user messages are usually answers, it will search for related
    # message to the question and deletes it, the question will be repeated.
    def delete_message(self, msg_id: str) -> bool:
        try:
            message = self.__retrieve_message(msg_id)
            if not message:
                return False
            # Deletes the message from History
            self.__set_existing_message(msg_id, None, True)
            # Empties the existing answer in Questionnaire
            self.__set_existing_answer(message.content, None)
            return True
        except Exception as e:
            logger.error(f"Failed to delete message: {str(e)}")
            return False

    # Saves the answer to questionnaire
    async def __handle_text_message(self, msg: str) -> List[ChatMessage]:
        try:
            # Answer the current question
            self.__set_new_answer(msg)
            # Create User Message
            user_message = self.__create_message(msg, 'user')
            # Respond with New Question
            responses = await self.__handle_question_response()
            return [user_message, *responses]
        except Exception as e:
            logger.error(f"Failed to handle text message: {str(e)}")
            return []

    # Will convert the audio to transcript to save the answer as text while
    # Scoring the pronunciation with a separate service
    async def __handle_blob_message(self, msg: str) -> List[ChatMessage]:
        try:
            audio_bytes = base64_to_bytesio(msg)
            transcript = await speech_to_text(audio_bytes)
            file_url = await upload_audio_s3(audio_bytes)
            # Answer the current question
            self.__set_new_answer(transcript)
            # Create User Message
            user_message = self.__create_message(file_url, 'user', 'audio')
            # Respond with New Question
            responses = await self.__handle_question_response()
            return [user_message, *responses]
        except Exception as e:
            logger.error(f"Failed to handle blob message: {str(e)}")
            return []

    # Returns a message with the next question and adds extra content if needed
    # whether if it's text or audio
    async def __handle_question_response(self) -> List[ChatMessage]:
        try:
            next_question = self.__get_next_question()

            if not next_question:
                return await self.__handle_final_question()

            responses = [self.__create_message(next_question.question, 'bot')]

            # Additional Response
            bot_response_2 = None
            if next_question.type == 'reading':
                bot_response_2 = next_question.text_content
                responses.append(self.__create_message(bot_response_2, 'bot', 'text'))
            elif next_question.type == 'listening':
                transcript = next_question.audio_content
                audio_data = await text_to_speech(transcript)
                bot_response_2 = await upload_audio_s3(audio_data)
                responses.append(self.__create_message(bot_response_2, 'bot', 'audio'))

            return responses
        except Exception as e:
            logger.error(f"Failed to handle question response: {str(e)}")
            return []

    # Handles the case when the questions are answered and clears the redis keys
    async def __handle_final_question(self) -> List[ChatMessage]:
        try:
            score_sheet = await self.__complete_assessment()
            bot_response = self.__create_message(
                f"Assessment complete. Your score: {score_sheet.overall_score}, Your Level: {score_sheet.cefr_level}",
                'bot'
            )
            score_response = self.__create_message(score_sheet.model_dump_json(), 'bot', 'sheet')

            # Schedule Redis deletions asynchronously
            asyncio.create_task(self.__delete_redis_keys())

            return [bot_response, score_response]
        except Exception as e:
            logger.error(f"Failed to handle final question: {str(e)}")
            return []

    # Completes the assessment by scoring and saving the score
    async def __complete_assessment(self) -> EnglishScoreSheet:
        try:
            score_sheet = await generate_score_sheet(self.questionnaire, self.user_id)
            await save_score(score_sheet)
            return score_sheet
        except Exception as e:
            logger.error(f"Failed to complete assessment: {str(e)}")
            return None

    # Saves the chatHistory to Redis
    def __save_chat_history(self, chat_history: ChatHistory) -> bool:
        try:
            chat_data = chat_history.model_dump_json()
            redis_client.set(f"chat_history_{self.user_id}", chat_data)
            return True
        except Exception as e:
            logger.error(f"Failed to save chat history: {str(e)}")
            return False

    # Check the message type if it's text or blob to process the message accordingly
    def __check_message_type(self, msg: MutableMapping[str, Any]) -> Literal['text', 'blob']:
        if msg.startswith('"data:audio/mp3;base64'):
            return 'blob'
        else:
            return 'text'

    # Starts assessment session either by creating a questionnaire through
    # ChatGPT or retrieving an existing one from redis
    async def __start_assessment(self) -> bool:
        try:
            questionnaire = redis_client.get(f"questionnaire_{self.user_id}")
            if questionnaire:
                self.questionnaire = Questionnaire.model_validate_json(questionnaire)
            else:
                self.questionnaire = await generate_questionnaire()
                return self.__save_questionnaire()
        except Exception as e:
            logger.error(f"Failed to start assessment: {str(e)}")
            if self.websocket:
                await self.websocket.close()
            return False

    # Goes through all the questions of the questionnaire and returns the
    # unanswered question for the user to answer
    def __get_next_question(self) -> Question:
        try:
            for question in self.questionnaire.questions:
                if question.answer is None:
                    return question
            return None
        except Exception as e:
            logger.error(f"Failed to get next question: {str(e)}")
            return None

    # Creates a ChatMessage Object & updates the history
    def __create_message(self, msg_text: str, sender: Literal['bot', 'user'], msg_type='text') -> ChatMessage:
        try:
            message = ChatMessage(
                created=datetime.now(timezone.utc),
                id=str(uuid4()),
                content=msg_text,
                sender=sender,
                type=msg_type
            )
            chat_history = self.get_chat_history()
            chat_history.messages.append(message)
            self.__save_chat_history(chat_history)
            return message
        except Exception as e:
            logger.error(f"Failed to create message: {str(e)}")
            return None

    # Searches for a ChatMessage through the ChatHistory
    def __retrieve_message(self, msg_id: str) -> ChatMessage:
        try:
            messages = self.get_chat_history().messages
            for msg in messages:
                if msg.id == msg_id:
                    return msg
            return None
        except Exception as e:
            logger.error(f"Failed to retrieve message: {str(e)}")
            return None

    # Edits or deletes an existing message used by PUT & DELETE
    def __set_existing_message(self, msg_id: str, new_msg: ChatMessage, delete: bool = False) -> bool:
        try:
            messages = self.get_chat_history().messages
            for i, msg in enumerate(messages):
                if msg.id == msg_id:
                    if delete:
                        del messages[i]
                    else:
                        messages[i] = new_msg
            return self.__save_chat_history(ChatHistory(messages=messages))
        except Exception as e:
            logger.error(f"Failed to set existing message: {str(e)}")
            return False

    # Will search in the questionnaire for similar text in answer and replace it
    def __set_existing_answer(self, msg_text: str, new_text: str) -> bool:
        try:
            for question in self.questionnaire.questions:
                if question.answer == msg_text:
                    question.answer = new_text
                    return self.__save_questionnaire()
            return False
        except Exception as e:
            logger.error(f"Failed to set existing answer: {str(e)}")
            return False

    # Loops over questions and sets the answer to the first unanswered one
    def __set_new_answer(self, answer: str) -> bool:
        try:
            for question in self.questionnaire.questions:
                if question.answer is None:
                    question.answer = answer
                    return self.__save_questionnaire()
            return False
        except Exception as e:
            logger.error(f"Failed to set new answer: {str(e)}")
            return False

    # Saves the questionnaire to Redis after turning it to JSON
    def __save_questionnaire(self) -> bool:
        try:
            questionnaire_data = self.questionnaire.model_dump_json()
            redis_client.set(f"questionnaire_{self.user_id}", questionnaire_data)
            return True
        except Exception as e:
            logger.error(f"Failed to save questionnaire: {str(e)}")
            return False

    # Deletes the Redis keys for Questionnaire & Chat History
    async def __delete_redis_keys(self):
        try:
            redis_client.delete(f"questionnaire_{self.user_id}")
            redis_client.delete(f"chat_history_{self.user_id}")
        except Exception as e:
            logger.error(f"Failed to delete Redis keys: {str(e)}")
