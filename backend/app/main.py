# main.py
from fastapi import FastAPI, HTTPException, UploadFile, File
from app.routers import auth, assessment, scores,chat
# To be cleaned VVVVVVVV
# from fastapi.responses import StreamingResponse
# from models import (ChatMessage, TextToAudioRequest)
# from database import (
#     add_chat,
#     delete_chat,
#     retrieve_chats,
#     retrieve_chat,
#     update_chat
# )
# from bucket_storage import upload_audio_s3
# from openai_integration import (get_openai_response,text_to_speech, speech_to_text)
# from pathlib import Path
# import os
# To be cleaned ^^^^^^^^^^

app = FastAPI()

app.include_router(auth.router, prefix="/auth")
app.include_router(assessment.router, prefix="/assessment")
app.include_router(scores.router, prefix="/scores")
app.include_router(chat.router, prefix="/chat")


# To be cleaned VVVVVVVV
# def iterfile(file_path: str):
#     with open(file_path, mode="rb") as file_like:
#         yield from file_like

# @fastapi_app.get("/chats", response_model=list[ChatMessage])
# async def get_chats():
#     chats = await retrieve_chats()
#     return chats

# @fastapi_app.post("/chats", response_model=ChatMessage)
# async def create_chat(chat: ChatMessage):
#     chat_data = chat.dict(exclude_unset=True)
#     chat_data['sender'] = "user"
#     user_chat = await add_chat(chat_data)

#     # Get OpenAI response
#     bot_response_text = await get_openai_response(chat.text)

#     # Save OpenAI response to the database
#     bot_chat = ChatMessage(
#         text=bot_response_text,
#         sender="bot",
#     ).dict(exclude_unset=True)

#     bot_chat_saved = await add_chat(bot_chat)

#     return bot_chat_saved

# @fastapi_app.get("/chats/{id}", response_model=ChatMessage)
# async def get_chat(id: str):
#     chat = await retrieve_chat(id)
#     if chat:
#         return chat
#     raise HTTPException(status_code=404, detail=f"Chat with ID {id} not found")

# @fastapi_app.put("/chats/{id}")
# async def update_chat_data(id: str, chat: ChatMessage):
#     chat_data = chat.dict(exclude_unset=True)
#     updated = await update_chat(id, chat_data)
#     if updated:
#         return f"Chat with ID {id} updated successfully"
#     raise HTTPException(status_code=404, detail=f"Chat with ID {id} not found")

# @fastapi_app.delete("/chats/{id}")
# async def delete_chat_data(id: str):
#     deleted = await delete_chat(id)
#     if deleted:
#         return f"Chat with ID {id} deleted successfully"
#     raise HTTPException(status_code=404, detail=f"Chat with ID {id} not found")

# @fastapi_app.post("/text-to-audio")
# async def text_to_audio_endpoint(request: TextToAudioRequest):
#     speech_file_path = Path(__file__).parent / "speech.mp3"

#     audio_file = await text_to_speech(request.text)

#     if not os.path.exists(speech_file_path):
#             raise HTTPException(status_code=404, detail="File not found")

#     if audio_file:
#         return StreamingResponse(iterfile(speech_file_path), media_type="audio/mpeg")
#     raise HTTPException(status_code=404, detail=f"Couldn't generate an audio file")

# @fastapi_app.post("/upload-audio/")
# async def upload_audio(file: UploadFile = File(...)):

#         audio_data = await file.read()
#         # Transcribe the audio file using OpenAI
#         transcription = speech_to_text(audio_data)

#         # Upload the file to S3
#         fileUrl = await upload_audio_s3(file, audio_data)

#         return {
#             "transcription": transcription,
#             "s3_url": fileUrl
#         }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
