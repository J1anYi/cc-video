"""Forum routes for community discussions."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.dependencies import get_db, get_current_user, get_current_user_optional
from app.models.user import User
from app.middleware.tenant import get_tenant_id
from app.services.forum_service import ForumService


router = APIRouter(prefix="/forums", tags=["forums"])


class ForumCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    category: str = "general"
    order: int = 0


class ThreadCreate(BaseModel):
    forum_id: int
    title: str
    content: str


class PostCreate(BaseModel):
    content: str


class ModerationAction(BaseModel):
    action: str
    target_type: str
    target_id: int
    reason: Optional[str] = None


@router.post("")
async def create_forum(
    data: ForumCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = ForumService(db)
    forum = await service.create_forum(
        tenant_id=tenant_id,
        name=data.name,
        slug=data.slug,
        description=data.description,
        category=data.category,
        order=data.order,
    )
    return {"id": forum.id, "name": forum.name, "slug": forum.slug}


@router.get("")
async def get_forums(
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
):
    service = ForumService(db)
    forums = await service.get_forums(tenant_id)
    return {"forums": [{"id": f.id, "name": f.name, "slug": f.slug, "description": f.description, "category": f.category, "thread_count": f.thread_count} for f in forums]}


@router.post("/threads")
async def create_thread(
    data: ThreadCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = ForumService(db)
    thread = await service.create_thread(
        forum_id=data.forum_id,
        author_id=current_user.id,
        tenant_id=tenant_id,
        title=data.title,
        content=data.content,
    )
    return {"id": thread.id, "title": thread.title}


@router.get("/threads/search")
async def search_threads(
    q: str = Query(..., min_length=2),
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
):
    service = ForumService(db)
    threads = await service.search_threads(tenant_id, q, skip, limit)
    return {"threads": [{"id": t.id, "title": t.title, "forum_id": t.forum_id, "reply_count": t.reply_count, "created_at": t.created_at.isoformat()} for t in threads]}


@router.get("/{forum_id}/threads")
async def get_forum_threads(
    forum_id: int,
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
):
    service = ForumService(db)
    threads = await service.get_threads(forum_id, tenant_id, skip=skip, limit=limit)
    return {"threads": [{"id": t.id, "title": t.title, "author_id": t.author_id, "is_pinned": t.is_pinned, "reply_count": t.reply_count, "view_count": t.view_count, "last_post_at": t.last_post_at.isoformat() if t.last_post_at else None} for t in threads]}


@router.get("/threads/{thread_id}")
async def get_thread_posts(
    thread_id: int,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
):
    service = ForumService(db)
    posts = await service.get_posts(thread_id, tenant_id, skip, limit)
    return {"posts": [{"id": p.id, "author_id": p.author_id, "content": p.content, "helpful_count": p.helpful_count, "created_at": p.created_at.isoformat()} for p in posts]}


@router.post("/threads/{thread_id}/posts")
async def create_post(
    thread_id: int,
    data: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = ForumService(db)
    post = await service.create_post(
        thread_id=thread_id,
        author_id=current_user.id,
        tenant_id=tenant_id,
        content=data.content,
    )
    return {"id": post.id, "content": post.content}


@router.post("/moderate")
async def moderate(
    data: ModerationAction,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = ForumService(db)
    moderation = await service.moderate(
        moderator_id=current_user.id,
        tenant_id=tenant_id,
        action=data.action,
        target_type=data.target_type,
        target_id=data.target_id,
        reason=data.reason,
    )
    return {"id": moderation.id, "action": moderation.action}
