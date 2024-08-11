import pytest
from unittest.mock import patch, AsyncMock
from app.services.scores import save_score, get_all_scores, get_score_by_id, delete_score_by_id
from app.models.score import EnglishScoreSheet
from bson import ObjectId
from datetime import datetime, timezone

pytestmark = pytest.mark.asyncio

@pytest.fixture
def score_sheet():
    return EnglishScoreSheet(
        user_id="test_user_id",
        test_date=str(datetime.now(timezone.utc)),
        writing={
            "task_achievement": 10,
            "coherence_and_cohesion": 10,
            "lexical_resource": 10,
            "grammatical_range_and_accuracy": 10,
            "total": 40
        },
        speaking={
            "fluency_and_coherence": 10,
            "pronunciation": 10,
            "lexical_resource": 10,
            "grammatical_range_and_accuracy": 10,
            "total": 40
        },
        reading={
            "understanding_main_ideas": 10,
            "understanding_details": 10,
            "inference": 10,
            "lexical_resource": 10,
            "total": 40
        },
        listening={
            "understanding_main_ideas": 10,
            "understanding_details": 10,
            "inference": 10,
            "lexical_resource": 10,
            "total": 40
        },
        overall_score=160,
        cefr_level="B2"
    )

@patch("app.services.scores.scores_collection.insert_one", new_callable=AsyncMock)
async def test_save_score(mock_insert_one, score_sheet):
    # Simulate a successful insert operation
    mock_insert_one.return_value.acknowledged = True

    result = await save_score(score_sheet)

    assert result is True  # Ensure it returns True for a successful save

    # Simulate a failed insert operation
    mock_insert_one.return_value.acknowledged = False

    result = await save_score(score_sheet)

    assert result is False  # Ensure it returns False for a failed save

@patch("app.services.scores.scores_collection.find")
async def test_get_all_scores(mock_find, score_sheet):
    # Create an async mock for the cursor
    mock_cursor = AsyncMock()
    mock_cursor.__aiter__.return_value = [score_sheet.model_dump()]
    mock_find.return_value = mock_cursor

    result = await get_all_scores("test_user_id")

    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], EnglishScoreSheet)
    assert result[0].overall_score == 160


@patch("app.services.scores.scores_collection.find_one", new_callable=AsyncMock)
async def test_get_score_by_id(mock_find_one, score_sheet):
    mock_find_one.return_value = score_sheet.model_dump()

    result = await get_score_by_id(score_sheet.id)

    assert result is not None
    assert isinstance(result, EnglishScoreSheet)  # Ensure the result is an instance of EnglishScoreSheet
    assert result.overall_score == 160

@patch("app.services.scores.scores_collection.delete_one", new_callable=AsyncMock)
async def test_delete_score_by_id(mock_delete_one):
    mock_delete_one.return_value.deleted_count = 1
    result = await delete_score_by_id(str(ObjectId()))

    assert result == 1
