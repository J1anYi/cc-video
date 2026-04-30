import uuid
from pathlib import Path
from typing import List, Optional
from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.video_file import VideoFile


class VideoFileService:
    """Service layer for video file upload and storage operations."""

    async def upload(
        self, db: AsyncSession, movie_id: int, file: UploadFile
    ) -> VideoFile:
        """Upload and store a video file.

        Args:
            db: Database session
            movie_id: Movie ID to attach video to
            file: Uploaded file from FastAPI

        Returns:
            Created VideoFile record

        Raises:
            ValueError: If file validation fails
        """
        # Validate MIME type
        if file.content_type not in settings.ALLOWED_VIDEO_TYPES:
            raise ValueError(
                f"Invalid file type: {file.content_type}. "
                f"Allowed types: {', '.join(settings.ALLOWED_VIDEO_TYPES)}"
            )

        # Read file content
        content = await file.read()
        file_size = len(content)

        # Validate file size
        if file_size > settings.MAX_VIDEO_SIZE:
            raise ValueError(
                f"File too large: {file_size} bytes. "
                f"Maximum size: {settings.MAX_VIDEO_SIZE} bytes"
            )

        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}_{file.filename}"

        # Ensure upload directory exists
        upload_dir = Path(settings.UPLOAD_DIR)
        upload_dir.mkdir(parents=True, exist_ok=True)

        # Save file to disk
        file_path = upload_dir / unique_filename
        file_path.write_bytes(content)

        # Create database record
        video_file = VideoFile(
            movie_id=movie_id,
            filename=file.filename or "unknown",
            file_path=str(file_path),
            file_size=file_size,
            mime_type=file.content_type,
        )
        db.add(video_file)
        await db.commit()
        await db.refresh(video_file)

        return video_file

    async def get_by_movie(
        self, db: AsyncSession, movie_id: int
    ) -> List[VideoFile]:
        """Get all video files for a movie.

        Args:
            db: Database session
            movie_id: Movie ID to look up

        Returns:
            List of VideoFile records for the movie
        """
        result = await db.execute(
            select(VideoFile).where(VideoFile.movie_id == movie_id)
        )
        return list(result.scalars().all())

    async def get_by_id(
        self, db: AsyncSession, video_file_id: int
    ) -> Optional[VideoFile]:
        """Get a video file by ID.

        Args:
            db: Database session
            video_file_id: Video file ID to look up

        Returns:
            VideoFile if found, None otherwise
        """
        result = await db.execute(
            select(VideoFile).where(VideoFile.id == video_file_id)
        )
        return result.scalar_one_or_none()

    async def delete(self, db: AsyncSession, video_file_id: int) -> bool:
        """Delete a video file and its database record.

        Args:
            db: Database session
            video_file_id: Video file ID to delete

        Returns:
            True if deleted, False if not found
        """
        video_file = await self.get_by_id(db, video_file_id)
        if not video_file:
            return False

        # Delete file from disk
        file_path = Path(video_file.file_path)
        if file_path.exists():
            file_path.unlink()

        # Delete database record
        await db.delete(video_file)
        await db.commit()

        return True


video_file_service = VideoFileService()
