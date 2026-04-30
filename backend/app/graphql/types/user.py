import strawberry
from typing import Optional, List
from datetime import datetime


@strawberry.type
class UserType:
    id: int
    username: str
    email: str
    is_admin: bool
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None


@strawberry.type
class UserProfile:
    user: UserType
    bio: Optional[str] = None
    avatar_url: Optional[str] = None


@strawberry.input
class UserUpdateInput:
    username: Optional[str] = None
    email: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None


@strawberry.input
class UserCreateInput:
    username: str
    email: str
    password: str
