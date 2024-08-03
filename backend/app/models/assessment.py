from pydantic import BaseModel
from typing import Optional, Literal, List

class Question(BaseModel):
    type: Literal['reading', 'writing', 'listening', 'speaking']
    question: str
    answer: Optional[str] = None
    content_type: Literal['text', 'audio']
    text_content: Optional[str] = None
    audio_content: Optional[str] = None
    audio_url: Optional[str] = None

class Questionnaire(BaseModel):
    questions: List[Question]