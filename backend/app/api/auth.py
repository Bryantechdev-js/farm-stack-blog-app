from fastapi import APIRouter, Response, HTTPException, Request
from app.db.mongo import db
from app.core.security import hash_password, verify_password, create_token, SECRET, ALGO
from app.core.email import send_otp_email, verify_otp, delete_otp
from app.models.user import UserCreate, UserUpdate, ForgotPasswordRequest, VerifyOTPRequest, ResetPasswordRequest
from datetime import datetime
from bson import ObjectId
from jose import jwt, JWTError
import json
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth")

@router.post("/signup")
async def signup(user: UserCreate):
    try:
        logger.info(f"Signup attempt for email: {user.email}")
        
        # Check if user exists
        existing = await db.users.find_one({"email": user.email})
        if existing:
            logger.warning(f"Signup failed - email already exists: {user.email}")
            raise HTTPException(400, "Email already exists")
        
        # Hash password
        logger.debug(f"Hashing password for user: {user.email}")
        hashed = hash_password(user.password)
        logger.debug(f"Password hashed successfully for user: {user.email}")
        
        # Check if this is the first user (make them admin)
        user_count = await db.users.count_documents({})
        is_first_user = user_count == 0
        role = "admin" if is_first_user else "user"
        
        logger.info(f"User count: {user_count}, assigning role: {role} to {user.email}")
        
        # Insert user
        logger.debug(f"Inserting user into database: {user.email}")
        result = await db.users.insert_one({
            "email": user.email,
            "password": hashed,
            "role": role,
            "full_name": None,
            "bio": None,
            "avatar_url": None,
            "created_at": datetime.utcnow()
        })
        
        logger.info(f"User created successfully - ID: {result.inserted_id}, Email: {user.email}, Role: {role}")
        return {
            "message": "User created successfully",
            "user_id": str(result.inserted_id),
            "is_admin": is_first_user
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signup error for {user.email}: {str(e)}", exc_info=True)
        raise HTTPException(500, f"Signup failed: {str(e)}")

@router.post("/login")
async def login(user: UserCreate, response: Response):
    try:
        logger.info(f"Login attempt for email: {user.email}")
        
        # Find user
        db_user = await db.users.find_one({"email": user.email})
        if not db_user:
            logger.warning(f"Login failed - user not found: {user.email}")
            raise HTTPException(401, "Invalid credentials")
        
        # Verify password
        logger.debug(f"Verifying password for user: {user.email}")
        if not verify_password(user.password, db_user["password"]):
            logger.warning(f"Login failed - invalid password for: {user.email}")
            raise HTTPException(401, "Invalid credentials")
        
        # Create token
        logger.debug(f"Creating JWT token for user: {user.email}")
        token = create_token(str(db_user["_id"]), db_user.get("role", "user"))
        logger.debug(f"JWT token created for user: {user.email}")
        
        # Set cookie
        logger.debug(f"Setting authentication cookie for user: {user.email}")
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=3600,
            path="/",
        )
        logger.info(f"Login successful for user: {user.email}, Role: {db_user.get('role', 'user')}")
        
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
        logger.error(f"Login error for {user.email}: {str(e)}", exc_info=True)
        raise HTTPException(500, f"Login failed: {str(e)}")

@router.post("/logout")
async def logout(response: Response):
    try:
        logger.info("Logout request received")
        response.delete_cookie(
            "access_token",
            path="/",
            samesite="lax"
        )
        logger.info("User logged out successfully")
        return {"message": "Logged out successfully","status":200,"ok":True}
    except Exception as e:
        logger.error(f"Logout error: {str(e)}", exc_info=True)
        raise HTTPException(500, f"Logout failed: {str(e)}")

@router.get("/me")
async def get_current_user(request: Request):
    try:
        token = request.cookies.get("access_token")
        if not token:
            logger.warning("Get current user failed - no token provided")
            raise HTTPException(401, "Not authenticated")
        
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        user_id = payload.get("sub")
        if not user_id:
            logger.warning("Get current user failed - invalid token payload")
            raise HTTPException(401, "Invalid token")
        
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            logger.warning(f"Get current user failed - user not found: {user_id}")
            raise HTTPException(401, "User not found")
        
        logger.debug(f"Retrieved current user: {user['email']}")
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
        logger.error(f"Get current user error: {str(e)}", exc_info=True)
        raise HTTPException(401, "Invalid token")


