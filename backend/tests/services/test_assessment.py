import pytest
from unittest.mock import patch, AsyncMock
from app.services.assessment import generate_questionnaire, generate_score_sheet
from app.models.assessment import Questionnaire, Question
from app.models.score import EnglishScoreSheet

pytestmark = pytest.mark.asyncio

@pytest.fixture
def sample_questionnaire():
    return Questionnaire(
        questions=[
            Question(
                type='reading',
                question="What is the main idea of the passage?",
                content_type='text',
                text_content="The passage content goes here..."
            ),
            Question(
                type='writing',
                question="Write an essay on climate change.",
                content_type='text'
            ),
            Question(
                type='listening',
                question="What did the speaker say about renewable energy?",
                content_type='audio',
                audio_content="Renewable energy is crucial for sustainable development.",
                audio_url="http://example.com/audio/renewable_energy.mp3"
            ),
            Question(
                type='speaking',
                question="Describe your favorite hobby.",
                content_type='text'
            )
        ]
    )

@patch("app.services.assessment.create_gpt_completion", new_callable=AsyncMock)
async def test_generate_questionnaire(mock_gpt_completion):
    mock_gpt_completion.return_value = """
    {
        "questions": [
            {
                "type": "reading",
                "question": "What is the main idea of the passage?",
                "content_type": "text",
                "text_content": "The passage content goes here..."
            },
            {
                "type": "writing",
                "question": "Write an essay on climate change.",
                "content_type": "text"
            },
            {
                "type": "listening",
                "question": "What did the speaker say about renewable energy?",
                "content_type": "audio",
                "audio_content": "Renewable energy is crucial for sustainable development.",
                "audio_url": "http://example.com/audio/renewable_energy.mp3"
            },
            {
                "type": "speaking",
                "question": "Describe your favorite hobby.",
                "content_type": "text"
            }
        ]
    }
    """
    result = await generate_questionnaire()
    assert isinstance(result, Questionnaire)
    assert len(result.questions) == 4

@patch("app.services.assessment.generate_score_sheet")
async def test_generate_score_sheet(mock_generate, sample_questionnaire):
    # Mock the function that introduces randomness
    mock_generate.return_value = EnglishScoreSheet(
        user_id="test_user_id",
        test_date="2024-08-10T10:00:00Z",
        writing={
            "task_achievement": 15,
            "coherence_and_cohesion": 15,
            "lexical_resource": 15,
            "grammatical_range_and_accuracy": 15,
            "total": 60
        },
        speaking={
            "fluency_and_coherence": 15,
            "pronunciation": 15,
            "lexical_resource": 15,
            "grammatical_range_and_accuracy": 15,
            "total": 60
        },
        reading={
            "understanding_main_ideas": 15,
            "understanding_details": 15,
            "inference": 15,
            "lexical_resource": 15,
            "total": 60
        },
        listening={
            "understanding_main_ideas": 15,
            "understanding_details": 15,
            "inference": 15,
            "lexical_resource": 15,
            "total": 60
        },
        overall_score=240,
        cefr_level="B2"
    )

    result = await generate_score_sheet(sample_questionnaire, "test_user_id")

    # Validate the structure
    assert isinstance(result, EnglishScoreSheet)

    # Check key properties
    assert result.user_id == "test_user_id"
    assert result.cefr_level in ["A1", "A2", "B1", "B2", "C1", "C2"]

    # Ensure scores are within the expected range
    assert 0 <= result.overall_score <= 320
    assert 0 <= result.writing["total"] <= 80
    assert 0 <= result.speaking["total"] <= 80
    assert 0 <= result.reading["total"] <= 80
    assert 0 <= result.listening["total"] <= 80
