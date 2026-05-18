"""
Comprehensive tests for authentication endpoints.
Tests signup, login, logout, profile management, and password reset.
"""

import pytest
from httpx import AsyncClient
from datetime import datetime
from bson import ObjectId


@pytest.mark.asyncio
@pytest.mark.auth
class TestSignup:
    """Test user signup functionality"""
    
    async def test_signup_success(self, client, test_db):
        """Test successful user signup"""
        response = await client.post(
            "/auth/signup",
            json={
                "email": "newuser@example.com",
                "password": "SecurePassword123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "User created successfully"
        assert "user_id" in data
        assert "is_admin" in data
        
        # Verify user was created in database
        user = await test_db.users.find_one({"email": "newuser@example.com"})
        assert user is not None
        assert user["email"] == "newuser@example.com"
    
    async def test_signup_first_user_becomes_admin(self, client, test_db):
        """Test that first user becomes admin"""
        response = await client.post(
            "/auth/signup",
            json={
                "email": "firstuser@example.com",
                "password": "SecurePassword123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_admin"] is True
        
        # Verify user role is admin
        user = await test_db.users.find_one({"email": "firstuser@example.com"})
        assert user["role"] == "admin"
    
    async def test_signup_duplicate_email(self, client, setup_test_user):
        """Test signup with duplicate email fails"""
        response = await client.post(
            "/auth/signup",
            json={
                "email": setup_test_user["email"],
                "password": "SecurePassword123"
            }
        )
        
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]
    
    async def test_signup_invalid_email(self, client):
        """Test signup with invalid email"""
        response = await client.post(
            "/auth/signup",
            json={
                "email": "invalid-email",
                "password": "SecurePassword123"
            }
        )
        
        assert response.status_code == 422  # Validation error
    
    async def test_signup_weak_password(self, client):
        """Test signup with weak password"""
        response = await client.post(
            "/auth/signup",
            json={
                "email": "user@example.com",
                "password": "weak"
            }
        )
        
        assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
@pytest.mark.auth
class TestLogin:
    """Test user login functionality"""
    
    async def test_login_success(self, client, setup_test_user):
        """Test successful login"""
        response = await client.post(
            "/auth/login",
            json={
                "email": setup_test_user["email"],
                "password": "TestPassword123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Login successful"
        assert data["user"]["email"] == setup_test_user["email"]
        assert data["user"]["role"] == "user"
        
        # Verify cookie was set
        assert "access_token" in client.cookies
    
    async def test_login_invalid_email(self, client):
        """Test login with non-existent email"""
        response = await client.post(
            "/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "SomePassword123"
            }
        )
        
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]
    
    async def test_login_invalid_password(self, client, setup_test_user):
        """Test login with wrong password"""
        response = await client.post(
            "/auth/login",
            json={
                "email": setup_test_user["email"],
                "password": "WrongPassword123"
            }
        )
        
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]
    
    async def test_login_admin_user(self, client, setup_admin_user):
        """Test admin user login"""
        response = await client.post(
            "/auth/login",
            json={
                "email": setup_admin_user["email"],
                "password": "AdminPassword123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["role"] == "admin"


@pytest.mark.asyncio
@pytest.mark.auth
class TestLogout:
    """Test user logout functionality"""
    
    async def test_logout_success(self, authenticated_client):
        """Test successful logout"""
        response = await authenticated_client.post("/auth/logout")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Logged out successfully"
        
        # Verify cookie was deleted
        assert "access_token" not in authenticated_client.cookies
    
    async def test_logout_without_auth(self, client):
        """Test logout without authentication"""
        response = await client.post("/auth/logout")
        
        # Logout should succeed even without auth
        assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.auth
class TestGetCurrentUser:
    """Test get current user endpoint"""
    
    async def test_get_current_user_success(self, authenticated_client, setup_test_user):
        """Test getting current user info"""
        response = await authenticated_client.get("/auth/me")
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == setup_test_user["email"]
        assert data["role"] == "user"
        assert data["full_name"] == setup_test_user["full_name"]
    
    async def test_get_current_user_no_auth(self, client):
        """Test get current user without authentication"""
        response = await client.get("/auth/me")
        
        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]
    
    async def test_get_current_user_invalid_token(self, client):
        """Test get current user with invalid token"""
        client.cookies.set("access_token", "invalid-token")
        response = await client.get("/auth/me")
        
        assert response.status_code == 401


@pytest.mark.asyncio
@pytest.mark.auth
class TestUpdateProfile:
    """Test profile update functionality"""
    
    async def test_update_profile_success(self, authenticated_client, setup_test_user, test_db):
        """Test successful profile update"""
        response = await authenticated_client.put(
            "/auth/profile",
            json={
                "full_name": "Updated Name",
                "bio": "Updated bio",
                "avatar_url": "https://example.com/new-avatar.jpg"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Updated Name"
        assert data["bio"] == "Updated bio"
        assert data["avatar_url"] == "https://example.com/new-avatar.jpg"
        
        # Verify update in database
        user = await test_db.users.find_one({"email": setup_test_user["email"]})
        assert user["full_name"] == "Updated Name"
    
    async def test_update_profile_partial(self, authenticated_client, setup_test_user):
        """Test partial profile update"""
        response = await authenticated_client.put(
            "/auth/profile",
            json={
                "full_name": "New Name"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "New Name"
    
    async def test_update_profile_no_auth(self, client):
        """Test profile update without authentication"""
        response = await client.put(
            "/auth/profile",
            json={"full_name": "New Name"}
        )
        
        assert response.status_code == 401
    
    async def test_update_profile_no_fields(self, authenticated_client):
        """Test profile update with no fields"""
        response = await authenticated_client.put(
            "/auth/profile",
            json={}
        )
        
        assert response.status_code == 400


@pytest.mark.asyncio
@pytest.mark.auth
class TestChangePassword:
    """Test password change functionality"""
    
    async def test_change_password_success(self, authenticated_client, setup_test_user, test_db):
        """Test successful password change"""
        response = await authenticated_client.post(
            "/auth/change-password",
            json={
                "current_password": "TestPassword123",
                "new_password": "NewPassword123"
            }
        )
        
        assert response.status_code == 200
        assert response.json()["message"] == "Password changed successfully"
        
        # Verify new password works
        login_response = await authenticated_client.post(
            "/auth/login",
            json={
                "email": setup_test_user["email"],
                "password": "NewPassword123"
            }
        )
        assert login_response.status_code == 200
    
    async def test_change_password_wrong_current(self, authenticated_client):
        """Test password change with wrong current password"""
        response = await authenticated_client.post(
            "/auth/change-password",
            json={
                "current_password": "WrongPassword123",
                "new_password": "NewPassword123"
            }
        )
        
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"]
    
    async def test_change_password_weak_new(self, authenticated_client):
        """Test password change with weak new password"""
        response = await authenticated_client.post(
            "/auth/change-password",
            json={
                "current_password": "TestPassword123",
                "new_password": "weak"
            }
        )
        
        assert response.status_code == 400
    
    async def test_change_password_no_auth(self, client):
        """Test password change without authentication"""
        response = await client.post(
            "/auth/change-password",
            json={
                "current_password": "TestPassword123",
                "new_password": "NewPassword123"
            }
        )
        
        assert response.status_code == 401


@pytest.mark.asyncio
@pytest.mark.auth
class TestForgotPassword:
    """Test forgot password functionality"""
    
    async def test_forgot_password_success(self, client, setup_test_user, test_db):
        """Test forgot password request"""
        response = await client.post(
            "/auth/forgot-password",
            json={"email": setup_test_user["email"]}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "OTP" in data["message"]
        assert "otp" in data  # For testing
        
        # Verify OTP was stored
        otp_record = await test_db.otp_tokens.find_one({"email": setup_test_user["email"]})
        assert otp_record is not None
    
    async def test_forgot_password_nonexistent_email(self, client):
        """Test forgot password with non-existent email"""
        response = await client.post(
            "/auth/forgot-password",
            json={"email": "nonexistent@example.com"}
        )
        
        # Should not reveal if email exists
        assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.auth
class TestVerifyOTP:
    """Test OTP verification"""
    
    async def test_verify_otp_success(self, client, setup_test_user, test_db):
        """Test successful OTP verification"""
        # First generate OTP
        from app.core.email import send_otp_email
        otp = await send_otp_email(setup_test_user["email"])
        
        # Then verify it
        response = await client.post(
            "/auth/verify-otp",
            json={
                "email": setup_test_user["email"],
                "otp": otp
            }
        )
        
        assert response.status_code == 200
        assert "verified" in response.json()["message"]
    
    async def test_verify_otp_invalid(self, client, setup_test_user):
        """Test OTP verification with invalid OTP"""
        response = await client.post(
            "/auth/verify-otp",
            json={
                "email": setup_test_user["email"],
                "otp": "000000"
            }
        )
        
        assert response.status_code == 400


@pytest.mark.asyncio
@pytest.mark.auth
class TestResetPassword:
    """Test password reset with OTP"""
    
    async def test_reset_password_success(self, client, setup_test_user, test_db):
        """Test successful password reset"""
        # Generate OTP
        from app.core.email import send_otp_email
        otp = await send_otp_email(setup_test_user["email"])
        
        # Reset password
        response = await client.post(
            "/auth/reset-password",
            json={
                "email": setup_test_user["email"],
                "otp": otp,
                "new_password": "ResetPassword123"
            }
        )
        
        assert response.status_code == 200
        assert "reset successfully" in response.json()["message"]
        
        # Verify OTP was deleted
        otp_record = await test_db.otp_tokens.find_one({"email": setup_test_user["email"]})
        assert otp_record is None
    
    async def test_reset_password_invalid_otp(self, client, setup_test_user):
        """Test password reset with invalid OTP"""
        response = await client.post(
            "/auth/reset-password",
            json={
                "email": setup_test_user["email"],
                "otp": "000000",
                "new_password": "ResetPassword123"
            }
        )
        
        assert response.status_code == 400
