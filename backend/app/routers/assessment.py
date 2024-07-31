import json

from fastapi import APIRouter, Depends
from app.routers.auth import get_current_user
from app.models.user import User
from app.models.assessment import Questionnaire
from app.services.assessment import generate_questionnaire
from app.utils.redis_client import redis_client


router = APIRouter()

@router.get("/questionnaire")
async def get_questionnaire(current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    questionnaire = redis_client.get(f"questionnaire_{user_id}")
    if not questionnaire:
        questionnaire = await generate_questionnaire()
        redis_client.set(f"questionnaire_{user_id}", questionnaire.model_dump_json())
    else:
        questionnaire = Questionnaire.model_validate_json(questionnaire)
    return questionnaire


