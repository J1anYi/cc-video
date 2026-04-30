"""Group service for user clubs and communities."""
import json
from datetime import datetime
from typing import List, Optional
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.group import (
    Group, GroupMember, GroupCollection, GroupCollectionItem,
    GroupDiscussion, GroupDiscussionReply, GroupActivity,
    GroupPrivacy, GroupRole
)


class GroupService:
    """Service for group operations."""

    async def create_group(
        self, session: AsyncSession, tenant_id: int, name: str, slug: str,
        created_by: int, description: Optional[str] = None,
        privacy: GroupPrivacy = GroupPrivacy.PUBLIC
    ) -> Group:
        group = Group(
            tenant_id=tenant_id, name=name, slug=slug,
            description=description, privacy=privacy, created_by=created_by
        )
        session.add(group)
        await session.flush()
        member = GroupMember(
            group_id=group.id, user_id=created_by,
            tenant_id=tenant_id, role=GroupRole.OWNER
        )
        session.add(member)
        group.member_count = 1
        await self.log_activity(session, group.id, created_by, tenant_id, "group_created", json.dumps({"name": name}))
        await session.commit()
        return group

    async def get_groups(self, session: AsyncSession, tenant_id: int, user_id: int) -> List[Group]:
        member_groups = select(GroupMember.group_id).where(
            GroupMember.user_id == user_id, GroupMember.tenant_id == tenant_id
        )
        result = await session.execute(
            select(Group).where(
                Group.tenant_id == tenant_id, Group.is_active == True,
                or_(Group.privacy == GroupPrivacy.PUBLIC, Group.id.in_(member_groups))
            ).order_by(Group.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_group(self, session: AsyncSession, group_id: int) -> Optional[Group]:
        result = await session.execute(
            select(Group).where(Group.id == group_id, Group.is_active == True)
        )
        return result.scalar_one_or_none()

    async def update_group(self, session: AsyncSession, group_id: int, **kwargs) -> Optional[Group]:
        group = await self.get_group(session, group_id)
        if not group:
            return None
        for key, value in kwargs.items():
            if hasattr(group, key) and value is not None:
                setattr(group, key, value)
        group.updated_at = datetime.utcnow()
        await session.commit()
        return group

    async def delete_group(self, session: AsyncSession, group_id: int) -> bool:
        group = await self.get_group(session, group_id)
        if not group:
            return False
        group.is_active = False
        await session.commit()
        return True

    async def join_group(self, session: AsyncSession, group_id: int, user_id: int, tenant_id: int) -> Optional[GroupMember]:
        group = await self.get_group(session, group_id)
        if not group or group.privacy != GroupPrivacy.PUBLIC:
            return None
        existing = await session.execute(
            select(GroupMember).where(GroupMember.group_id == group_id, GroupMember.user_id == user_id)
        )
        if existing.scalar_one_or_none():
            return None
        member = GroupMember(group_id=group_id, user_id=user_id, tenant_id=tenant_id, role=GroupRole.MEMBER)
        session.add(member)
        group.member_count += 1
        await self.log_activity(session, group_id, user_id, tenant_id, "member_joined", json.dumps({"user_id": user_id}))
        await session.commit()
        return member

    async def leave_group(self, session: AsyncSession, group_id: int, user_id: int) -> bool:
        result = await session.execute(
            select(GroupMember).where(GroupMember.group_id == group_id, GroupMember.user_id == user_id)
        )
        member = result.scalar_one_or_none()
        if not member or member.role == GroupRole.OWNER:
            return False
        await session.delete(member)
        group = await self.get_group(session, group_id)
        if group:
            group.member_count = max(0, group.member_count - 1)
        await session.commit()
        return True

    async def invite_member(self, session: AsyncSession, group_id: int, user_id: int, invited_by: int, tenant_id: int) -> Optional[GroupMember]:
        group = await self.get_group(session, group_id)
        if not group:
            return None
        existing = await session.execute(
            select(GroupMember).where(GroupMember.group_id == group_id, GroupMember.user_id == user_id)
        )
        if existing.scalar_one_or_none():
            return None
        member = GroupMember(group_id=group_id, user_id=user_id, tenant_id=tenant_id, role=GroupRole.MEMBER)
        session.add(member)
        group.member_count += 1
        await self.log_activity(session, group_id, invited_by, tenant_id, "member_invited", json.dumps({"user_id": user_id}))
        await session.commit()
        return member

    async def get_members(self, session: AsyncSession, group_id: int) -> List[GroupMember]:
        result = await session.execute(
            select(GroupMember).where(GroupMember.group_id == group_id).order_by(GroupMember.joined_at)
        )
        return list(result.scalars().all())

    async def update_member_role(self, session: AsyncSession, group_id: int, user_id: int, role: GroupRole) -> Optional[GroupMember]:
        result = await session.execute(
            select(GroupMember).where(GroupMember.group_id == group_id, GroupMember.user_id == user_id)
        )
        member = result.scalar_one_or_none()
        if not member:
            return None
        member.role = role
        await session.commit()
        return member

    async def remove_member(self, session: AsyncSession, group_id: int, user_id: int) -> bool:
        result = await session.execute(
            select(GroupMember).where(GroupMember.group_id == group_id, GroupMember.user_id == user_id)
        )
        member = result.scalar_one_or_none()
        if not member:
            return False
        await session.delete(member)
        group = await self.get_group(session, group_id)
        if group:
            group.member_count = max(0, group.member_count - 1)
        await session.commit()
        return True

    async def create_collection(self, session: AsyncSession, group_id: int, tenant_id: int, name: str, created_by: int, description: Optional[str] = None) -> GroupCollection:
        collection = GroupCollection(group_id=group_id, tenant_id=tenant_id, name=name, description=description, created_by=created_by)
        session.add(collection)
        await self.log_activity(session, group_id, created_by, tenant_id, "collection_created", json.dumps({"name": name}))
        await session.commit()
        return collection

    async def get_collections(self, session: AsyncSession, group_id: int) -> List[GroupCollection]:
        result = await session.execute(
            select(GroupCollection).where(GroupCollection.group_id == group_id).order_by(GroupCollection.created_at.desc())
        )
        return list(result.scalars().all())

    async def add_collection_item(self, session: AsyncSession, collection_id: int, movie_id: int, added_by: int, tenant_id: int) -> Optional[GroupCollectionItem]:
        result = await session.execute(select(GroupCollection).where(GroupCollection.id == collection_id))
        collection = result.scalar_one_or_none()
        if not collection:
            return None
        existing = await session.execute(
            select(GroupCollectionItem).where(GroupCollectionItem.collection_id == collection_id, GroupCollectionItem.movie_id == movie_id)
        )
        if existing.scalar_one_or_none():
            return None
        item = GroupCollectionItem(collection_id=collection_id, movie_id=movie_id, added_by=added_by)
        session.add(item)
        collection.item_count += 1
        await self.log_activity(session, collection.group_id, added_by, tenant_id, "item_added", json.dumps({"movie_id": movie_id}))
        await session.commit()
        return item

    async def remove_collection_item(self, session: AsyncSession, item_id: int) -> bool:
        result = await session.execute(select(GroupCollectionItem).where(GroupCollectionItem.id == item_id))
        item = result.scalar_one_or_none()
        if not item:
            return False
        coll_result = await session.execute(select(GroupCollection).where(GroupCollection.id == item.collection_id))
        collection = coll_result.scalar_one_or_none()
        if collection:
            collection.item_count = max(0, collection.item_count - 1)
        await session.delete(item)
        await session.commit()
        return True

    async def create_discussion(self, session: AsyncSession, group_id: int, tenant_id: int, title: str, content: str, author_id: int) -> GroupDiscussion:
        discussion = GroupDiscussion(group_id=group_id, tenant_id=tenant_id, title=title, content=content, author_id=author_id)
        session.add(discussion)
        await self.log_activity(session, group_id, author_id, tenant_id, "discussion_created", json.dumps({"title": title}))
        await session.commit()
        return discussion

    async def get_discussions(self, session: AsyncSession, group_id: int) -> List[GroupDiscussion]:
        result = await session.execute(
            select(GroupDiscussion).where(GroupDiscussion.group_id == group_id).order_by(GroupDiscussion.is_pinned.desc(), GroupDiscussion.created_at.desc())
        )
        return list(result.scalars().all())

    async def create_discussion_reply(self, session: AsyncSession, discussion_id: int, tenant_id: int, content: str, author_id: int) -> Optional[GroupDiscussionReply]:
        result = await session.execute(select(GroupDiscussion).where(GroupDiscussion.id == discussion_id))
        discussion = result.scalar_one_or_none()
        if not discussion or discussion.is_locked:
            return None
        reply = GroupDiscussionReply(discussion_id=discussion_id, tenant_id=tenant_id, content=content, author_id=author_id)
        session.add(reply)
        discussion.reply_count += 1
        await self.log_activity(session, discussion.group_id, author_id, tenant_id, "reply_created", json.dumps({"discussion_id": discussion_id}))
        await session.commit()
        return reply

    async def get_activity_feed(self, session: AsyncSession, group_id: int, limit: int = 50) -> List[GroupActivity]:
        result = await session.execute(
            select(GroupActivity).where(GroupActivity.group_id == group_id).order_by(GroupActivity.created_at.desc()).limit(limit)
        )
        return list(result.scalars().all())

    async def log_activity(self, session: AsyncSession, group_id: int, user_id: int, tenant_id: int, activity_type: str, content: str) -> GroupActivity:
        activity = GroupActivity(group_id=group_id, user_id=user_id, tenant_id=tenant_id, activity_type=activity_type, content=content)
        session.add(activity)
        return activity

    async def get_member_role(self, session: AsyncSession, group_id: int, user_id: int) -> Optional[GroupRole]:
        result = await session.execute(
            select(GroupMember).where(GroupMember.group_id == group_id, GroupMember.user_id == user_id)
        )
        member = result.scalar_one_or_none()
        return member.role if member else None

    async def is_admin(self, session: AsyncSession, group_id: int, user_id: int) -> bool:
        role = await self.get_member_role(session, group_id, user_id)
        return role in [GroupRole.OWNER, GroupRole.ADMIN]

    async def is_owner(self, session: AsyncSession, group_id: int, user_id: int) -> bool:
        role = await self.get_member_role(session, group_id, user_id)
        return role == GroupRole.OWNER
