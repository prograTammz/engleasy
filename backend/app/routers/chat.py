# Packages
from fastapi import APIRouter, WebSocket, Depends, WebSocketDisconnect, HTTPException, status, Body
from typing import Dict
# Routing
from app.routers.auth import get_current_user, get_current_user_websocket
# Models
from app.models.chat import ChatMessage
from app.models.user import User
# Services
from app.services.chat import ChatService

router = APIRouter()
connections: Dict[str, WebSocket] = {}

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chat communication.

    Args:
        websocket (WebSocket): The WebSocket connection.

    Raises:
        WebSocketDisconnect: If the connection is closed unexpectedly.
    """
    # Opening the Socket connection & storing it in memory
    await websocket.accept()

    # Getting the token and user
    user: User = await get_current_user_websocket(websocket)
    user_id = user.id
    connections[user_id] = websocket

    # Initializing ChatService
    chat_service = ChatService(user_id, websocket)
    await chat_service.setup()

    try:
        opening_messages = await chat_service.get_opening_message()
        for message in opening_messages:
            await websocket.send_text(message.model_dump_json())

        while True:
            message = await websocket.receive_text()
            responses = await chat_service.handle_message(message)
            for response in responses:
                await websocket.send_text(response.model_dump_json())
                # When the chat is over
                if response.type == 'sheet':
                    websocket.close(status.WS_1000_NORMAL_CLOSURE)

    except WebSocketDisconnect:
        # Deleting the connection
        del connections[user_id]
    except Exception as e:
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        del connections[user_id]

# The chatbot will use this request to get the chat history IF EXIST
# Before opening a websocket
@router.get("/messages")
async def get_chat_history(current_user: User = Depends(get_current_user)):
    """
    Retrieves the chat history for the current user.

    Args:
        current_user (User): The current authenticated user.

    Returns:
        ChatHistory: The user's chat history.
    """
    user_id = current_user.id
    # Initializing ChatService
    chat_service = ChatService(user_id)
    await chat_service.setup()
    return chat_service.get_chat_history()

# For editing a message, it will search the questionnaire answers
# and edit the answer accordingly
@router.patch("/messages/{message_id}", response_model=ChatMessage)
async def edit_message(message_id: str, text = Body(..., embed=True), current_user: User = Depends(get_current_user)):
    """
    Edits a specific message and updates the corresponding answer in the questionnaire.

    Args:
        message_id (str): The ID of the message to edit.
        text (str): The new text for the message.
        current_user (User): The current authenticated user.

    Returns:
        ChatMessage: The updated message.

    Raises:
        HTTPException: If the message is not found or cannot be updated.
    """
    user_id = current_user.id
    chat_service = ChatService(user_id)
    await chat_service.setup()

    chat_message = chat_service.edit_message(message_id, text)

    if not chat_message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found or could not be updated.")

    return chat_message

# For deleting a message, it will search the questionnaire answers
# and delete the answer accordingly, and if the questionnaire is still on-going the question will be repeated
@router.delete("/messages/{message_id}")
async def delete_message(message_id: str, current_user: User = Depends(get_current_user)):
    """
    Deletes a specific message and updates the questionnaire accordingly.

    Args:
        message_id (str): The ID of the message to delete.
        current_user (User): The current authenticated user.

    Returns:
        dict: A confirmation of deletion.

    Raises:
        HTTPException: If the message is not found or cannot be deleted.
    """
    user_id = current_user.id
    chat_service = ChatService(user_id)
    await chat_service.setup()

    success = chat_service.delete_message(message_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found or could not be deleted.")

    return {"message": "Message deleted successfully"}
