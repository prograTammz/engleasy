from fastapi import APIRouter, Depends, HTTPException
from app.routers.auth import get_current_user
from app.models.user import User
from app.services.scores import (
    get_all_scores,
    get_score_by_id,
    delete_score_by_id
)

router = APIRouter()

@router.get("/")
async def get_scores(current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    scores = await get_all_scores(user_id)
    return scores

@router.get("/{score_id}")
async def get_score(score_id: str, current_user: User = Depends(get_current_user)):
    score = await get_score_by_id(score_id)
    if not score:
        raise HTTPException(status_code=404, detail="Score not found")
    return score

@router.delete("/{score_id}")
async def delete_score(score_id: str, current_user: User = Depends(get_current_user)):
    result = await delete_score_by_id(score_id)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Score not found")
    return {"message": "Score deleted successfully"}