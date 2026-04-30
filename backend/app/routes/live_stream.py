"""Live streaming routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.live_stream import CreatorLiveStreamService
from app.models.live_stream import CreatorLiveStream

router = APIRouter(prefix="/live", tags=["live-stream"])

@router.post("/streams")
def create_stream(title: str, description: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return CreatorLiveStreamService.create_stream(db, current_user.id, title, description)

@router.get("/streams")
def get_streams(db: Session = Depends(get_db)):
    return db.query(CreatorLiveStream).all()

@router.post("/streams/{stream_id}/start")
def start_stream(stream_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return CreatorLiveStreamService.start_stream(db, stream_id)

@router.post("/streams/{stream_id}/end")
def end_stream(stream_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return CreatorLiveStreamService.end_stream(db, stream_id)

@router.post("/chat")
def send_chat(stream_id: int, message: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return CreatorLiveStreamService.add_chat_message(db, stream_id, current_user.id, message)

@router.get("/chat/{stream_id}")
def get_chat(stream_id: int, limit: int = 50, db: Session = Depends(get_db)):
    return CreatorLiveStreamService.get_chat_messages(db, stream_id, limit)

@router.post("/schedule")
def schedule_stream(title: str, scheduled_start: datetime, description: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return CreatorLiveStreamService.schedule_stream(db, current_user.id, title, scheduled_start, description)

@router.get("/schedule")
def get_scheduled(creator_id: Optional[int] = None, db: Session = Depends(get_db)):
    return CreatorLiveStreamService.get_scheduled_streams(db, creator_id)
