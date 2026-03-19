#!/usr/bin/env python3
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

async def check_image_paths():
    mongo_url = os.getenv("MONGO_URL")
    client = AsyncIOMotorClient(mongo_url)
    db = client.blog_db
    
    posts = await db.posts.find({}).to_list(None)
    print(f"Found {len(posts)} posts")
    
    for post in posts:
        print(f"\nPost: {post.get('title')}")
        print(f"  Image path in DB: {post.get('image')}")
        print(f"  Image path type: {type(post.get('image'))}")
        
        # Check if file exists
        image_path = post.get('image')
        if image_path:
            if image_path.startswith('/'):
                check_path = image_path[1:]  # Remove leading /
            else:
                check_path = image_path
            
            if os.path.exists(check_path):
                size = os.path.getsize(check_path)
                print(f"  File exists: YES ({size} bytes)")
            else:
                print(f"  File exists: NO (checked path: {check_path})")
    
    client.close()

asyncio.run(check_image_paths())
