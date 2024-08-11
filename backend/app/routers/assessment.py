from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
# Routers
from app.routers.auth import get_current_user
# Modles
from app.models.user import User
from app.models.assessment import Questionnaire
# Services
from app.services.assessment import generate_questionnaire, generate_score_sheet
from app.services.scores import save_score
# Utilies
from app.utils.mongo_client import users_collection
from app.utils.redis_client import redis_client

router = APIRouter()

@router.get("/questionnaire", response_model=Questionnaire)
async def get_questionnaire(current_user: User = Depends(get_current_user)) -> Questionnaire:
    """
    Retrieves the current user's questionnaire. Generates a new one if not found in Redis.

    Args:
        current_user (User): The current authenticated user.

    Returns:
        Questionnaire: The questionnaire for the user.

    Raises:
        HTTPException: If the questionnaire could not be generated or retrieved.
    """
    try:
        user_id = current_user.id
        questionnaire = redis_client.get(f"questionnaire_{user_id}")
        if not questionnaire:
            questionnaire = await generate_questionnaire()
            redis_client.set(f"questionnaire_{user_id}", questionnaire.model_dump_json())
        else:
            questionnaire = Questionnaire.model_validate_json(questionnaire)
        return questionnaire
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to get questionnaire: {str(e)}")

@router.post("/submit")
async def submit_questionnaire(questionnaire: Questionnaire, current_user: User = Depends(get_current_user)):
    """
    Submits the user's completed questionnaire, generates a score sheet, and saves it.

    Args:
        questionnaire (Questionnaire): The completed questionnaire.
        current_user (User): The current authenticated user.

    Returns:
        dict: The ID of the saved score and the score sheet.

    Raises:
        HTTPException: If the submission or score generation fails.
    """
    try:
        user_id = current_user.id
        score_sheet = await generate_score_sheet(questionnaire, user_id)
        await save_score(score_sheet)
        redis_client.delete(f"questionnaire_{user_id}")
        return {"score_id": score_sheet.id, "score": score_sheet}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to submit questionnaire: {str(e)}")




