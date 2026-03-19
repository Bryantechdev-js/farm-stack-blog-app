#!/usr/bin/env python3
"""
Simple test script to verify auth endpoints work
"""
import asyncio
import json
from app.db.mongo import db
from app.core.security import hash_password, verify_password, create_token
from app.models.user import UserCreate
from datetime import datetime
from bson import ObjectId

async def test_auth():
    print("=" * 50)
    print("Testing Auth System")
    print("=" * 50)
    
    # Test 1: Hash and verify password
    print("\n[TEST 1] Password hashing and verification")
    try:
        password = "testpassword123"
        hashed = hash_password(password)
        print(f"✅ Password hashed: {hashed[:30]}...")
        
        is_valid = verify_password(password, hashed)
        print(f"✅ Password verification: {is_valid}")
        
        is_invalid = verify_password("wrongpassword", hashed)
        print(f"✅ Wrong password rejected: {not is_invalid}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Create token
    print("\n[TEST 2] Token creation")
    try:
        user_id = "507f1f77bcf86cd799439011"
        role = "user"
        token = create_token(user_id, role)
        print(f"✅ Token created: {token[:30]}...")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 3: Database connection
    print("\n[TEST 3] Database connection")
    try:
        result = await db.users.find_one({"email": "test@test.com"})
        print(f"✅ Database query successful")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 4: Create test user
    print("\n[TEST 4] Create test user")
    try:
        test_email = f"test_{datetime.utcnow().timestamp()}@test.com"
        test_password = "testpassword123"
        
        # Check if exists
        existing = await db.users.find_one({"email": test_email})
        if existing:
            print(f"⚠️  User already exists")
        else:
            # Create user
            hashed = hash_password(test_password)
            result = await db.users.insert_one({
                "email": test_email,
                "password": hashed,
                "role": "user",
                "created_at": datetime.utcnow()
            })
            print(f"✅ User created: {result.inserted_id}")
            
            # Verify user
            user = await db.users.find_one({"_id": result.inserted_id})
            print(f"✅ User verified: {user['email']}")
            
            # Test password verification
            is_valid = verify_password(test_password, user['password'])
            print(f"✅ Password verification: {is_valid}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("All tests completed!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(test_auth())
