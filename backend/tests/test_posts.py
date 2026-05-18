"""
Comprehensive tests for posts endpoints.
Tests CRUD operations, comments, likes, and bookmarks.
"""

import pytest
from httpx import AsyncClient
from io import BytesIO
from datetime import datetime
from bson import ObjectId


@pytest.mark.asyncio
@pytest.mark.posts
class TestCreatePost:
    """Test post creation"""
    
    async def test_create_post_success(self, authenticated_client, test_db):
        """Test successful post creation"""
        # Create a test image file
        image_content = b"fake image content"
        
        response = await authenticated_client.post(
            "/posts/",
            data={
                "title": "Test Post",
                "content": "This is test content"
            },
            files={"image": ("test.jpg", BytesIO(image_content), "image/jpeg")}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Post"
        assert data["content"] == "This is test content"
        assert "id" in data
        assert data["likes_count"] == 0
        assert data["comments_count"] == 0
    
    async def test_create_post_no_auth(self, client):
        """Test post creation without authentication"""
        response = await client.post(
            "/posts/",
            data={
                "title": "Test Post",
                "content": "This is test content"
            },
            files={"image": ("test.jpg", BytesIO(b"content"), "image/jpeg")}
        )
        
        assert response.status_code == 401
    
    async def test_create_post_missing_fields(self, authenticated_client):
        """Test post creation with missing fields"""
        response = await authenticated_client.post(
            "/posts/",
            data={"title": "Test Post"},
            files={"image": ("test.jpg", BytesIO(b"content"), "image/jpeg")}
        )
        
        assert response.status_code == 422


@pytest.mark.asyncio
@pytest.mark.posts
class TestGetPosts:
    """Test getting posts"""
    
    async def test_get_posts_success(self, client, setup_test_post):
        """Test getting all posts"""
        response = await client.get("/posts/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert data[0]["title"] == setup_test_post["title"]
    
    async def test_get_posts_empty(self, client, test_db):
        """Test getting posts when none exist"""
        response = await client.get("/posts/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    async def test_get_single_post_success(self, client, setup_test_post):
        """Test getting a single post"""
        response = await client.get(f"/posts/{setup_test_post['_id']}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(setup_test_post["_id"])
        assert data["title"] == setup_test_post["title"]
    
    async def test_get_single_post_not_found(self, client):
        """Test getting non-existent post"""
        fake_id = ObjectId()
        response = await client.get(f"/posts/{fake_id}")
        
        assert response.status_code == 404


@pytest.mark.asyncio
@pytest.mark.posts
class TestUpdatePost:
    """Test post updates"""
    
    async def test_update_post_success(self, authenticated_client, setup_test_post, setup_test_user):
        """Test successful post update"""
        response = await authenticated_client.put(
            f"/posts/{setup_test_post['_id']}",
            data={
                "title": "Updated Title",
                "content": "Updated content"
            },
            files={"image": ("test.jpg", BytesIO(b"content"), "image/jpeg")}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["content"] == "Updated content"
    
    async def test_update_post_no_auth(self, client, setup_test_post):
        """Test post update without authentication"""
        response = await client.put(
            f"/posts/{setup_test_post['_id']}",
            data={
                "title": "Updated Title",
                "content": "Updated content"
            },
            files={"image": ("test.jpg", BytesIO(b"content"), "image/jpeg")}
        )
        
        assert response.status_code == 401
    
    async def test_update_post_not_owner(self, client, setup_test_post, test_db):
        """Test updating post by non-owner"""
        # Create another user
        other_user = {
            "_id": ObjectId(),
            "email": "other@example.com",
            "password": "hash",
            "role": "user",
            "created_at": datetime.utcnow()
        }
        await test_db.users.insert_one(other_user)
        
        # Create client for other user
        from app.core.security import create_token
        token = create_token(str(other_user["_id"]), "user")
        client.cookies.set("access_token", token)
        
        response = await client.put(
            f"/posts/{setup_test_post['_id']}",
            data={
                "title": "Updated Title",
                "content": "Updated content"
            },
            files={"image": ("test.jpg", BytesIO(b"content"), "image/jpeg")}
        )
        
        assert response.status_code == 403


@pytest.mark.asyncio
@pytest.mark.posts
class TestDeletePost:
    """Test post deletion"""
    
    async def test_delete_post_success(self, authenticated_client, setup_test_post, test_db):
        """Test successful post deletion"""
        response = await authenticated_client.delete(f"/posts/{setup_test_post['_id']}")
        
        assert response.status_code == 200
        assert "deleted" in response.json()["message"]
        
        # Verify post was deleted
        post = await test_db.posts.find_one({"_id": setup_test_post["_id"]})
        assert post is None
    
    async def test_delete_post_no_auth(self, client, setup_test_post):
        """Test post deletion without authentication"""
        response = await client.delete(f"/posts/{setup_test_post['_id']}")
        
        assert response.status_code == 401
    
    async def test_delete_post_not_found(self, authenticated_client):
        """Test deleting non-existent post"""
        fake_id = ObjectId()
        response = await authenticated_client.delete(f"/posts/{fake_id}")
        
        assert response.status_code == 404


@pytest.mark.asyncio
@pytest.mark.comments
class TestComments:
    """Test comment functionality"""
    
    async def test_add_comment_success(self, authenticated_client, setup_test_post, test_db):
        """Test adding a comment"""
        response = await authenticated_client.post(
            f"/posts/{setup_test_post['_id']}/comments",
            json={"content": "Great post!"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["content"] == "Great post!"
        assert "id" in data
        
        # Verify comment count increased
        post = await test_db.posts.find_one({"_id": setup_test_post["_id"]})
        assert post["comments_count"] == 1
    
    async def test_add_comment_no_auth(self, client, setup_test_post):
        """Test adding comment without authentication"""
        response = await client.post(
            f"/posts/{setup_test_post['_id']}/comments",
            json={"content": "Great post!"}
        )
        
        assert response.status_code == 401
    
    async def test_add_comment_empty_content(self, authenticated_client, setup_test_post):
        """Test adding comment with empty content"""
        response = await authenticated_client.post(
            f"/posts/{setup_test_post['_id']}/comments",
            json={"content": ""}
        )
        
        assert response.status_code == 400
    
    async def test_get_comments_success(self, client, setup_test_comment):
        """Test getting comments"""
        response = await client.get(f"/posts/{setup_test_comment['post_id']}/comments")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert data[0]["content"] == setup_test_comment["content"]
    
    async def test_delete_comment_success(self, authenticated_client, setup_test_comment, test_db):
        """Test deleting a comment"""
        response = await authenticated_client.delete(
            f"/posts/{setup_test_comment['post_id']}/comments/{setup_test_comment['_id']}"
        )
        
        assert response.status_code == 200
        
        # Verify comment was deleted
        comment = await test_db.comments.find_one({"_id": setup_test_comment["_id"]})
        assert comment is None


@pytest.mark.asyncio
@pytest.mark.posts
class TestLikes:
    """Test like functionality"""
    
    async def test_like_post_success(self, authenticated_client, setup_test_post, test_db):
        """Test liking a post"""
        response = await authenticated_client.post(f"/posts/{setup_test_post['_id']}/like")
        
        assert response.status_code == 200
        data = response.json()
        assert data["liked"] is True
        assert data["likes_count"] == 1
        
        # Verify like was added
        post = await test_db.posts.find_one({"_id": setup_test_post["_id"]})
        assert len(post["likes"]) == 1
    
    async def test_unlike_post(self, authenticated_client, setup_test_post, test_db):
        """Test unliking a post"""
        # First like
        await authenticated_client.post(f"/posts/{setup_test_post['_id']}/like")
        
        # Then unlike
        response = await authenticated_client.post(f"/posts/{setup_test_post['_id']}/like")
        
        assert response.status_code == 200
        data = response.json()
        assert data["liked"] is False
        assert data["likes_count"] == 0
    
    async def test_like_post_no_auth(self, client, setup_test_post):
        """Test liking without authentication"""
        response = await client.post(f"/posts/{setup_test_post['_id']}/like")
        
        assert response.status_code == 401


@pytest.mark.asyncio
@pytest.mark.posts
class TestBookmarks:
    """Test bookmark functionality"""
    
    async def test_bookmark_post_success(self, authenticated_client, setup_test_post, test_db):
        """Test bookmarking a post"""
        response = await authenticated_client.post(f"/posts/{setup_test_post['_id']}/bookmark")
        
        assert response.status_code == 200
        data = response.json()
        assert data["bookmarked"] is True
        assert data["bookmarks_count"] == 1
        
        # Verify bookmark was added
        post = await test_db.posts.find_one({"_id": setup_test_post["_id"]})
        assert len(post["bookmarks"]) == 1
    
    async def test_remove_bookmark(self, authenticated_client, setup_test_post):
        """Test removing a bookmark"""
        # First bookmark
        await authenticated_client.post(f"/posts/{setup_test_post['_id']}/bookmark")
        
        # Then remove
        response = await authenticated_client.post(f"/posts/{setup_test_post['_id']}/bookmark")
        
        assert response.status_code == 200
        data = response.json()
        assert data["bookmarked"] is False
        assert data["bookmarks_count"] == 0
    
    async def test_bookmark_post_no_auth(self, client, setup_test_post):
        """Test bookmarking without authentication"""
        response = await client.post(f"/posts/{setup_test_post['_id']}/bookmark")
        
        assert response.status_code == 401
