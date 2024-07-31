from openai import OpenAI
from pathlib import Path
from io import BytesIO, BufferedReader
import uuid
import os

client = OpenAI()

async def get_openai_response(user_message: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content

async def text_to_speech(text: str):
    speech_file_path = Path(__file__).parent / "speech.mp3"

    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="alloy",
        input=text
    ) as response:
        response.stream_to_file(speech_file_path)

    return True


def speech_to_text(audio_data) -> str:
    # Read file content
    buffer = BytesIO(audio_data)
    buffer.name = "file.mp3"

    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=buffer,
        language="en",
        response_format="text"
    )

    buffer.close()

    return transcript
