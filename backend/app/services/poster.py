import os
import uuid
from pathlib import Path
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings


class PosterService:
    def __init__(self):
        self.upload_dir = Path(settings.upload_dir) / "posters"
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.allowed_types = {"image/jpeg", "image/png", "image/webp", "image/gif"}
    
    async def upload(self, db: AsyncSession, movie_id: int, file: UploadFile) -> str:
        """Upload a poster image for a movie. Returns the relative path."""
        if file.content_type not in self.allowed_types:
            raise ValueError(f"Invalid file type. Allowed: {self.allowed_types}")
        
        # Generate unique filename
        ext = os.path.splitext(file.filename or "image.jpg")[1] or ".jpg"
        filename = f"{uuid.uuid4()}_poster{ext}"
        file_path = self.upload_dir / filename
        
        # Save file
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Return relative path for storage
        return f"/uploads/posters/{filename}"
    
    def delete(self, poster_path: str | None) -> bool:
        """Delete a poster file if it exists."""
        if not poster_path:
            return False
        
        # Extract filename from path
        filename = poster_path.split("/")[-1]
        file_path = self.upload_dir / filename
        
        if file_path.exists():
            os.remove(file_path)
            return True
        return False


poster_service = PosterService()
