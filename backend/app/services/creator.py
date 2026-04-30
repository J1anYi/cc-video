"""Creator platform services."""
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.creator import (
    CreatorProfile, CreatorContent, CreatorContentAnalytics,
    CreatorTeamMember
)
from app.models.user import User
from app.schemas.creator import (
    CreatorProfileCreate, CreatorProfileUpdate,
    CreatorContentCreate, CreatorContentUpdate,
    TeamMemberInvite
)


class CreatorService:
    @staticmethod
    def create_profile(db, user_id, profile_data):
        profile = CreatorProfile(
            user_id=user_id,
            channel_name=profile_data.channel_name,
            channel_description=profile_data.channel_description,
            channel_art_url=profile_data.channel_art_url
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile

    @staticmethod
    def get_profile(db, user_id):
        return db.query(CreatorProfile).filter(CreatorProfile.user_id == user_id).first()

    @staticmethod
    def get_dashboard(db, user_id):
        profile = CreatorService.get_profile(db, user_id)
        if not profile:
            return None
        recent_content = db.query(CreatorContent).filter(
            CreatorContent.creator_id == profile.id
        ).order_by(CreatorContent.created_at.desc()).limit(5).all()
        total_revenue = db.query(func.sum(CreatorContentAnalytics.estimated_revenue)).filter(
            CreatorContentAnalytics.content_id.in_(
                db.query(CreatorContent.id).filter(CreatorContent.creator_id == profile.id)
            )
        ).scalar() or 0.0
        return {
            "profile": profile,
            "total_views": profile.total_views,
            "total_subscribers": profile.subscriber_count,
            "total_watch_time": profile.total_watch_time,
            "estimated_revenue": float(total_revenue),
            "recent_content": recent_content,
            "top_content": [],
            "audience_growth": {},
            "engagement_rate": 0.0
        }

    @staticmethod
    def create_content(db, creator_id, content_data):
        content = CreatorContent(creator_id=creator_id, **content_data.model_dump())
        db.add(content)
        db.commit()
        db.refresh(content)
        analytics = CreatorContentAnalytics(content_id=content.id)
        db.add(analytics)
        db.commit()
        return content

    @staticmethod
    def get_content(db, creator_id, status=None):
        query = db.query(CreatorContent).filter(CreatorContent.creator_id == creator_id)
        if status:
            query = query.filter(CreatorContent.status == status)
        return query.order_by(CreatorContent.created_at.desc()).all()

    @staticmethod
    def get_team_members(db, creator_id):
        return db.query(CreatorTeamMember).filter(
            CreatorTeamMember.creator_id == creator_id,
            CreatorTeamMember.is_active == True
        ).all()
