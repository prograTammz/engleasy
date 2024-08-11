# import pytest
# from unittest.mock import patch, AsyncMock
# from datetime import datetime, timezone
# from app.services.chat import ChatService
# from app.models.chat import ChatMessage, ChatHistory

# @pytest.fixture
# def chat_service():
#     return ChatService(user_id="test_user_id")

# @patch("app.services.chat.ChatService.__save_chat_history", new_callable=AsyncMock)
# def test_create_message(mock_save_history, chat_service):
#     message = chat_service._ChatService__create_message("Hello!", "user")
#     assert isinstance(message, ChatMessage)
#     assert message.content == "Hello!"
#     assert message.sender == "user"
#     mock_save_history.assert_called_once()

# @patch("app.services.chat.ChatService.__save_chat_history", new_callable=AsyncMock)
# def test_edit_message(mock_save_history, chat_service):
#     message_id = "test_message_id"
#     new_text = "Edited text"
#     chat_service.edit_message(message_id, new_text)
#     mock_save_history.assert_called_once()

# @patch("app.services.chat.ChatService.__save_chat_history", new_callable=AsyncMock)
# def test_delete_message(mock_save_history, chat_service):
#     message_id = "test_message_id"
#     chat_service.delete_message(message_id)
#     mock_save_history.assert_called_once()

# @patch("app.services.chat.generate_questionnaire", new_callable=AsyncMock)
# def test_start_assessment(mock_generate_questionnaire, chat_service):
#     mock_generate_questionnaire.return_value = ChatHistory(messages=[])
#     result = chat_service._ChatService__start_assessment()
#     assert result is not None
#     mock_generate_questionnaire.assert_called_once()
