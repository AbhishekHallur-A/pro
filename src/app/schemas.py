from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)


class UserRead(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Pagination(BaseModel):
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class PostCreate(BaseModel):
    author_id: int
    content: str = Field(min_length=1, max_length=1000)


class PostRead(BaseModel):
    id: int
    author_id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    author_id: int
    content: str = Field(min_length=1, max_length=1000)


class CommentRead(BaseModel):
    id: int
    post_id: int
    author_id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class LikeCreate(BaseModel):
    user_id: int


class LikeRead(BaseModel):
    id: int
    post_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class FollowRead(BaseModel):
    id: int
    follower_id: int
    following_id: int
    created_at: datetime

    class Config:
        from_attributes = True
