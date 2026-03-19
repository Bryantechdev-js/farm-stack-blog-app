from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise ValueError("MONGO_URL environment variable is not set. Please check your .env file.")

print(f"🔄 Connecting to MongoDB: {MONGO_URL[:50]}...")

client = AsyncIOMotorClient(MONGO_URL)
db = client.blog

print("✅ MongoDB connection initialized")