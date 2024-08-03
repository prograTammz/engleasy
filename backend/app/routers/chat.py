# Packages
from fastapi import APIRouter, WebSocket, Depends, WebSocketDisconnect
from typing import List, Dict
#Routing
from app.routers.auth import get_current_user, get_current_user_websocket
# Models
from app.models.chat import ChatMessage
from app.models.user import User
# Services
from app.services.chat import ChatService
# Utilities

router = APIRouter()
connections: Dict[str, WebSocket] = {}

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Opnning the Socket connection & storing it in the memory
    await websocket.accept()
    # Getting the token
    user: User = await get_current_user_websocket(websocket)
    user_id = user.id
    connections[user_id] = websocket
    # Initalizing ChatService
    chat_service = ChatService(user_id, websocket)
    await chat_service.setup()

    try:
        opening_messages = chat_service.get_opening_message()

        for message in opening_messages:
                await websocket.send_json(message.model_dump_json())

        while True:
            data = await websocket.receive()
            responses = await chat_service.handle_message(data)

            for response in responses:
                await websocket.send_json(response.model_dump_json())


    except WebSocketDisconnect:
        # Deleting the connection
        del connections[user_id]

# The chatbot will use this request to get the chat history IF EXIST
# Before openning a websocket
@router.get("/messages")
async def get_chat_history(current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    # Initalizing ChatService
    chat_service = ChatService(user_id)
    await chat_service.setup()

    return chat_service.get_chat_history()

# For editing a message, it will search the questionaire answers
# and edit the answer accordingly
@router.put("/messages/{message_id}", response_model=ChatMessage)
async def edit_message(message_id: str, text: str, current_user: User = Depends(get_current_user)):
    pass

# For deleting a message, it will search the questionaire answers
# and delete the answer accordingly, and if the questionaire is still on-going the
@router.delete("/messages/{message_id}")
async def delete_message(message_id: str, current_user: User = Depends(get_current_user)):
    pass