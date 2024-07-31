from app.models.score import EnglishScoreSheet
from datetime import datetime
from app.utils.mongo_client import scores_collection

# Saves EnglishScoreSheet to database
def save_score(score_sheet: EnglishScoreSheet):
    result = scores_collection.insert_one(score_sheet.model_dump())
    return str(result.inserted_id)