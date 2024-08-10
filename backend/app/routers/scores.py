from fastapi import APIRouter, Depends, HTTPException, status
from app.routers.auth import get_current_user
from app.models.user import User
from app.services.scores import (
    get_all_scores,
    get_score_by_id,
    delete_score_by_id
)

router = APIRouter()

@router.get("/")
async def get_scores(current_user: User = Depends(get_current_user)) -> list:
    """
    Retrieves all English scores for the current user.

    Args:
        current_user (User): The current authenticated user.

    Returns:
        list: A list of scores associated with the user.
    """
    user_id = current_user.id
    scores = await get_all_scores(user_id)
    return scores

@router.get("/{score_id}")
async def get_score(score_id: str, current_user: User = Depends(get_current_user)) -> dict:
    """
    Retrieves a specific English score by its ID.

    Args:
        score_id (str): The ID of the score to retrieve.
        current_user (User): The current authenticated user.

    Returns:
        dict: The score data.

    Raises:
        HTTPException: If the score is not found.
    """
    score = await get_score_by_id(score_id)
    if not score:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Score not found")
    return score

@router.delete("/{score_id}")
async def delete_score(score_id: str, current_user: User = Depends(get_current_user)) -> dict:
    """
    Deletes a specific English score by its ID.

    Args:
        score_id (str): The ID of the score to delete.
        current_user (User): The current authenticated user.

    Returns:
        dict: A message confirming the deletion.

    Raises:
        HTTPException: If the score is not found.
    """
    result = await delete_score_by_id(score_id)
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Score not found")
    return {"message": "Score deleted successfully"}
