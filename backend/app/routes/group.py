"""Group routes for user clubs and communities."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.group import GroupPrivacy, GroupRole
from app.services.group_service import GroupService


router = APIRouter(prefix="/groups", tags=["groups"])
group_service = GroupService()


class GroupCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    privacy: str = "public"


class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    privacy: Optional[str] = None


class MemberInvite(BaseModel):
    user_id: int


class MemberRoleUpdate(BaseModel):
    role: str


class CollectionCreate(BaseModel):
    name: str
    description: Optional[str] = None


class CollectionItemAdd(BaseModel):
    movie_id: int


class DiscussionCreate(BaseModel):
    title: str
    content: str


class DiscussionReplyCreate(BaseModel):
    content: str
