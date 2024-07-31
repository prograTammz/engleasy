from fastapi import APIRouter
from app.models.user import User, UserCreate
from app.utils.mongo_client import users_collection
from app.services.auth import get_password_hash
router = APIRouter()

@router.post("/register", response_model=User)
async def register(user: UserCreate):
    user_dict = user.model_dump()
    user_dict['hashed_password'] = get_password_hash(user.password)
    del user_dict['password']
    new_user = User(**user_dict)
    result = await users_collection.insert_one(new_user.model_dump())
    new_user.id = str(result.inserted_id)
    return new_user