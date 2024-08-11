import os
import pytest
from app.services.auth import get_password_hash, verify_password, create_access_token, decode_access_token
from datetime import datetime, timedelta, timezone
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

os.environ['SECRET_KEY'] = 'fake_secret_key'

def test_get_password_hash():
    password = "mysecretpassword"
    hashed_password = get_password_hash(password)
    assert hashed_password != password  # Ensure the hash is different from the plain password
    assert len(hashed_password) > 0     # Ensure the hash is not empty

def test_verify_password():
    password = "mysecretpassword"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password) is True  # Password should match the hash
    assert verify_password("wrongpassword", hashed_password) is False  # Wrong password should not match

def test_create_access_token():
    data = {"sub": "user_id"}
    token = create_access_token(data)
    assert isinstance(token, str)  # Ensure the token is a string
    assert len(token) > 0          # Ensure the token is not empty

def test_decode_access_token():
    data = {"sub": "user_id"}
    token = create_access_token(data)
    decoded_data = decode_access_token(token)
    assert decoded_data["sub"] == "user_id"  # Ensure the correct data is decoded

def test_decode_access_token_expired():
    # Create an already expired token
    data = {"sub": "user_id"}
    expired_token = create_access_token(data, expires_delta=timedelta(seconds=-1))  # Token expired 1 second ago

    # Attempt to decode the expired token, which should raise ExpiredSignatureError
    with pytest.raises(ExpiredSignatureError):
        decode_access_token(expired_token)

def test_decode_access_token_invalid():
    with pytest.raises(InvalidTokenError):
        decode_access_token("invalid.token.here")
