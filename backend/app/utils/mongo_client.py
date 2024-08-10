from motor.motor_asyncio import AsyncIOMotorClient
import os

# MongoDB connection
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')

try:
    client = AsyncIOMotorClient(MONGO_URL)
    database = client.english_assessment
except Exception as e:
    raise RuntimeError(f"Failed to connect to MongoDB: {str(e)}")

users_collection = database.get_collection("users")
scores_collection = database.get_collection("scores")