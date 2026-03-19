#!/usr/bin/env python3
"""
Test MongoDB connection
Run this to verify your MongoDB connection is working
"""

import os
import asyncio
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Load environment variables
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

async def test_connection():
    print("=" * 60)
    print("MongoDB Connection Test")
    print("=" * 60)
    print()
    
    if not MONGO_URL:
        print("❌ ERROR: MONGO_URL not found in .env file")
        print("Please create backend/.env with:")
        print("MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/blog")
        return False
    
    print(f"📍 MongoDB URL: {MONGO_URL[:50]}...")
    print()
    
    try:
        print("🔄 Connecting to MongoDB...")
        client = AsyncIOMotorClient(MONGO_URL, serverSelectionTimeoutMS=5000)
        
        # Try to connect
        await client.admin.command('ping')
        print("✅ Successfully connected to MongoDB!")
        print()
        
        # Get database info
        db = client.blog
        collections = await db.list_collection_names()
        print(f"📚 Collections in 'blog' database: {collections if collections else 'None yet'}")
        print()
        
        # Count documents
        users_count = await db.users.count_documents({})
        posts_count = await db.posts.count_documents({})
        print(f"👥 Users: {users_count}")
        print(f"📝 Posts: {posts_count}")
        print()
        
        print("=" * 60)
        print("✅ All tests passed! MongoDB is working correctly.")
        print("=" * 60)
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print()
        print("Troubleshooting:")
        print("1. Check your MongoDB URL in backend/.env")
        print("2. Verify MongoDB Atlas cluster is running")
        print("3. Check IP whitelist in MongoDB Atlas")
        print("4. Verify username and password are correct")
        print()
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = asyncio.run(test_connection())
    exit(0 if success else 1)
