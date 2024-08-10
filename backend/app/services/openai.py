from openai import OpenAI
from io import BytesIO

client = OpenAI()

# Takes a prompt as a string and creates request to Chatgpt 4o
async def create_gpt_completion(prompt: str) -> str:

    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "assistant", "content": prompt}
        ]
    )

    return response.choices[0].message.content

async def text_to_speech(text: str) -> BytesIO:
    # Initialize a BytesIO buffer
    audio_data = BytesIO()

    # Call the OpenAI API to generate speech from text
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="alloy",
        input=text,
        response_format="mp3"
    ) as response:
        for chunk in response.iter_bytes(1024):
            audio_data.write(chunk)

    audio_data.seek(0)

    return audio_data

def speech_to_text(buffer: BytesIO) -> str:
    # Read file content
    buffer.seek(0)
    buffer.name = "file.mp3"

    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=buffer,
        language="en",
        response_format="text"
    )

    return transcript
