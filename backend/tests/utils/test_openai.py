import pytest
from io import BytesIO
from app.utils.openai import base64_to_bytesio

def test_base64_to_bytesio():
    # Properly padded base64 string for "Hello world!"
    base64_audio = "SGVsbG8gd29ybGQh"  # This is already correctly padded

    result = base64_to_bytesio(base64_audio)
    assert isinstance(result, BytesIO)
    assert result.read() == b"Hello world!"

