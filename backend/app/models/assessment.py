from pydantic import BaseModel
from typing import Optional, Literal, List

class Question(BaseModel):
    type: str
    question: str
    answer: Optional[str] = None
    content_type: Literal['text', 'audio']
    audio_content: Optional[str] = None
    audio_url: Optional[str] = None

class Questionnaire(BaseModel):
    tests: List[Question]