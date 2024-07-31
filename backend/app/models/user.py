from pydantic import BaseModel, EmailStr
from typing import List, Optional

class User(BaseModel):
    id: Optional[str]
    email: EmailStr
    hashed_password: str
    previous_tests: Optional[List[str]] = []
    on_progress_test: Optional[bool] = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserToken(BaseModel):
    access_token: str
    token_type: str