"""
Comprehensive tests for admin endpoints.
Tests user management, post management, comments management, and analytics.
"""

import pytest
from httpx import AsyncClient
from datetime import datetime
from bson import ObjectId


@pytest.mark.asyncio
@pytest.mark.admin
class TestAdminUsers:
    """Test admin user management"""
    
    async def test_get_all_users_success(self, admin_client, setup_test_user, test_db):
        """Test getting all users as admin"""
        response = await admin_client.get("/admin/users")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    async def test_get_all_users_no_auth(self, client):
        """Test getting users without authentication"""
        response = await client.get("/admin/users")
        
        assert response.status_code == 401
    
    async def test_get_all_users_not_admin(self, authenticated_client):
        """Test getting users as non-admin"""
        response = await authenticated_client.get("/admin/users")
        
        assert response.status_code == 403
    
    async def test_update_user_role_success(self, admin_client, setup_test_user, test_db):
        """Test updating user role"""
        response = await admin_client.put(
            f"/admin/users/{setup_test_user['_id']}/role",
            json={"role": "admin"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["role"] == "admin"
        
        # Verify in database
        user = await test_db.users.find_one({"_id": setup_test_user["_id"]})
        assert user["role"] == "admin"
    
    async def test_update_user_role_invalid(self, admin_client, setup_test_user):
        """Test updating user role with invalid role"""
        response = await admin_client.put(
            f"/admin/users/{setup_test_user['_id']}/role",
            json={"role": "invalid"}
        )
        
        assert response.status_code == 400
    
    async def test_delete_user_success(self, admin_client, setup_test_user, test_db):
        """Test deleting a user"""
        response = await admin_client.delete(f"/admin/users/{setup_test_user['_id']}")
        
        assert response.status_code == 200
        
        # Verify user was deleted
        user = await test_db.users.find_one({"_id": setup_test_user["_id"]})
        assert user is None
    
    async def test_delete_user_not_found(self, admin_client):
        """Test deleting non-existent user"""
        fake_id = ObjectId()
        response = await admin_client.delete(f"/admin/users/{fake_id}")
        
        assert response.status_code == 404


@pytest.mark.asyncio
@pytest.mark.admin
class TestAdminPosts:
    """Test admin post management"""
    
    async def test_get_all_posts_success(self, admin_client, setup_test_post):
        """Test getting all posts as admin"""
        response = await admin_client.get("/admin/posts")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    async def test_get_all_posts_no_auth(self, client):
        """Test getting posts without authentication"""
        response = await client.get("/admin/posts")
        
        assert response.status_code == 401
    
    async def test_get_all_posts_not_admin(self, authenticated_client):
        """Test getting posts as non-admin"""
        response = await authenticated_client.get("/admin/posts")
        
        assert response.status_code == 403
    
    async def test_delete_post_success(self, admin_client, setup_test_post, test_db):
        """Test deleting a post as admin"""
        response = await admin_client.delete(f"/admin/posts/{setup_test_post['_id']}")
        
        assert response.status_code == 200
        
        # Verify post was deleted
        post = await test_db.posts.find_one({"_id": setup_test_post["_id"]})
        assert post is None
    
    async def test_delete_post_not_found(self, admin_client):
        """Test deleting non-existent post"""
        fake_id = ObjectId()
        response = await admin_client.delete(f"/admin/posts/{fake_id}")
        
        assert response.status_code == 404


@pytest.mark.asyncio
@pytest.mark.admin
class TestAdminComments:
    """Test admin comment management"""
    
    async def test_get_all_comments_success(self, admin_client, setup_test_comment):
        """Test getting all comments as admin"""
        response = await admin_client.get("/admin/comments")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    async def test_get_all_comments_no_auth(self, client):
        """Test getting comments without authentication"""
        response = await client.get("/admin/comments")
        
        assert response.status_code == 401
    
    async def test_get_all_comments_not_admin(self, authenticated_client):
        """Test getting comments as non-admin"""
        response = await authenticated_client.get("/admin/comments")
        
        assert response.status_code == 403
    
    async def test_delete_comment_success(self, admin_client, setup_test_comment, test_db):
        """Test deleting a comment as admin"""
        response = await admin_client.delete(f"/admin/comments/{setup_test_comment['_id']}")
        
        assert response.status_code == 200
        
        # Verify comment was deleted
        comment = await test_db.comments.find_one({"_id": setup_test_comment["_id"]})
        assert comment is None
    
    async def test_delete_comment_not_found(self, admin_client):
        """Test deleting non-existent comment"""
        fake_id = ObjectId()
        response = await admin_client.delete(f"/admin/comments/{fake_id}")
        
        assert response.status_code == 404


@pytest.mark.asyncio
@pytest.mark.admin
class TestAdminAnalytics:
    """Test admin analytics"""
    
    async def test_get_analytics_success(self, admin_client, setup_test_post, setup_test_comment):
        """Test getting analytics as admin"""
        response = await admin_client.get("/admin/analytics")
        
        assert response.status_code == 200
        data = response.json()
        assert "total_users" in data
        assert "total_posts" in data
        assert "total_comments" in data
        assert "total_likes" in data
        assert "total_bookmarks" in data
    
    async def test_get_analytics_no_auth(self, client):
        """Test getting analytics without authentication"""
        response = await client.get("/admin/analytics")
        
        assert response.status_code == 401
    
    async def test_get_analytics_not_admin(self, authenticated_client):
        """Test getting analytics as non-admin"""
        response = await authenticated_client.get("/admin/analytics")
        
        assert response.status_code == 403
