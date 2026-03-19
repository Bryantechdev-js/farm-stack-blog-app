#!/usr/bin/env python3
"""
Simple MongoDB connection test
"""

import os
import asyncio
from dotenv import load_dotenv

print("=" * 70)
print("MongoDB Connection Test")
print("=" * 70)
print()

# Load environment variables
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

print(f"MONGO_URL: {MONGO_URL}")
print()

if not MONGO_URL:
    print("❌ ERROR: MONGO_URL not found in .env")
    exit(1)

if "localhost" in MONGO_URL:
    print("❌ ERROR: MONGO_URL points to localhost (should be MongoDB Atlas)")
    print()
    print("Fix your .env file:")
    print("MONGO_URL=mongodb+srv://bryan:bryantech.dev@cluster0.vpzmmtb.mongodb.net/blog?appName=Cluster0")
    exit(1)

print("Testing connection...")
print()

try:
    from motor.motor_asyncio import AsyncIOMotorClient
    
    async def test():
        client = AsyncIOMotorClient(MONGO_URL, serverSelectionTimeoutMS=5000)
        await client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
        
        db = client.blog
        users = await db.users.count_documents({})
        posts = await db.posts.count_documents({})
        
        print(f"   Users: {users}")
        print(f"   Posts: {posts}")
        
        client.close()
        return True
    
    asyncio.run(test())
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print()
    print("Troubleshooting:")
    print("1. Check MongoDB Atlas cluster is running")
    print("2. Check your IP is whitelisted in MongoDB Atlas")
    print("3. Check username and password are correct")
    print("4. Check internet connection")
    exit(1)

print()
print("=" * 70)
print("✅ All tests passed!")
print("=" * 70)
