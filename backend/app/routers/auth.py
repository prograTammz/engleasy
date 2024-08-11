from fastapi import WebSocket, APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.models.user import User, UserCreate, UserToken, UserLogin, UserBase
from app.utils.mongo_client import users_collection
from app.services.auth import get_password_hash, verify_password, create_access_token, decode_access_token
from uuid import uuid4
from bson import ObjectId

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate) -> User:
    """
    Registers a new user.

    Args:
        user (UserCreate): The user data to register.

    Returns:
        User: The newly registered user.

    Raises:
        HTTPException: If the email is already registered.
    """
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user_dict = user.model_dump()
    user_dict['hashed_password'] = get_password_hash(user.password)
    del user_dict['password']
    new_user = User(**user_dict)
    result = await users_collection.insert_one(new_user.model_dump())
    new_user.id = str(result.inserted_id)
    return new_user

@router.post("/login", response_model=UserToken)
async def login(login: UserLogin) -> UserToken:
    """
    Authenticates a user and returns a JWT token.

    Args:
        login (UserLogin): The user's login credentials.

    Returns:
        UserToken: The access token and token type.

    Raises:
        HTTPException: If the email or password is incorrect.
    """
    user = await users_collection.find_one({"email": login.email})
    if not user or not verify_password(login.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(user["_id"])})
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserBase:
    """
    Retrieves the current user based on the JWT token.

    Args:
        token (str): The JWT token.

    Returns:
        UserBase: The current authenticated user.

    Raises:
        HTTPException: If the token is invalid or the user is not found.
    """
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials: Wrong Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id: str = payload.get("sub")
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials: User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    del user['hashed_password']
    return UserBase(**user)

@router.get("/me", response_model=UserBase)
async def get_me(current_user: UserBase = Depends(get_current_user)) -> UserBase:
    """
    Retrieves the current authenticated user's information.

    Args:
        current_user (UserBase): The current user.

    Returns:
        UserBase: The user's information.
    """
    return current_user

async def get_current_user_websocket(websocket: WebSocket) -> UserBase:
    """
    Retrieves the current authenticated user based on the JWT token in a WebSocket connection.

    Args:
        websocket (WebSocket): The WebSocket connection.

    Returns:
        UserBase: The current authenticated user.

    Raises:
        Exception: If the token is invalid or missing.
    """
    try:
        data = await websocket.receive_json()
        token = data.get("token")

        if not token:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        user = await get_current_user(token)

        if user is None:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return None

        return user

    except Exception as e:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None
