"""Group routes for user clubs and communities."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.dependencies import get_db, get_current_user
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


@router.post("")
async def create_group(data: GroupCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    privacy = GroupPrivacy.PUBLIC if data.privacy == "public" else GroupPrivacy.PRIVATE
    group = await group_service.create_group(db, current_user.tenant_id, data.name, data.slug, current_user.id, data.description, privacy)
    return {"id": group.id, "name": group.name, "slug": group.slug}


@router.get("")
async def get_groups(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    groups = await group_service.get_groups(db, current_user.tenant_id, current_user.id)
    return [{"id": g.id, "name": g.name, "slug": g.slug, "privacy": g.privacy.value, "member_count": g.member_count} for g in groups]


@router.get("/{group_id}")
async def get_group(group_id: int, db: AsyncSession = Depends(get_db)):
    group = await group_service.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return {"id": group.id, "name": group.name, "slug": group.slug, "description": group.description, "privacy": group.privacy.value, "member_count": group.member_count}


@router.post("/{group_id}/join")
async def join_group(group_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    member = await group_service.join_group(db, group_id, current_user.id, current_user.tenant_id)
    if not member:
        raise HTTPException(status_code=400, detail="Cannot join group")
    return {"message": "Joined group"}


@router.post("/{group_id}/invite")
async def invite_member(group_id: int, data: MemberInvite, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    member = await group_service.invite_member(db, group_id, data.user_id, current_user.id, current_user.tenant_id)
    if not member:
        raise HTTPException(status_code=400, detail="Cannot invite")
    return {"message": "Invitation sent"}
