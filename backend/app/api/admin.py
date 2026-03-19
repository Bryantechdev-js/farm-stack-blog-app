from fastapi import APIRouter, HTTPException, Request
from app.db.mongo import db
from bson import ObjectId
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.security import SECRET, ALGO

router = APIRouter(prefix="/admin")

# Helper to get current user and verify admin role
async def get_admin_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(401, "Not authenticated")
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(401, "Invalid token")
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(401, "User not found")
        if user.get("role") != "admin":
            raise HTTPException(403, "Admin access required")
        return {"id": str(user["_id"]), "email": user["email"], "role": user.get("role")}
    except JWTError:
        raise HTTPException(401, "Invalid token")

# Users management
@router.get("/users")
async def get_all_users(request: Request = None):
    try:
        await get_admin_user(request)
        users = await db.users.find().to_list(1000)
        return [format_user(u) for u in users]
    except HTTPException:
        raise
    except Exception as e:
        print(f"Get users error: {e}")
        raise HTTPException(500, f"Error fetching users: {str(e)}")

@router.put("/users/{user_id}/role")
async def update_user_role(user_id: str, role: dict, request: Request = None):
    try:
        admin_user = await get_admin_user(request)
        
        if role.get("role") not in ["user", "admin"]:
            raise HTTPException(400, "Invalid role")
        
        # Prevent removing the last admin
        if role.get("role") == "user":
            admin_count = await db.users.count_documents({"role": "admin"})
            if admin_count <= 1:
                raise HTTPException(400, "Cannot remove the last admin. Promote another user to admin first.")
        
        result = await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"role": role.get("role")}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(404, "User not found")
        
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        return format_user(user)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Update user role error: {e}")
        raise HTTPException(500, f"Error updating user: {str(e)}")

@router.delete("/users/{user_id}")
async def delete_user(user_id: str, request: Request = None):
    try:
        await get_admin_user(request)
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        
        if not user:
            raise HTTPException(404, "User not found")
        
        # Delete user's posts and related data
        await db.posts.delete_many({"author_id": ObjectId(user_id)})
        await db.comments.delete_many({"user_id": ObjectId(user_id)})
        await db.users.delete_one({"_id": ObjectId(user_id)})
        
        return {"message": "User deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Delete user error: {e}")
        raise HTTPException(500, f"Error deleting user: {str(e)}")

# Posts management
@router.get("/posts")
async def get_all_posts(request: Request = None):
    try:
        await get_admin_user(request)
        posts = await db.posts.find().sort("created_at", -1).to_list(1000)
        return [format_post(p) for p in posts]
    except HTTPException:
        raise
    except Exception as e:
        print(f"Get posts error: {e}")
        raise HTTPException(500, f"Error fetching posts: {str(e)}")

@router.delete("/posts/{post_id}")
async def delete_post_admin(post_id: str, request: Request = None):
    try:
        await get_admin_user(request)
        post = await db.posts.find_one({"_id": ObjectId(post_id)})
        
        if not post:
            raise HTTPException(404, "Post not found")
        
        await db.posts.delete_one({"_id": ObjectId(post_id)})
        await db.comments.delete_many({"post_id": ObjectId(post_id)})
        
        return {"message": "Post deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Delete post error: {e}")
        raise HTTPException(500, f"Error deleting post: {str(e)}")

# Comments management
@router.get("/comments")
async def get_all_comments(request: Request = None):
    try:
        await get_admin_user(request)
        comments = await db.comments.find().sort("created_at", -1).to_list(1000)
        return [format_comment(c) for c in comments]
    except HTTPException:
        raise
    except Exception as e:
        print(f"Get comments error: {e}")
        raise HTTPException(500, f"Error fetching comments: {str(e)}")

@router.delete("/comments/{comment_id}")
async def delete_comment_admin(comment_id: str, request: Request = None):
    try:
        await get_admin_user(request)
        comment = await db.comments.find_one({"_id": ObjectId(comment_id)})
        
        if not comment:
            raise HTTPException(404, "Comment not found")
        
        await db.comments.delete_one({"_id": ObjectId(comment_id)})
        await db.posts.update_one(
            {"_id": comment["post_id"]},
            {"$inc": {"comments_count": -1}}
        )
        
        return {"message": "Comment deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Delete comment error: {e}")
        raise HTTPException(500, f"Error deleting comment: {str(e)}")

# Analytics
@router.get("/analytics")
async def get_analytics(request: Request = None):
    try:
        await get_admin_user(request)
        
        # Get counts
        total_users = await db.users.count_documents({})
        total_posts = await db.posts.count_documents({})
        total_comments = await db.comments.count_documents({})
        
        # Get posts by date (last 7 days)
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        posts_last_7_days = await db.posts.count_documents({"created_at": {"$gte": seven_days_ago}})
        
        # Get top posts by likes
        top_posts = await db.posts.find().sort("likes", -1).limit(5).to_list(5)
        
        # Get most active users
        pipeline = [
            {"$group": {"_id": "$author_id", "post_count": {"$sum": 1}}},
            {"$sort": {"post_count": -1}},
            {"$limit": 5}
        ]
        top_authors = await db.posts.aggregate(pipeline).to_list(5)
        
        # Get engagement stats
        total_likes = 0
        total_bookmarks = 0
        for post in await db.posts.find().to_list(1000):
            total_likes += len(post.get("likes", []))
            total_bookmarks += len(post.get("bookmarks", []))
        
        return {
            "total_users": total_users,
            "total_posts": total_posts,
            "total_comments": total_comments,
            "posts_last_7_days": posts_last_7_days,
            "total_likes": total_likes,
            "total_bookmarks": total_bookmarks,
            "top_posts": [format_post(p) for p in top_posts],
            "top_authors": top_authors
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Get analytics error: {e}")
        raise HTTPException(500, f"Error fetching analytics: {str(e)}")

# Helper functions
def format_user(user):
    return {
        "id": str(user["_id"]),
        "email": user.get("email"),
        "role": user.get("role", "user"),
        "created_at": user.get("created_at")
    }

def format_post(post):
    return {
        "id": str(post["_id"]),
        "title": post.get("title"),
        "content": post.get("content"),
        "image": post.get("image"),
        "author_id": str(post.get("author_id")),
        "author_email": post.get("author_email"),
        "created_at": post.get("created_at"),
        "updated_at": post.get("updated_at"),
        "likes_count": len(post.get("likes", [])),
        "comments_count": post.get("comments_count", 0),
        "bookmarks_count": len(post.get("bookmarks", []))
    }

def format_comment(comment):
    return {
        "id": str(comment["_id"]),
        "post_id": str(comment["post_id"]),
        "user_id": str(comment["user_id"]),
        "user_email": comment.get("user_email"),
        "content": comment.get("content"),
        "created_at": comment.get("created_at")
    }
