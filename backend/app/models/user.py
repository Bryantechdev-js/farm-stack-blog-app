from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=1000)

class UserResponse(BaseModel):
    id: str
    email: str
    role: str
    created_at: Optional[datetime] = None

class CommentCreate(BaseModel):
    content: str = Field(min_length=1, max_length=1000)

class CommentResponse(BaseModel):
    id: str
    post_id: str
    user_id: str
    user_email: str
    content: str
    created_at: datetime

class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=5000)

class PostResponse(BaseModel):
    id: str
    title: str
    content: str
    image: Optional[str] = None
    author_id: str
    author_email: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    likes_count: int = 0
    comments_count: int = 0
    bookmarks_count: int = 0