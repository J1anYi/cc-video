"""Forum service for community discussions."""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.forum import Forum, ForumThread, ForumPost, ForumModeration, ThreadStatus


class ForumService:
    """Service for forum operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_forum(
        self,
        tenant_id: int,
        name: str,
        slug: str,
        description: str = None,
        category: str = "general",
        order: int = 0,
    ) -> Forum:
        """Create a forum."""
        forum = Forum(
            tenant_id=tenant_id,
            name=name,
            slug=slug,
            description=description,
            category=category,
            order=order,
        )
        self.db.add(forum)
        await self.db.commit()
        await self.db.refresh(forum)
        return forum

    async def get_forums(self, tenant_id: int) -> List[Forum]:
        """Get all forums for tenant."""
        query = select(Forum).where(
            Forum.tenant_id == tenant_id,
            Forum.is_active == True,
        ).order_by(Forum.order.asc())
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_thread(
        self,
        forum_id: int,
        author_id: int,
        tenant_id: int,
        title: str,
        content: str,
    ) -> ForumThread:
        """Create a thread with first post."""
        thread = ForumThread(
            forum_id=forum_id,
            author_id=author_id,
            tenant_id=tenant_id,
            title=title,
        )
        self.db.add(thread)
        await self.db.commit()
        await self.db.refresh(thread)
        
        # Create first post
        post = ForumPost(
            thread_id=thread.id,
            author_id=author_id,
            tenant_id=tenant_id,
            content=content,
        )
        self.db.add(post)
        
        # Update forum thread count
        forum = await self.db.get(Forum, forum_id)
        if forum:
            forum.thread_count += 1
        
        await self.db.commit()
        await self.db.refresh(thread)
        return thread

    async def get_threads(
        self,
        forum_id: int,
        tenant_id: int,
        pinned_first: bool = True,
        skip: int = 0,
        limit: int = 20,
    ) -> List[ForumThread]:
        """Get threads for a forum."""
        query = select(ForumThread).where(
            ForumThread.forum_id == forum_id,
            ForumThread.tenant_id == tenant_id,
            ForumThread.status != ThreadStatus.HIDDEN,
        )
        
        if pinned_first:
            query = query.order_by(
                ForumThread.is_pinned.desc(),
                ForumThread.last_post_at.desc(),
            )
        else:
            query = query.order_by(ForumThread.last_post_at.desc())
        
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_post(
        self,
        thread_id: int,
        author_id: int,
        tenant_id: int,
        content: str,
    ) -> ForumPost:
        """Create a post in a thread."""
        post = ForumPost(
            thread_id=thread_id,
            author_id=author_id,
            tenant_id=tenant_id,
            content=content,
        )
        self.db.add(post)
        
        # Update thread stats
        thread = await self.db.get(ForumThread, thread_id)
        if thread:
            thread.reply_count += 1
            thread.last_post_at = datetime.utcnow()
            thread.last_post_by = author_id
        
        # Update forum post count
        if thread:
            forum = await self.db.get(Forum, thread.forum_id)
            if forum:
                forum.post_count += 1
        
        await self.db.commit()
        await self.db.refresh(post)
        return post

    async def get_posts(
        self,
        thread_id: int,
        tenant_id: int,
        skip: int = 0,
        limit: int = 50,
    ) -> List[ForumPost]:
        """Get posts for a thread."""
        query = select(ForumPost).where(
            ForumPost.thread_id == thread_id,
            ForumPost.tenant_id == tenant_id,
            ForumPost.is_hidden == False,
        ).order_by(ForumPost.created_at.asc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def search_threads(
        self,
        tenant_id: int,
        query_str: str,
        skip: int = 0,
        limit: int = 20,
    ) -> List[ForumThread]:
        """Search threads by title."""
        query = select(ForumThread).where(
            ForumThread.tenant_id == tenant_id,
            ForumThread.status != ThreadStatus.HIDDEN,
            ForumThread.title.ilike(f"%{query_str}%"),
        ).order_by(ForumThread.created_at.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def moderate(
        self,
        moderator_id: int,
        tenant_id: int,
        action: str,
        target_type: str,
        target_id: int,
        reason: str = None,
    ) -> ForumModeration:
        """Apply moderation action."""
        moderation = ForumModeration(
            moderator_id=moderator_id,
            tenant_id=tenant_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            reason=reason,
        )
        self.db.add(moderation)
        
        # Apply action
        if target_type == "thread":
            thread = await self.db.get(ForumThread, target_id)
            if thread:
                if action == "pin":
                    thread.is_pinned = True
                elif action == "unpin":
                    thread.is_pinned = False
                elif action == "lock":
                    thread.status = ThreadStatus.CLOSED
                elif action == "unlock":
                    thread.status = ThreadStatus.OPEN
                elif action == "hide":
                    thread.status = ThreadStatus.HIDDEN
        elif target_type == "post":
            post = await self.db.get(ForumPost, target_id)
            if post and action == "hide":
                post.is_hidden = True
        
        await self.db.commit()
        await self.db.refresh(moderation)
        return moderation
