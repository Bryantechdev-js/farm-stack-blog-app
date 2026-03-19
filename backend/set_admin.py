#!/usr/bin/env python3
"""
Script to set a specific user as admin by email
Usage: python set_admin.py bryantech.dev@gmail.com
"""
import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

async def set_admin(email: str):
    mongo_url = os.getenv("MONGO_URL")
    client = AsyncIOMotorClient(mongo_url)
    db = client.blog_db
    
    try:
        # Find user by email
        user = await db.users.find_one({"email": email})
        if not user:
            print(f"❌ User with email '{email}' not found")
            return False
        
        # Update user role to admin
        result = await db.users.update_one(
            {"email": email},
            {"$set": {"role": "admin"}}
        )
        
        if result.modified_count > 0:
            print(f"✅ User '{email}' is now an admin!")
            return True
        else:
            print(f"⚠️ User '{email}' is already an admin")
            return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    finally:
        client.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python set_admin.py <email>")
        print("Example: python set_admin.py bryantech.dev@gmail.com")
        sys.exit(1)
    
    email = sys.argv[1]
    success = asyncio.run(set_admin(email))
    sys.exit(0 if success else 1)
