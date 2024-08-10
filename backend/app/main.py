# main.py
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, assessment, scores, chat
import os

app = FastAPI(
    title="Engleasy Backend",
    description="AI assistant to improve your English skills",
    version="0.1.0"
)

# CORS settings based on environment variables
origins = os.getenv("CORS_ORIGINS", "http://localhost:4242").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth")
app.include_router(assessment.router, prefix="/assessment")
app.include_router(scores.router, prefix="/scores")
app.include_router(chat.router, prefix="/chat")

if __name__ == "__main__":
    import uvicorn
    # Host and port can be set via environment variables
    uvicorn.run(app, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 8000)))

