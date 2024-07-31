from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User, UserCreate, UserToken
from app.utils.mongo_client import users_collection
from app.services.auth import get_password_hash, verify_password, create_access_token
from uuid import uuid4
router = APIRouter()

@router.post("/register", response_model=User)
async def register(user: UserCreate):
    user_dict = user.model_dump()
    user_dict['hashed_password'] = get_password_hash(user.password)
    user_dict['id'] = str(uuid4())
    del user_dict['password']
    new_user = User(**user_dict)
    result = await users_collection.insert_one(new_user.model_dump())
    new_user.id = str(result.inserted_id)
    return new_user

@router.post("/token", response_model=UserToken)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": str(user["_id"])}
    )
    return {"access_token": access_token, "token_type": "bearer"}