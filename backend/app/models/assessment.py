from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal, List

class Question(BaseModel):
    """
    Represents a single question in the assessment.
    """
    type: Literal['reading', 'writing', 'listening', 'speaking'] = Field(..., description="The type of the question.")
    question: str = Field(..., description="The text of the question.")
    answer: Optional[str] = Field(None, description="The user's answer to the question.")
    content_type: Literal['text', 'audio'] = Field(..., description="The content type for the question.")
    text_content: Optional[str] = Field(None, description="The text content for the question (if applicable).")
    audio_content: Optional[str] = Field(None, description="The transcript of the audio content (if applicable).")
    audio_url: Optional[str] = Field(None, description="The URL of the audio content (if applicable).")

    @model_validator(mode="before")
    def check_content_fields(cls, values):
        content_type = values.get('content_type')
        text_content = values.get('text_content')
        audio_content = values.get('audio_content')
        audio_url = values.get('audio_url')

        if content_type == 'text' and not text_content:
            raise ValueError('text_content must be provided for text questions')
        if content_type == 'audio' and (not audio_content or not audio_url):
            raise ValueError('audio_content and audio_url must be provided for audio questions')

        return values

class Questionnaire(BaseModel):
    """
    Represents a list of questions as part of the assessment.
    """
    questions: List[Question] = Field(..., description="The list of questions in the questionnaire.")

