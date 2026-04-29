import os
import uuid
from pathlib import Path
from typing import List
from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.subtitle import Subtitle


class SubtitleService:
    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR) / "subtitles"
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.allowed_types = {"application/x-subrip", "text/vtt", "text/srt", "text/plain"}
    
    async def upload(self, db: AsyncSession, movie_id: int, language: str, file: UploadFile) -> Subtitle:
        """Upload a subtitle file for a movie. Returns the Subtitle record."""
        # Check content type - be lenient since browsers may not recognize subtitle types
        content_type = file.content_type or "text/plain"
        # Check extension as fallback
        filename = file.filename or ""
        ext = os.path.splitext(filename)[1].lower()
        valid_extensions = {".srt", ".vtt"}
        
        if content_type not in self.allowed_types and ext not in valid_extensions:
            raise ValueError(f"Invalid file type. Allowed: SRT, VTT files")
        
        # Generate unique filename
        ext = ext or ".vtt"
        unique_filename = f"{uuid.uuid4()}_subtitle{ext}"
        file_path = self.upload_dir / unique_filename
        
        # Save file
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Create database record
        subtitle = Subtitle(
            movie_id=movie_id,
            language=language,
            file_path=str(file_path)
        )
        db.add(subtitle)
        await db.commit()
        await db.refresh(subtitle)
        
        return subtitle
    
    async def get_by_movie(self, db: AsyncSession, movie_id: int) -> List[Subtitle]:
        """Get all subtitles for a movie."""
        result = await db.execute(
            select(Subtitle).where(Subtitle.movie_id == movie_id)
        )
        return list(result.scalars().all())
    
    async def get_by_id(self, db: AsyncSession, subtitle_id: int) -> Subtitle | None:
        """Get a subtitle by ID."""
        result = await db.execute(
            select(Subtitle).where(Subtitle.id == subtitle_id)
        )
        return result.scalar_one_or_none()
    
    async def delete(self, db: AsyncSession, subtitle_id: int) -> bool:
        """Delete a subtitle file and its database record."""
        subtitle = await self.get_by_id(db, subtitle_id)
        if not subtitle:
            return False
        
        # Delete file from disk
        file_path = Path(subtitle.file_path)
        if file_path.exists():
            os.remove(file_path)
        
        # Delete database record
        await db.delete(subtitle)
        await db.commit()
        
        return True


subtitle_service = SubtitleService()
