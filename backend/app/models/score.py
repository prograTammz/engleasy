from pydantic import BaseModel, Field
from typing import Literal

"""
The scores are based on EnglishScore system by the British Council
provides a standardized way to measure English proficiency,
often used in conjunction with the CEFR level.
"""
class WritingScores(BaseModel):
    """
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
    total: int = Field(..., ge=0, le=80)

class SpeakingScores(BaseModel):
    """
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
    total: int = Field(..., ge=0, le=80)

class ReadingScores(BaseModel):
    """
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
    total: int = Field(..., ge=0, le=80)

class ListeningScores(BaseModel):
    """
        TODO: Add the Listening Criteria
    """
    understanding_main_ideas: int = Field(..., ge=0, le=20)
    understanding_details: int = Field(..., ge=0, le=20)
    inference: int = Field(..., ge=0, le=20)
    lexical_resource: int = Field(..., ge=0, le=20)
    total: int = Field(..., ge=0, le=80)

"""
    ScoreSheet after assessing it, should be presenting by graph
"""
class EnglishScoreSheet(BaseModel):
    user_id: str = Field(...)
    test_date: str = Field(...)
    writing: WritingScores = Field(...)
    speaking: SpeakingScores = Field(...)
    reading: ReadingScores = Field(...)
    listening: ListeningScores = Field(...)
    overall_score: int = Field(..., ge=0, le=320)
    cefr_level: Literal['A1', 'A2', 'B1', 'B2', 'C1', 'C2'] = Field(...)