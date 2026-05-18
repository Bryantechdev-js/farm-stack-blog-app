"""
Pytest configuration and fixtures for the blog application.
Provides test database, client, and authentication fixtures.
"""

import pytest
import asyncio
import os
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from datetime import datetime
from bson import ObjectId

# Load environment variables
load_dotenv()


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client():
    """Create async test client"""
    # Import here to avoid connection during collection
    from app.main import app
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def test_db():
    """
    Connect to test MongoDB database.
    Uses separate test database to avoid affecting production data.
    """
    test_db_url = os.getenv("MONGO_URL_TEST", "mongodb://localhost:27017/blog_test")
    client = AsyncIOMotorClient(test_db_url)
    test_db = client.blog_test
    
    # Clear all collections before test
    await test_db.users.delete_many({})
    await test_db.posts.delete_many({})
    await test_db.comments.delete_many({})
    await test_db.otp_tokens.delete_many({})
    
    yield test_db
    
    # Cleanup: drop test database after tests
    await client.drop_database("blog_test")
    client.close()


@pytest.fixture
async def setup_test_user(test_db):
    """Create a test user in the database"""
    from app.core.security import hash_password
    
    user_data = {
        "_id": ObjectId(),
        "email": "test@example.com",
        "password": hash_password("TestPassword123"),
        "role": "user",
        "full_name": "Test User",
        "bio": "Test bio",
        "avatar_url": "https://example.com/avatar.jpg",
        "created_at": datetime.utcnow()
    }
    result = await test_db.users.insert_one(user_data)
    user_data["_id"] = result.inserted_id
    return user_data


@pytest.fixture
async def setup_admin_user(test_db):
    """Create a test admin user in the database"""
    from app.core.security import hash_password
    
    admin_data = {
        "_id": ObjectId(),
        "email": "admin@example.com",
        "password": hash_password("AdminPassword123"),
        "role": "admin",
        "full_name": "Admin User",
        "bio": "Admin bio",
        "avatar_url": "https://example.com/admin.jpg",
        "created_at": datetime.utcnow()
    }
    result = await test_db.users.insert_one(admin_data)
    admin_data["_id"] = result.inserted_id
    return admin_data


@pytest.fixture
async def auth_token(setup_test_user):
    """Generate JWT token for test user"""
    from app.core.security import create_token
    
    user_id = str(setup_test_user["_id"])
    token = create_token(user_id, "user")
    return token


@pytest.fixture
async def admin_token(setup_admin_user):
    """Generate JWT token for admin user"""
    from app.core.security import create_token
    
    user_id = str(setup_admin_user["_id"])
    token = create_token(user_id, "admin")
    return token


@pytest.fixture
async def authenticated_client(client, auth_token):
    """Create authenticated test client with user token"""
    client.cookies.set("access_token", auth_token)
    return client


@pytest.fixture
async def admin_client(client, admin_token):
    """Create authenticated test client with admin token"""
    client.cookies.set("access_token", admin_token)
    return client


@pytest.fixture
async def setup_test_post(test_db, setup_test_user):
    """Create a test post in the database"""
    post_data = {
        "_id": ObjectId(),
        "title": "Test Post",
        "content": "This is a test post content",
        "image": "/uploads/test-image.jpg",
        "author_id": setup_test_user["_id"],
        "author_email": setup_test_user["email"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "likes": [],
        "bookmarks": [],
        "comments_count": 0
    }
    result = await test_db.posts.insert_one(post_data)
    post_data["_id"] = result.inserted_id
    return post_data


@pytest.fixture
async def setup_test_comment(test_db, setup_test_post, setup_test_user):
    """Create a test comment in the database"""
    comment_data = {
        "_id": ObjectId(),
        "post_id": setup_test_post["_id"],
        "user_id": setup_test_user["_id"],
        "user_email": setup_test_user["email"],
        "content": "This is a test comment",
        "created_at": datetime.utcnow()
    }
    result = await test_db.comments.insert_one(comment_data)
    comment_data["_id"] = result.inserted_id
    return comment_data


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "asyncio: mark test as async"
    )
    config.addinivalue_line(
        "markers", "auth: mark test as authentication related"
    )
    config.addinivalue_line(
        "markers", "posts: mark test as posts related"
    )
    config.addinivalue_line(
        "markers", "comments: mark test as comments related"
    )
    config.addinivalue_line(
        "markers", "admin: mark test as admin related"
    )
