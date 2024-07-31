from pydantic import BaseModel, Field

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