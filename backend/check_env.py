#!/usr/bin/env python3
"""
Check if environment variables are being loaded correctly
"""

import os
from dotenv import load_dotenv

print("=" * 70)
print("Environment Variable Check")
print("=" * 70)
print()

# Load from .env file
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

print("1. MONGO_URL from environment:")
if MONGO_URL:
    print(f"   ✅ Found: {MONGO_URL[:60]}...")
    print(f"   Length: {len(MONGO_URL)} characters")
    
    # Check if it's the correct format
    if "mongodb+srv://" in MONGO_URL:
        print("   ✅ Correct format (MongoDB Atlas)")
    elif "localhost" in MONGO_URL:
        print("   ❌ Wrong format (localhost - should be MongoDB Atlas)")
    else:
        print("   ⚠️  Unknown format")
else:
    print("   ❌ NOT FOUND - .env file not loaded correctly")
    print()
    print("   Troubleshooting:")
    print("   1. Check backend/.env exists")
    print("   2. Check MONGO_URL is set in .env")
    print("   3. Check .env file is not empty")
    print("   4. Check .env file has no line breaks in URL")

print()
print("2. .env file location:")
import pathlib
env_path = pathlib.Path("backend/.env")
if env_path.exists():
    print(f"   ✅ Found at: {env_path.absolute()}")
    print(f"   Size: {env_path.stat().st_size} bytes")
else:
    print(f"   ❌ NOT FOUND at: {env_path.absolute()}")

print()
print("3. .env file contents:")
try:
    with open("backend/.env", "r") as f:
        content = f.read()
        print(f"   {repr(content)}")
except Exception as e:
    print(f"   ❌ Error reading file: {e}")

print()
print("=" * 70)

if MONGO_URL and "mongodb+srv://" in MONGO_URL:
    print("✅ Environment variables are correctly configured!")
    print()
    print("Next steps:")
    print("1. Restart the backend: uvicorn app.main:app --reload")
    print("2. Test signup at http://localhost:3000")
else:
    print("❌ Environment variables are NOT correctly configured!")
    print()
    print("Fix:")
    print("1. Edit backend/.env")
    print("2. Make sure MONGO_URL is on a single line")
    print("3. Make sure it starts with mongodb+srv://")
    print("4. Restart the backend")

print("=" * 70)
