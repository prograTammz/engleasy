import json

from fastapi import APIRouter, Depends, HTTPException
from app.routers.auth import get_current_user
from app.models.user import User
from app.models.assessment import Questionnaire
from app.models.score import EnglishScoreSheet
from app.services.assessment import generate_questionnaire, generate_score_sheet
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

@router.post("/submit")
async def submit_questionnaire(questionnaire: Questionnaire, current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    # questionnaire_json = redis_client.get(f"questionnaire_{user_id}")
    # if not questionnaire_json:
    #     raise HTTPException(status_code=404, detail="Questionnaire not found")
    score = await generate_score_sheet(questionnaire.model_dump_json(), user_id)
    redis_client.delete(f"questionnaire_{user_id}")
    return {"score": score}


