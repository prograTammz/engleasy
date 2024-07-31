from pydantic import BaseModel, Field

class WritingScores(BaseModel):
    task_achievement: int = Field(..., ge=0, le=20)
    coherence_and_cohesion: int = Field(..., ge=0, le=20)
    lexical_resource: int = Field(..., ge=0, le=20)
    grammatical_range_and_accuracy: int = Field(..., ge=0, le=20)
    total: int = Field(..., ge=0, le=80)

class SpeakingScores(BaseModel):
    fluency_and_coherence: int = Field(..., ge=0, le=20)
    pronunciation: int = Field(..., ge=0, le=20)
    lexical_resource: int = Field(..., ge=0, le=20)
    grammatical_range_and_accuracy: int = Field(..., ge=0, le=20)
    total: int = Field(..., ge=0, le=80)