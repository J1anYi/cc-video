from pathlib import Path
from fastapi.responses import FileResponse
from fastapi import Request
from app.models.video_file import VideoFile


class VideoStreamingService:
    """Service for streaming video files with Range header support."""

    async def stream(self, video_file: VideoFile, request: Request = None) -> FileResponse:
        """Stream a video file with Range header support.

        Args:
            video_file: VideoFile record to stream
            request: Optional FastAPI request for Range header

        Returns:
            FileResponse with appropriate headers for video streaming
        """
        file_path = Path(video_file.file_path)
        
        if not file_path.exists():
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Video file not found on disk")

        # FileResponse automatically handles Range requests
        return FileResponse(
            path=file_path,
            media_type=video_file.mime_type,
            filename=video_file.filename,
        )


video_streaming_service = VideoStreamingService()
