from fastapi import APIRouter, HTTPException, Request
from app.db.mongo import db
from bson import ObjectId
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.security import SECRET, ALGO

router = APIRouter(prefix="/admin")

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

@router.get("/analytics/advanced")
async def get_advanced_analytics(request: Request = None):
    try:
        await get_admin_user(request)
        
        # Get all posts with engagement data
        posts = await db.posts.find().to_list(10000)
        
        # Post engagement breakdown
        engagement_by_post = []
        for post in posts[:10]:  # Top 10 posts
            engagement_by_post.append({
                "title": post.get("title", "Untitled")[:25],
                "likes": len(post.get("likes", [])),
                "comments": post.get("comments_count", 0),
                "bookmarks": len(post.get("bookmarks", []))
            })
        
        # Active users trend (last 30 days)
        active_users_trend = []
        for i in range(30, 0, -1):
            date = datetime.utcnow() - timedelta(days=i)
            date_str = date.strftime("%m-%d")
            
            # Count users who created posts on this day
            count = await db.posts.count_documents({
                "created_at": {
                    "$gte": date.replace(hour=0, minute=0, second=0, microsecond=0),
                    "$lt": date.replace(hour=23, minute=59, second=59, microsecond=999999)
                }
            })
            
            active_users_trend.append({
                "date": date_str,
                "count": count
            })
        
        # Post rate trend (last 30 days)
        post_rate_trend = []
        for i in range(30, 0, -1):
            date = datetime.utcnow() - timedelta(days=i)
            date_str = date.strftime("%m-%d")
            
            # Count posts created on this day
            count = await db.posts.count_documents({
                "created_at": {
                    "$gte": date.replace(hour=0, minute=0, second=0, microsecond=0),
                    "$lt": date.replace(hour=23, minute=59, second=59, microsecond=999999)
                }
            })
            
            post_rate_trend.append({
                "date": date_str,
                "count": count
            })
        
        # Get basic stats
        total_users = await db.users.count_documents({})
        total_posts = await db.posts.count_documents({})
        total_comments = await db.comments.count_documents({})
        
        total_likes = sum(len(post.get("likes", [])) for post in posts)
        total_bookmarks = sum(len(post.get("bookmarks", [])) for post in posts)
        
        return {
            "total_users": total_users,
            "total_posts": total_posts,
            "total_comments": total_comments,
            "total_likes": total_likes,
            "total_bookmarks": total_bookmarks,
            "engagement_by_post": engagement_by_post,
            "active_users_trend": active_users_trend,
            "post_rate_trend": post_rate_trend
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Get advanced analytics error: {e}")
        raise HTTPException(500, f"Error fetching analytics: {str(e)}")
