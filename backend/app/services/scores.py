from app.models.score import EnglishScoreSheet
from bson import ObjectId
from app.utils.mongo_client import scores_collection
from typing import List

# Saves EnglishScoreSheet to database
async def save_score(score_sheet: EnglishScoreSheet) -> bool:
    """
    Saves an EnglishScoreSheet to the database.

    Args:
        score_sheet (EnglishScoreSheet): The score sheet to save.

    Returns:
        str: The ID of the inserted document.

    Raises:
        Exception: If the insertion fails.
    """
    try:
        result = await scores_collection.insert_one(score_sheet.model_dump())
        return result.acknowledged
    except Exception as e:
        raise Exception(f"Failed to save score: {str(e)}")

# Retrieves all the EnglishScores of the user
async def get_all_scores(user_id: str) -> List[EnglishScoreSheet]:
    """
    Retrieves all English scores for a given user.

    Args:
        user_id (str): The ID of the user whose scores to retrieve.

    Returns:
        List[dict]: A list of score sheets.
    """
    try:
        score_sheets = []
        async for score_sheet in scores_collection.find({"user_id": user_id}):
            score_sheets.append(EnglishScoreSheet.model_validate(score_sheet))
        return score_sheets
    except Exception as e:
        raise Exception(f"Failed to retrieve all scores: {str(e)}")

# Retrieves single EnglishScore by ID
async def get_score_by_id(score_id: str) -> EnglishScoreSheet:
    """
    Retrieves a single English score by its ID.

    Args:
        score_id (str): The ID of the score to retrieve.

    Returns:
        Optional[dict]: The score sheet if found, None otherwise.
    """
    try:
        score_sheet = await scores_collection.find_one({"id": score_id})
        if score_sheet:
            return EnglishScoreSheet.model_validate(score_sheet)
        return None
    except Exception as e:
        raise Exception(f"Failed to retrieve score by ID: {str(e)}")

# Deletes single EnglishScore by ID
async def delete_score_by_id(score_id: str) -> bool:
    """
    Deletes a single English score by its ID.

    Args:
        score_id (str): The ID of the score to delete.

    Returns:
        bool: True if the deletion was successful, False otherwise.
    """
    try:
        result = await scores_collection.delete_one({"_id": ObjectId(score_id)})
        return result.deleted_count > 0
    except Exception as e:
        raise Exception(f"Failed to delete score by ID: {str(e)}")
