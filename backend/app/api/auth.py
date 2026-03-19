from fastapi import APIRouter, Response, HTTPException, Request
from app.db.mongo import db
from app.core.security import hash_password, verify_password, create_token, SECRET, ALGO
from app.models.user import UserCreate
from datetime import datetime
from bson import ObjectId
from jose import jwt, JWTError
import json

router = APIRouter(prefix="/auth")

@router.post("/signup")
async def signup(user: UserCreate):
    try:
        print(f"[SIGNUP] Attempt for email: {user.email}")
        
        # Check if user exists
        existing = await db.users.find_one({"email": user.email})
        if existing:
            print(f"[SIGNUP] Email already exists: {user.email}")
            raise HTTPException(400, "Email already exists")
        
        # Hash password
        print(f"[SIGNUP] Hashing password...")
        hashed = hash_password(user.password)
        print(f"[SIGNUP] Password hashed successfully")
        
        # Insert user
        print(f"[SIGNUP] Inserting user into database...")
        result = await db.users.insert_one({
            "email": user.email,
            "password": hashed,
            "role": "user",
            "created_at": datetime.utcnow()
        })
        
        print(f"[SIGNUP] User created successfully: {result.inserted_id}")
        return {
            "message": "User created successfully",
            "user_id": str(result.inserted_id)
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"[SIGNUP] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Signup failed: {str(e)}")

@router.post("/login")
async def login(user: UserCreate, response: Response):
    try:
        print(f"[LOGIN] Attempt for email: {user.email}")
        
        # Find user
        db_user = await db.users.find_one({"email": user.email})
        if not db_user:
            print(f"[LOGIN] User not found: {user.email}")
            raise HTTPException(401, "Invalid credentials")
        
        # Verify password
        print(f"[LOGIN] Verifying password...")
        if not verify_password(user.password, db_user["password"]):
            print(f"[LOGIN] Password verification failed for: {user.email}")
            raise HTTPException(401, "Invalid credentials")
        
        # Create token
        print(f"[LOGIN] Creating token...")
        token = create_token(str(db_user["_id"]), db_user.get("role", "user"))
        print(f"[LOGIN] Token created for user: {user.email}")
        
        # Set cookie
        print(f"[LOGIN] Setting cookie...")
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=3600,
            path="/",
        )
        print(f"[LOGIN] Cookie set for user: {user.email}")
        
        return {
            "message": "Login successful",
            "user": {
                "id": str(db_user["_id"]),
                "email": db_user["email"],
                "role": db_user.get("role", "user")
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"[LOGIN] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Login failed: {str(e)}")

@router.post("/logout")
async def logout(response: Response):
    try:
        response.delete_cookie(
            "access_token",
            path="/",
            samesite="lax"
        )
        return {"message": "Logged out successfully","status":200,"ok":True}
    except Exception as e:
        print(f"[LOGOUT] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Logout failed: {str(e)}")

@router.get("/me")
async def get_current_user(request: Request):
    try:
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(401, "Not authenticated")
        
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(401, "Invalid token")
        
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(401, "User not found")
        
        return {
            "id": str(user["_id"]),
            "email": user["email"],
            "role": user.get("role", "user"),
            "created_at": user.get("created_at")
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"[GET_ME] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(401, "Invalid token")
