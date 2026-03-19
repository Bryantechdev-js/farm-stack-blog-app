from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request
from app.db.mongo import db
from bson import ObjectId
from datetime import datetime
import bleach
import os
import uuid
from jose import jwt, JWTError
from app.core.security import SECRET, ALGO

router = APIRouter(prefix="/posts")

# Helper to get current user from token
async def get_current_user(request: Request):
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
        return {"id": str(user["_id"]), "email": user["email"], "role": user.get("role", "user")}
    except JWTError:
        raise HTTPException(401, "Invalid token")

# Helper to ensure uploads directory exists
def ensure_uploads_dir():
    os.makedirs("uploads", exist_ok=True)

# Helper to save uploaded file
async def save_upload_file(file: UploadFile) -> str:
    ensure_uploads_dir()
    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = f"uploads/{unique_filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return file_path

@router.post("/")
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile = File(...),
    request: Request = None
):
    try:
        current_user = await get_current_user(request)
        safe_content = bleach.clean(content)
        image_path = await save_upload_file(image)
        
        result = await db.posts.insert_one({
            "title": title,
            "content": safe_content,
            "image": image_path,
            "author_id": ObjectId(current_user["id"]),
            "author_email": current_user["email"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "likes": [],
            "bookmarks": [],
            "comments_count": 0
        })
        post = await db.posts.find_one({"_id": result.inserted_id})
        return format_post(post)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Create post error: {e}")
        raise HTTPException(500, f"Error creating post: {str(e)}")

@router.get("/")
async def get_posts():
    try:
        posts = await db.posts.find().sort("created_at", -1).to_list(100)
        return [format_post(p) for p in posts]
    except Exception as e:
        print(f"Get posts error: {e}")
        raise HTTPException(500, f"Error fetching posts: {str(e)}")

@router.get("/{post_id}")
async def get_post(post_id: str):
    try:
        post = await db.posts.find_one({"_id": ObjectId(post_id)})
        if not post:
            raise HTTPException(404, "Post not found")
        return format_post(post)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Get post error: {e}")
        raise HTTPException(400, "Invalid post ID")

@router.put("/{post_id}")
async def update_post(
    post_id: str,
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile = File(None),
    request: Request = None
):
    try:
        current_user = await get_current_user(request)
        post = await db.posts.find_one({"_id": ObjectId(post_id)})
        
        if not post:
            raise HTTPException(404, "Post not found")
        
        if str(post["author_id"]) != current_user["id"] and current_user["role"] != "admin":
            raise HTTPException(403, "Not authorized to update this post")
        
        safe_content = bleach.clean(content)
        image_path = post["image"]
        
        if image:
            image_path = await save_upload_file(image)
        
        await db.posts.update_one(
            {"_id": ObjectId(post_id)},
            {"$set": {
                "title": title,
                "content": safe_content,
                "image": image_path,
                "updated_at": datetime.utcnow()
            }}
        )
        
        updated_post = await db.posts.find_one({"_id": ObjectId(post_id)})
        return format_post(updated_post)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Update post error: {e}")
        raise HTTPException(500, f"Error updating post: {str(e)}")

@router.delete("/{post_id}")
async def delete_post(post_id: str, request: Request = None):
    try:
        current_user = await get_current_user(request)
        post = await db.posts.find_one({"_id": ObjectId(post_id)})
        
        if not post:
            raise HTTPException(404, "Post not found")
        
        if str(post["author_id"]) != current_user["id"] and current_user["role"] != "admin":
            raise HTTPException(403, "Not authorized to delete this post")
        
        await db.posts.delete_one({"_id": ObjectId(post_id)})
        await db.comments.delete_many({"post_id": ObjectId(post_id)})
        
        return {"message": "Post deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Delete post error: {e}")
        raise HTTPException(500, f"Error deleting post: {str(e)}")

# Comments endpoints
@router.post("/{post_id}/comments")
async def add_comment(post_id: str, request: Request):
    try:
        current_user = await get_current_user(request)
        post = await db.posts.find_one({"_id": ObjectId(post_id)})
        
        if not post:
            raise HTTPException(404, "Post not found")
        
        body = await request.json()
        content = body.get("content", "").strip()
        
        if not content:
            raise HTTPException(400, "Comment content is required")
        
        safe_content = bleach.clean(content)
        result = await db.comments.insert_one({
            "post_id": ObjectId(post_id),
            "user_id": ObjectId(current_user["id"]),
            "user_email": current_user["email"],
            "content": safe_content,
            "created_at": datetime.utcnow()
        })
        
        await db.posts.update_one(
            {"_id": ObjectId(post_id)},
            {"$inc": {"comments_count": 1}}
        )
        
        comment = await db.comments.find_one({"_id": result.inserted_id})
        return format_comment(comment)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Add comment error: {e}")
        raise HTTPException(500, f"Error adding comment: {str(e)}")

@router.get("/{post_id}/comments")
async def get_comments(post_id: str):
    try:
        comments = await db.comments.find({"post_id": ObjectId(post_id)}).sort("created_at", -1).to_list(100)
        return [format_comment(c) for c in comments]
    except Exception as e:
        print(f"Get comments error: {e}")
        raise HTTPException(500, f"Error fetching comments: {str(e)}")

@router.delete("/{post_id}/comments/{comment_id}")
async def delete_comment(post_id: str, comment_id: str, request: Request = None):
    try:
        current_user = await get_current_user(request)
        comment = await db.comments.find_one({"_id": ObjectId(comment_id)})
        
        if not comment:
            raise HTTPException(404, "Comment not found")
        
        if str(comment["user_id"]) != current_user["id"] and current_user["role"] != "admin":
            raise HTTPException(403, "Not authorized to delete this comment")
        
        await db.comments.delete_one({"_id": ObjectId(comment_id)})
        await db.posts.update_one(
            {"_id": ObjectId(post_id)},
            {"$inc": {"comments_count": -1}}
        )
        
        return {"message": "Comment deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Delete comment error: {e}")
        raise HTTPException(500, f"Error deleting comment: {str(e)}")

# Likes endpoints
@router.post("/{post_id}/like")
async def like_post(post_id: str, request: Request = None):
    try:
        current_user = await get_current_user(request)
        post = await db.posts.find_one({"_id": ObjectId(post_id)})
        
        if not post:
            raise HTTPException(404, "Post not found")
        
        user_id = ObjectId(current_user["id"])
        if user_id in post.get("likes", []):
            await db.posts.update_one(
                {"_id": ObjectId(post_id)},
                {"$pull": {"likes": user_id}}
            )
            liked = False
        else:
            await db.posts.update_one(
                {"_id": ObjectId(post_id)},
                {"$push": {"likes": user_id}}
            )
            liked = True
        
        updated_post = await db.posts.find_one({"_id": ObjectId(post_id)})
        return {"liked": liked, "likes_count": len(updated_post.get("likes", []))}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Like post error: {e}")
        raise HTTPException(500, f"Error liking post: {str(e)}")

# Bookmarks endpoints
@router.post("/{post_id}/bookmark")
async def bookmark_post(post_id: str, request: Request = None):
    try:
        current_user = await get_current_user(request)
        post = await db.posts.find_one({"_id": ObjectId(post_id)})
        
        if not post:
            raise HTTPException(404, "Post not found")
        
        user_id = ObjectId(current_user["id"])
        if user_id in post.get("bookmarks", []):
            await db.posts.update_one(
                {"_id": ObjectId(post_id)},
                {"$pull": {"bookmarks": user_id}}
            )
            bookmarked = False
        else:
            await db.posts.update_one(
                {"_id": ObjectId(post_id)},
                {"$push": {"bookmarks": user_id}}
            )
            bookmarked = True
        
        updated_post = await db.posts.find_one({"_id": ObjectId(post_id)})
        return {"bookmarked": bookmarked, "bookmarks_count": len(updated_post.get("bookmarks", []))}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Bookmark post error: {e}")
        raise HTTPException(500, f"Error bookmarking post: {str(e)}")

# Helper functions
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