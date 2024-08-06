from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
import uuid

class UserBase(BaseModel):
    id: Optional[str]
    email: EmailStr
    name: str
    previous_tests: Optional[List[str]] = []
    on_progress_test: Optional[bool] = None

class User(UserBase):
    hashed_password: str


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str

class UserToken(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str