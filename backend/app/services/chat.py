# Packages
from fastapi import WebSocket
from typing import Any, Literal, List, cast, MutableMapping
from uuid import uuid4
from datetime import datetime, timezone
# Models
from app.models.assessment import Questionnaire, Question
from app.models.chat import ChatMessage, ChatHistory
from app.models.score import EnglishScoreSheet
# Services
from app.services.scores import save_score
from app.services.assessment import generate_score_sheet, generate_questionnaire
# Utilities
from app.utils.redis_client import redis_client

class ChatService:
    # Takes the user_id after openning connection and authenticating
    # the user, it starts the assesment session
    def __init__(self, user_id: str, websocket: WebSocket = None):
        self.user_id = user_id
        self.websocket = websocket

    # Setups the ChatService MUST BE CALLED BEFORE DOING ANYTHING
    async def setup(self):
        await self.__start_assessment()

    def get_opening_message(self) -> List[ChatMessage]:
        next_question = self.__get_next_question()

        if not next_question:
            return [self.__create_message('The assessment is already over','bot')]

        chat_history = self.__get_chat_history()
        if not chat_history.messages:
            welcome_message = self.__create_message(
            """
                Let's start your English assessment it will be 4 questions only.

                The questions will be Listening, Speaking, Writting & Reading,
                Each response will be consider an answer,
                so be careful with your responses.

                You can answer with text or voice message.

                It's a must to answer with voice message in speaking,
                and preferrable in the reading & listening as well.

                Your answer for writting question must be text message!
            """, 'bot')
            question_one = self.__handle_question_response()
            return [welcome_message,*question_one]
        else:
            message = self.__create_message("Resuming the Assessment", 'bot')
            return [message, *self.__handle_question_response()]

    # Processes Every message user sends
    async def handle_message(self, msg:MutableMapping[str, Any]) -> List[ChatMessage]:
        next_question = self.__get_next_question()

        # If there are questions not answerred
        if next_question:
            msg_type = self.__check_message_type(msg)
            if msg_type == 'text':
                msg = self.__cast_message_text(msg)
                return self.__handle_text_message(msg)
            else:
                msg = self.__cast_message_blob(msg)
                return self.__handle_blob_message(msg)

        # If it's Done
        else:
            score_sheet = await self.__complete_assessment()
            bot_response = f"Assessment complete. Your score: {score_sheet.overall_score}, Your Level: {score_sheet.cefr_level}"

            return [self.__create_message(bot_response, 'bot'), self.__create_message(score_sheet.model_dump_json(), 'bot', 'sheet')]

    # Edits the message (Only User Message)
    # Since user messages are usually answers, it will search for releated
    # message to the question and modifies it.
    def edit_message(self, msg_id:str, msg_text:str) -> bool:
        message = self.__retrieve_message(msg_id)
        # Update message
        message.content = msg_text
        message.is_modified = True
        message.modified = datetime.now(timezone.utc)
        # Save new History
        self.__set_existing_message(msg_id, message)
        # Update Questionnaire
        self.__set_existing_answer(msg_text)


    # Deletes the message (Only User Message)
    # Since user messages are usually answers, it will search for releated
    # message to the question and deletes it, the question will be repeated.
    def delete_message(self, msg_id: str) -> bool:
        message = self.__retrieve_message(msg_id)
        # Deletes the message from History
        self.__set_existing_message(msg_id, None, True)
        # Emptys the existing answer in Questionnaire
        self.__set_existing_answer(message.content, None)


    # Saves the answer to questionnaire
    def __handle_text_message(self, msg: str) -> List[ChatMessage]:
        # Answer the current question
        self.__set_new_answer(msg)
        # Create User Message
        self.__create_message(msg, 'user')
        # Respond with New Question
        return self.__handle_question_response()

    # Will convert the audio to transcript to save answer as text while
    #  Scoring the prouncation with separate service
    def __handle_blob_message(self, msg: bytes) -> List[ChatMessage]:
        return [self.__create_message('Not ready yet', 'bot')]

    def __handle_question_response(self) -> List[ChatMessage]:
        next_question = self.__get_next_question()
        responses = []
        responses.append(self.__create_message(next_question.question, 'bot'))

        # Additional Response
        bot_response_2 = None
        if next_question.type == 'reading':
            bot_response_2 = next_question.text_content
        if next_question.type == 'listening':
            transcript = next_question.audio_content
            # TODO: Upload Audio to AWS
            # TODO: Generate Audio from transcript
            # TODO: Create an Audio bot message
        if bot_response_2:
            responses.append(self.__create_message(bot_response_2, 'bot', 'audio'))

        return responses


    # Comepletes the assessment by scoring and saving the score
    # and deleting the questionnaire & chat history
    async def __complete_assessment(self) -> EnglishScoreSheet:
        try:
            score_sheet = await generate_score_sheet(self.questionnaire, self.user_id)
            save_score(score_sheet)
            redis_client.delete(f"questionnaire_{self.user_id}")
            redis_client.delete(f"chat_history_{self.user_id}")
            return score_sheet
        except:
            return None

    # Retrieves the ChatHistory from redis if exit, it not it creates new one
    def __get_chat_history(self) -> ChatHistory:
        chat_data = redis_client.get(f"chat_history_{self.user_id}")
        chat_history = None
        if chat_data:
            chat_history = ChatHistory.model_validate_json(chat_data)
        else:
            chat_history = ChatHistory(
                messages=[]
            )
            self.__save_chat_history(chat_history)

        return chat_history

    #  Saves the chatHistory to Redis
    def __save_chat_history(self, chat_history: ChatHistory) -> bool:
        try:
            chat_data = chat_history.model_dump_json()
            redis_client.set(f"chat_history_{self.user_id}", chat_data)
            return True
        except:
            return False



    # Check the message type if it's text or blob to process the message
    # accordingly
    def __check_message_type(self, msg:MutableMapping[str, Any]) -> Literal['text', 'blob']:
        if msg['text'].startswith("data:audio/mp3;"):
            return 'blob'
        else:
            return 'text'

    # Casts the message to Bytes
    def __cast_message_blob(self, msg:MutableMapping[str, Any]) -> bytes:
        return cast(bytes, msg["bytes"])

    # Casts the message to text
    def __cast_message_text(self, msg:MutableMapping[str, Any]) -> str:
        return cast(str, msg['text'])


    # Starts assessment session either by creating a questionnaire through
    # ChatGPT or retrieving existing one from redis
    async def __start_assessment(self) -> bool:
        try:
            questionnaire = redis_client.get(f"questionnaire_{self.user_id}")
            if questionnaire:
                self.questionnaire = Questionnaire.model_validate_json(questionnaire)
            else:
                self.questionnaire = await generate_questionnaire()
                return self.__save_questionnaire()
        except:
            if self.websocket:
                await self.websocket.close()
            return False

    # Goes through all the questions of the questionnaire and return the
    # unanswered question for the user to answer
    def __get_next_question(self) -> Question:
        for question in self.questionnaire.questions:
            if question.answer is None:
                return question
        return None

    # Creates a ChatMessage Object & updates the history
    def __create_message(self, msg_text:str, sender: Literal['bot', 'user'], msg_type='text') -> ChatMessage:
        try:
            message = ChatMessage(
                created=datetime.now(timezone.utc),
                id=str(uuid4()),
                content=msg_text,
                sender=sender,
                type=msg_type
            )
            chat_history = self.__get_chat_history()
            chat_history.messages.append(message)
            self.__save_chat_history(chat_history)
            return message
        except:
            return None


    # Searches for a ChatMessage through the ChatHistory
    def __retrieve_message(self, msg_id: str) -> ChatMessage:
        messages = self.__get_chat_history().messages
        for msg in messages:
            if msg.id == msg_id:
                return msg
        return None

    def __set_existing_message(self, msg_id: str, new_msg: ChatMessage, delete: bool = False) -> bool:
        try:
            messages = self.__get_chat_history().messages
            for msg in messages:
                if msg.id == msg_id:
                    if delete:
                        del msg
                    else:
                        msg = new_msg
            return self.__save_chat_history()
        except:
            return False

    # Will search in questionnaire similar text in anser and replace it.
    def __set_existing_answer(self, msg_text: str, new_text: str) -> bool:
        for question in self.questionnaire.questions:
            if question.answer == msg_text:
                question.answer = new_text
                return self.__save_questionnaire()
        return False

    def __set_new_answer(self, answer: str) -> bool:
        for question in self.questionnaire.questions:
            if question.answer is None:
                question.answer = answer
                return self.__save_questionnaire()
        return False


    def __save_questionnaire(self) -> bool:
        try:
            questionnaire_data = self.questionnaire.model_dump_json()
            redis_client.set(f"questionnaire_{self.user_id}", questionnaire_data)
            return True
        except:
            return False

