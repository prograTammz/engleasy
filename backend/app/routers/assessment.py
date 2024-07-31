from bson import ObjectId

from fastapi import APIRouter, Depends
from app.routers.auth import get_current_user
from app.models.user import User
from app.models.assessment import Questionnaire
from app.services.assessment import generate_questionnaire, generate_score_sheet
from app.utils.redis_client import redis_client
from app.services.scores import save_score
from app.utils.mongo_client import users_collection

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
    score_sheet = await generate_score_sheet(questionnaire.model_dump_json(), user_id)
    score_id = await save_score(score_sheet)
    redis_client.delete(f"questionnaire_{user_id}")
    await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"on_progress_test": False}})
    return {"score_id": score_id, "score": score_sheet}




