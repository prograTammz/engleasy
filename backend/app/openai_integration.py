from openai import OpenAI
from pathlib import Path

client = OpenAI()

async def get_openai_response(user_message: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    print(response.choices[0].message.content)
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


async def speech_to_text(audio_file) -> str:
    transcript = client.audio.transcriptions.create(
        model="whisper-2",
        file=audio_file,
        language="en",
        response_format='text'

    )

    return transcript
