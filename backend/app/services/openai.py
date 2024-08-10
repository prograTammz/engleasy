from openai import OpenAI
from io import BytesIO

client = OpenAI()

# Takes a prompt as a string and creates a request to ChatGPT 4o
async def create_gpt_completion(prompt: str) -> str:
    """
    Generates a completion for the provided prompt using OpenAI's GPT model.

    Args:
        prompt (str): The prompt to generate a response for.

    Returns:
        str: The generated response from the model.

    Raises:
        Exception: If the API request fails.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "assistant", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Failed to create GPT completion: {str(e)}")

async def text_to_speech(text: str) -> BytesIO:
    """
    Converts the provided text to speech using OpenAI's TTS model.

    Args:
        text (str): The text to convert to speech.

    Returns:
        BytesIO: The generated speech audio data.

    Raises:
        Exception: If the API request fails.
    """
    audio_data = BytesIO()

    try:
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
    except Exception as e:
        raise Exception(f"Failed to convert text to speech: {str(e)}")

def speech_to_text(buffer: BytesIO) -> str:
    """
    Converts the provided speech audio data to text using OpenAI's Whisper model.

    Args:
        buffer (BytesIO): The audio data buffer.

    Returns:
        str: The transcribed text.

    Raises:
        Exception: If the API request fails.
    """
    buffer.seek(0)
    buffer.name = "file.mp3"

    try:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=buffer,
            language="en",
            response_format="text"
        )
        return transcript
    except Exception as e:
        raise Exception(f"Failed to convert speech to text: {str(e)}")
