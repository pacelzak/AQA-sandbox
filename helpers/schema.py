from pydantic import BaseModel, ConfigDict , Field, EmailStr
from typing import Literal
from datetime import datetime
from uuid import UUID

class RegisterSchema(BaseModel):

    model_config = ConfigDict(extra="forbid")

    id: UUID
    email: EmailStr
    username: str
    display_name: str
    bio: str|None
    avatar_url: str|None
    cover_url: str|None
    role: str|None
    is_active: bool
    is_verified: bool
    is_private: bool
    created_at: datetime
    updated_at: datetime
    followers_count: int
    following_count: int
    posts_count: int
    is_following: bool
    is_followed_by: bool