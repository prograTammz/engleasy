import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from app.services.openai import create_gpt_completion, text_to_speech, speech_to_text
from io import BytesIO

pytestmark = pytest.mark.asyncio

# Test for create_gpt_completion function
@patch("app.services.openai.client.chat.completions.create")
async def test_create_gpt_completion(mock_create):
    # Mock the response from OpenAI's GPT-4 API
    mock_create.return_value.choices = [
        MagicMock(message=MagicMock(content='{"response": "This is a test completion"}'))
    ]

    prompt = "Test prompt"
    result = await create_gpt_completion(prompt)

    # Assertions
    assert result == '{"response": "This is a test completion"}'
    mock_create.assert_called_once_with(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "assistant", "content": prompt}
        ]
    )


# Test for speech_to_text function
@patch("app.services.openai.client.audio.transcriptions.create")
def test_speech_to_text(mock_create):
    # Mock the response from OpenAI's Whisper API
    mock_create.return_value = "This is the transcribed text"

    audio_bytes = BytesIO(b"fake_audio_content")
    result = speech_to_text(audio_bytes)

    # Assertions
    assert result == "This is the transcribed text"
    mock_create.assert_called_once_with(
        model="whisper-1",
        file=audio_bytes,
        language="en",
        response_format="text"
    )
