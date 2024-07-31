from app.models.score import EnglishScoreSheet
from bson import ObjectId
from app.utils.mongo_client import scores_collection

# Saves EnglishScoreSheet to database
async def save_score(score_sheet: EnglishScoreSheet):
    result = await scores_collection.insert_one(score_sheet.model_dump())
    return str(result.inserted_id)

# Retrieves all the EnglishScores of the user
async def get_all_scores(user_id: str) -> list:
    score_sheets = []
    async for score_sheet in scores_collection.find({"user_id": user_id}):
        score_sheets.append(EnglishScoreSheet.model_validate(score_sheet))
    return score_sheets

# Retrieves single EnglishScore
def get_score_by_id(score_id: str):
    return scores_collection.find_one({"_id": ObjectId(score_id)})

# Deletes single EnglishScore
def delete_score_by_id(score_id: str):
    return scores_collection.delete_one({"_id": ObjectId(score_id)})