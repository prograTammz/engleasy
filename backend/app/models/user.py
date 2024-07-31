from pydantic import BaseModel, EmailStr
from typing import List, Optional

class User(BaseModel):
    id: Optional[str]
    email: EmailStr
    hashed_password: str
    previous_tests: List[str] = []
    on_progress_test: Optional[str] = None