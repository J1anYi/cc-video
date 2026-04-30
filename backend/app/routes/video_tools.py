"""Video editing tools routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.video_tools import VideoToolsService

router = APIRouter(prefix="/video-tools", tags=["video-tools"])

@router.post("/projects")
def create_project(movie_id: int, name: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return VideoToolsService.create_edit_project(db, movie_id, current_user.id, name)

@router.get("/projects")
def get_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return VideoToolsService.get_edit_projects(db, current_user.id)

@router.post("/thumbnails/{movie_id}/generate")
def generate_thumbnails(movie_id: int, count: int = 5, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return VideoToolsService.generate_thumbnails(db, movie_id, "", count)

@router.get("/thumbnails/{movie_id}")
def get_thumbnails(movie_id: int, db: Session = Depends(get_db)):
    return VideoToolsService.get_thumbnails(db, movie_id)

@router.post("/chapters")
def create_chapter(movie_id: int, title: str, start_time: float, end_time: Optional[float] = None, description: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return VideoToolsService.create_chapter(db, movie_id, title, start_time, end_time, description)

@router.get("/chapters/{movie_id}")
def get_chapters(movie_id: int, db: Session = Depends(get_db)):
    return VideoToolsService.get_chapters(db, movie_id)

@router.post("/audio-tracks")
def add_audio_track(movie_id: int, language_code: str, language_name: str, audio_url: str, is_default: bool = False, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return VideoToolsService.add_audio_track(db, movie_id, language_code, language_name, audio_url, is_default)

@router.get("/audio-tracks/{movie_id}")
def get_audio_tracks(movie_id: int, db: Session = Depends(get_db)):
    return VideoToolsService.get_audio_tracks(db, movie_id)

@router.post("/subtitles")
def add_subtitle(movie_id: int, language_code: str, language_name: str, subtitle_url: str, is_default: bool = False, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return VideoToolsService.add_subtitle(db, movie_id, language_code, language_name, subtitle_url, is_default)

@router.get("/subtitles/{movie_id}")
def get_subtitles(movie_id: int, db: Session = Depends(get_db)):
    return VideoToolsService.get_subtitles(db, movie_id)

@router.post("/templates")
def create_template(name: str, category: str, config: dict, is_public: bool = False, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return VideoToolsService.create_template(db, name, category, config, current_user.id, is_public)

@router.get("/templates")
def get_templates(category: Optional[str] = None, db: Session = Depends(get_db)):
    return VideoToolsService.get_templates(db, category)
