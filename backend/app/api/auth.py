from fastapi import APIRouter, Response, HTTPException, Request
from app.db.mongo import db
from app.core.security import hash_password, verify_password, create_token, SECRET, ALGO
from app.core.email import send_otp_email, verify_otp, delete_otp
from app.models.user import UserCreate, UserUpdate, ForgotPasswordRequest, VerifyOTPRequest, ResetPasswordRequest
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
            "full_name": None,
            "bio": None,
            "avatar_url": None,
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
            "full_name": user.get("full_name"),
            "bio": user.get("bio"),
            "avatar_url": user.get("avatar_url"),
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


@router.post("/forgot-password")
async def forgot_password(request_data: ForgotPasswordRequest):
    try:
        print(f"[FORGOT_PASSWORD] Request for email: {request_data.email}")
        
        # Check if user exists
        user = await db.users.find_one({"email": request_data.email})
        if not user:
            # Don't reveal if email exists (security best practice)
            print(f"[FORGOT_PASSWORD] User not found: {request_data.email}")
            return {"message": "If email exists, OTP has been sent"}
        
        # Generate and send OTP
        otp = await send_otp_email(request_data.email)
        print(f"[FORGOT_PASSWORD] OTP sent to {request_data.email}")
        
        return {
            "message": "OTP sent to your email",
            "otp": otp  # For testing only - remove in production
        }
    except Exception as e:
        print(f"[FORGOT_PASSWORD] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Error processing request: {str(e)}")

@router.post("/verify-otp")
async def verify_otp_endpoint(request_data: VerifyOTPRequest):
    try:
        print(f"[VERIFY_OTP] Verifying OTP for email: {request_data.email}")
        
        # Verify OTP
        is_valid = await verify_otp(request_data.email, request_data.otp)
        if not is_valid:
            print(f"[VERIFY_OTP] Invalid or expired OTP for: {request_data.email}")
            raise HTTPException(400, "Invalid or expired OTP")
        
        print(f"[VERIFY_OTP] OTP verified for: {request_data.email}")
        return {"message": "OTP verified successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"[VERIFY_OTP] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Error verifying OTP: {str(e)}")

@router.post("/reset-password")
async def reset_password(request_data: ResetPasswordRequest):
    try:
        print(f"[RESET_PASSWORD] Request for email: {request_data.email}")
        
        # Verify OTP first
        is_valid = await verify_otp(request_data.email, request_data.otp)
        if not is_valid:
            print(f"[RESET_PASSWORD] Invalid or expired OTP for: {request_data.email}")
            raise HTTPException(400, "Invalid or expired OTP")
        
        # Find user
        user = await db.users.find_one({"email": request_data.email})
        if not user:
            print(f"[RESET_PASSWORD] User not found: {request_data.email}")
            raise HTTPException(404, "User not found")
        
        # Hash new password
        hashed_password = hash_password(request_data.new_password)
        
        # Update password
        await db.users.update_one(
            {"_id": user["_id"]},
            {"$set": {"password": hashed_password}}
        )
        
        # Delete OTP after successful reset
        await delete_otp(request_data.email)
        
        print(f"[RESET_PASSWORD] Password reset successful for: {request_data.email}")
        return {"message": "Password reset successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"[RESET_PASSWORD] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Error resetting password: {str(e)}")

@router.put("/profile")
async def update_profile(update_data: UserUpdate, request: Request):
    try:
        # Get current user
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(401, "Not authenticated")
        
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(401, "Invalid token")
        
        print(f"[UPDATE_PROFILE] Updating profile for user: {user_id}")
        
        # Build update dict with only provided fields
        update_dict = {}
        if update_data.full_name is not None:
            update_dict["full_name"] = update_data.full_name
        if update_data.bio is not None:
            update_dict["bio"] = update_data.bio
        if update_data.avatar_url is not None:
            update_dict["avatar_url"] = update_data.avatar_url
        
        if not update_dict:
            raise HTTPException(400, "No fields to update")
        
        # Update user
        result = await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_dict}
        )
        
        if result.matched_count == 0:
            raise HTTPException(404, "User not found")
        
        # Get updated user
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        
        print(f"[UPDATE_PROFILE] Profile updated for user: {user_id}")
        return {
            "id": str(user["_id"]),
            "email": user["email"],
            "full_name": user.get("full_name"),
            "bio": user.get("bio"),
            "avatar_url": user.get("avatar_url"),
            "role": user.get("role", "user"),
            "created_at": user.get("created_at")
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"[UPDATE_PROFILE] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Error updating profile: {str(e)}")
