from pydantic import BaseModel, EmailStr, Field
import uuid

class UserBase(BaseModel):
    """
    Base model for a user, containing common fields.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier for the user.")
    email: EmailStr = Field(..., description="The email address of the user.")
    name: str = Field(..., description="The name of the user.")

class User(UserBase):
    """
    Model representing a user, including hashed password.
    """
    hashed_password: str = Field(..., description="The hashed password of the user.")

class UserCreate(BaseModel):
    """
    Model for creating a new user.
    """
    email: EmailStr = Field(..., description="The email address of the new user.")
    name: str = Field(..., description="The name of the new user.")
    password: str = Field(..., description="The password for the new user.")

class UserToken(BaseModel):
    """
    Model representing the token returned after user authentication.
    """
    access_token: str = Field(..., description="The access token for the authenticated session.")
    token_type: str = Field(..., description="The type of the token (e.g., 'bearer').")

class UserLogin(BaseModel):
    """
    Model for user login credentials.
    """
    email: EmailStr = Field(..., description="The email address of the user attempting to log in.")
    password: str = Field(..., description="The password of the user attempting to log in.")
