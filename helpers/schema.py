from typing import Literal
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Union
from uuid import UUID
from datetime import datetime

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

class RegisterDublicateSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    detail: str
    error_code: str
    status_code: int

class LoginSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    access_token: str = Field(
        pattern=r"^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$"
    )
    refresh_token: str
    token_type: Literal["bearer"]

class FailedLoginSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
    detail: str
    error_code: str
    status_code: int

class ValidationErrorItem(BaseModel):

    loc: List[Union[str, int]]
    msg: str
    type: str



class HTTPValidationError(BaseModel):
    detail: List[ValidationErrorItem]

