from io import BytesIO
import base64

def base64_to_bytesio(base64_audio: str) -> BytesIO:
    """
    Converts a base64-encoded audio string into a BytesIO object.
    """
    # Step 1: Remove the "data:audio/mp3;base64," prefix if it's there
    if base64_audio.startswith('"') and base64_audio.endswith('"'):
        base64_audio = base64_audio[1:-1]
    if base64_audio.startswith("data:audio/mp3;base64,"):
        base64_audio = base64_audio.split(",")[1]

    # Step 2: Decode the base64 string into bytes
    audio_bytes = base64.b64decode(base64_audio)

    # Step 3: Wrap the bytes in a BytesIO object
    return BytesIO(audio_bytes)