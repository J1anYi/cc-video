"""Live streaming services."""
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.live_stream import LiveStream, LiveChatMessage, LiveStreamSchedule
import uuid

class LiveStreamService:
    @staticmethod
    def create_stream(db, creator_id, title, description=None):
        stream = LiveStream(creator_id=creator_id, title=title, description=description, stream_key=str(uuid.uuid4()))
        db.add(stream)
        db.commit()
        db.refresh(stream)
        return stream

    @staticmethod
    def get_stream(db, stream_id):
        return db.query(LiveStream).filter(LiveStream.id == stream_id).first()

    @staticmethod
    def get_creator_streams(db, creator_id):
        return db.query(LiveStream).filter(LiveStream.creator_id == creator_id).order_by(LiveStream.created_at.desc()).all()

    @staticmethod
    def start_stream(db, stream_id):
        stream = db.query(LiveStream).filter(LiveStream.id == stream_id).first()
        if stream:
            stream.status = 'live'
            stream.started_at = datetime.utcnow()
            db.commit()
            db.refresh(stream)
        return stream

    @staticmethod
    def end_stream(db, stream_id):
        stream = db.query(LiveStream).filter(LiveStream.id == stream_id).first()
        if stream:
            stream.status = 'ended'
            stream.ended_at = datetime.utcnow()
            if stream.started_at:
                stream.duration = int((stream.ended_at - stream.started_at).total_seconds())
            db.commit()
            db.refresh(stream)
        return stream

    @staticmethod
    def add_chat_message(db, stream_id, user_id, message):
        msg = LiveChatMessage(stream_id=stream_id, user_id=user_id, message=message)
        db.add(msg)
        db.commit()
        db.refresh(msg)
        return msg

    @staticmethod
    def get_chat_messages(db, stream_id, limit=50):
        return db.query(LiveChatMessage).filter(LiveChatMessage.stream_id == stream_id).order_by(LiveChatMessage.created_at.desc()).limit(limit).all()

    @staticmethod
    def schedule_stream(db, creator_id, title, scheduled_start, description=None):
        schedule = LiveStreamSchedule(creator_id=creator_id, title=title, description=description, scheduled_start=scheduled_start)
        db.add(schedule)
        db.commit()
        db.refresh(schedule)
        return schedule

    @staticmethod
    def get_scheduled_streams(db, creator_id=None):
        query = db.query(LiveStreamSchedule).filter(LiveStreamSchedule.scheduled_start > datetime.utcnow())
        if creator_id:
            query = query.filter(LiveStreamSchedule.creator_id == creator_id)
        return query.order_by(LiveStreamSchedule.scheduled_start).all()
