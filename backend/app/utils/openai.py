from io import BytesIO
import base64

def base64_to_bytesio(base64_audio: str) -> BytesIO:
    # Step 1: Remove the "data:audio/mp3;base64," prefix if it's there
    base64_audio =base64_audio[1:-1]
    if base64_audio.startswith("data:audio/mp3;base64,"):
        base64_audio = base64_audio.split(",")[1]

    # Step 2: Decode the base64 string into bytes
    audio_bytes = base64.b64decode(base64_audio)

    # Step 3: Wrap the bytes in a BytesIO object
    audio_bytes_io = BytesIO(audio_bytes)

    return audio_bytes_io