@router.post("/forgot-password")
async def forgot_password(request_data: ForgotPasswordRequest):
    try:
        logger.info(f"Forgot password request for email: {request_data.email}")
        
        # Check if user exists
        user = await db.users.find_one({"email": request_data.email})
        if not user:
            # Don't reveal if email exists (security best practice)
            logger.warning(f"Forgot password request for non-existent email: {request_data.email}")
            return {"message": "If email exists, OTP has been sent"}
        
        # Generate and send OTP
        otp = await send_otp_email(request_data.email)
        logger.info(f"OTP sent successfully to {request_data.email}")
        
        return {
            "message": "OTP sent to your email",
            "otp": otp  # For testing only - remove in production
        }
    except Exception as e:
        logger.error(f"Forgot password error for {request_data.email}: {str(e)}", exc_info=True)
        raise HTTPException(500, f"Error processing request: {str(e)}")

@router.post("/verify-otp")
async def verify_otp_endpoint(request_data: VerifyOTPRequest):
    try:
        logger.info(f"OTP verification request for email: {request_data.email}")
        
        # Verify OTP
        is_valid = await verify_otp(request_data.email, request_data.otp)
        if not is_valid:
            logger.warning(f"Invalid or expired OTP for: {request_data.email}")
            raise HTTPException(400, "Invalid or expired OTP")
        
        logger.info(f"OTP verified successfully for: {request_data.email}")
        return {"message": "OTP verified successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"OTP verification error for {request_data.email}: {str(e)}", exc_info=True)
        raise HTTPException(500, f"Error verifying OTP: {str(e)}")

@router.post("/reset-password")
async def reset_password(request_data: ResetPasswordRequest):
    try:
        logger.info(f"Password reset request for email: {request_data.email}")
        
        # Verify OTP first
        is_valid = await verify_otp(request_data.email, request_data.otp)
        if not is_valid:
            logger.warning(f"Invalid or expired OTP for password reset: {request_data.email}")
            raise HTTPException(400, "Invalid or expired OTP")
        
        # Find user
        user = await db.users.find_one({"email": request_data.email})
        if not user:
            logger.warning(f"User not found for password reset: {request_data.email}")
            raise HTTPException(404, "User not found")
        
        # Hash new password
        logger.debug(f"Hashing new password for user: {request_data.email}")
        hashed_password = hash_password(request_data.new_password)
        
        # Update password
        await db.users.update_one(
            {"_id": user["_id"]},
            {"$set": {"password": hashed_password}}
        )
        
        # Delete OTP after successful reset
        await delete_otp(request_data.email)
        
        logger.info(f"Password reset successful for: {request_data.email}")
        return {"message": "Password reset successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Password reset error for {request_data.email}: {str(e)}", exc_info=True)
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
        
        logger.info(f"Updating profile for user: {user_id}")
        
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
        
        logger.info(f"Profile updated successfully for user: {user_id}")
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
        logger.error(f"Profile update error: {str(e)}", exc_info=True)
        raise HTTPException(500, f"Error updating profile: {str(e)}")

@router.post("/change-password")
async def change_password(request_data: dict, request: Request):
    try:
        # Get current user
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(401, "Not authenticated")
        
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(401, "Invalid token")
        
        current_password = request_data.get("current_password")
        new_password = request_data.get("new_password")
        
        if not current_password or not new_password:
            raise HTTPException(400, "Missing required fields")
        
        if len(new_password) < 8:
            raise HTTPException(400, "Password must be at least 8 characters")
        
        # Find user
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(404, "User not found")
        
        # Verify current password
        if not verify_password(current_password, user["password"]):
            logger.warning(f"Password change failed - incorrect current password for user: {user_id}")
            raise HTTPException(401, "Current password is incorrect")
        
        # Hash new password
        logger.debug(f"Hashing new password for user: {user_id}")
        hashed_password = hash_password(new_password)
        
        # Update password
        await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"password": hashed_password}}
        )
        
        logger.info(f"Password changed successfully for user: {user_id}")
        return {"message": "Password changed successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Password change error: {str(e)}", exc_info=True)
        raise HTTPException(500, f"Error changing password: {str(e)}")
