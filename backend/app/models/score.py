from pydantic import BaseModel, Field, model_validator
from typing import Literal
from datetime import datetime, timezone
from uuid import uuid4

"""
The scores are based on the EnglishScore system by the British Council.
It provides a standardized way to measure English proficiency,
often used in conjunction with the CEFR level.
"""

class WritingScores(BaseModel):
    """
    Represents the writing assessment scores.

    Task Achievement/Response:
       - Measures how well the test taker addresses the task requirements.
    Coherence and Cohesion:
       - Assesses the organization of ideas and logical flow.
    Lexical Resource:
       - Evaluates the range and accuracy of vocabulary.
    Grammatical Range and Accuracy:
       - Looks at the use and accuracy of grammar.
    """
    task_achievement: int = Field(..., ge=0, le=20)
    coherence_and_cohesion: int = Field(..., ge=0, le=20)
    lexical_resource: int = Field(..., ge=0, le=20)
    grammatical_range_and_accuracy: int = Field(..., ge=0, le=20)
    total: int = Field(ge=0, le=80)

    @model_validator(mode="before")
    def calculate_total(cls, values):
        values['total'] = values['task_achievement'] + values['coherence_and_cohesion'] + values['lexical_resource'] + values['grammatical_range_and_accuracy']
        return values

class SpeakingScores(BaseModel):
    """
    Represents the speaking assessment scores.

    Fluency and Coherence:
       - Measures the smoothness and logical flow of speech.
    Pronunciation:
       - Evaluates clarity and accuracy of pronunciation.
       - **Evaluated Programmatically by comparison
    Lexical Resource:
       - Looks at the range and appropriateness of vocabulary used.
    Grammatical Range and Accuracy:
       - Assesses the use of grammar.
    """
    fluency_and_coherence: int = Field(..., ge=0, le=20)
    pronunciation: int = Field(..., ge=0, le=20)
    lexical_resource: int = Field(..., ge=0, le=20)
    grammatical_range_and_accuracy: int = Field(..., ge=0, le=20)
    total: int = Field(ge=0, le=80)

    @model_validator(mode="before")
    def calculate_total(cls, values):
        values['total'] = values['fluency_and_coherence'] + values['pronunciation'] + values['lexical_resource'] + values['grammatical_range_and_accuracy']
        return values

class ReadingScores(BaseModel):
    """
    Represents the reading assessment scores.

    Understanding Main Ideas:
       - Ability to grasp the main points of a text.
    Understanding Details:
       - Ability to comprehend specific details in the text.
    Inference:
       - Ability to make logical inferences based on the text.
    Lexical Resource:
       - Ability to understand and use vocabulary.
    """
    understanding_main_ideas: int = Field(..., ge=0, le=20)
    understanding_details: int = Field(..., ge=0, le=20)
    inference: int = Field(..., ge=0, le=20)
    lexical_resource: int = Field(..., ge=0, le=20)
    total: int = Field(ge=0, le=80)

    @model_validator(mode="before")
    def calculate_total(cls, values):
        values['total'] = values['understanding_main_ideas'] + values['understanding_details'] + values['inference'] + values['lexical_resource']
        return values

class ListeningScores(BaseModel):
    """
    Represents the listening assessment scores.

    Understanding Main Ideas:
       - Ability to grasp the main points of spoken content.
    Understanding Details:
       - Ability to comprehend specific details in the spoken content.
    Inference:
       - Ability to make logical inferences based on spoken content.
    Lexical Resource:
       - Ability to understand and use vocabulary.
    """
    understanding_main_ideas: int = Field(..., ge=0, le=20)
    understanding_details: int = Field(..., ge=0, le=20)
    inference: int = Field(..., ge=0, le=20)
    lexical_resource: int = Field(..., ge=0, le=20)
    total: int = Field(ge=0, le=80)

    @model_validator(mode="before")
    def calculate_total(cls, values):
        values['total'] = values['understanding_main_ideas'] + values['understanding_details'] + values['inference'] + values['lexical_resource']
        return values


class EnglishScoreSheet(BaseModel):
    """
    Represents the overall score sheet for an English assessment.
    """
    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique identifier for the scoresheet.")
    user_id: str = Field(...)
    test_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="The date and time when the test was taken.")
    writing: WritingScores = Field(...)
    speaking: SpeakingScores = Field(...)
    reading: ReadingScores = Field(...)
    listening: ListeningScores = Field(...)
    overall_score: int = Field(ge=0, le=320)
    cefr_level: Literal['A1', 'A2', 'B1', 'B2', 'C1', 'C2'] = Field(...)

    @model_validator(mode="before")
    def calculate_overall_score(cls, values):
        # Access the total directly from the dictionaries
        values['overall_score'] = values['writing']['total'] + values['speaking']['total'] + values['reading']['total'] + values['listening']['total']
        return values