from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner: UserResponse

    class Config:
        from_attributes = True

class PostVoteResponse(BaseModel):
    Post: Post
    votes: int

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

    class Config:
        from_attributes = True

class VoteResponse(BaseModel):
    post_id: int
    user_id: int

class Token(BaseModel):
    access_token: str
    type: str

class TokenData(BaseModel):
    id: Optional[int] = None