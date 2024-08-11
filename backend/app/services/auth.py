import jwt
import os
from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

# Constants for Password hashing and token generation
SECRET_KEY = os.getenv("SECRET_KEY", None)
if SECRET_KEY is None:
    raise EnvironmentError("SECRET_KEY is not set in environment variables.")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 43200  # Will expire after 30 days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Hash the given password using bcrypt.

    Args:
        password (str): The plain text password.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify that a plain password matches the hashed password.

    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Create a JWT access token.

    Args:
        data (dict): The data to encode in the token.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """
    Decode a JWT token.

    Args:
        token (str): The JWT token to decode.

    Returns:
        dict: The decoded data if the token is valid.

    Raises:
        ExpiredSignatureError: If the token has expired.
        InvalidTokenError: If the token is invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise ExpiredSignatureError("The token has expired.")
    except InvalidTokenError:
        raise InvalidTokenError("Invalid token.")