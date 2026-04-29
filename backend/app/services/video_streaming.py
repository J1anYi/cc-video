from pathlib import Path
from fastapi.responses import FileResponse, Response
from fastapi import Request
from app.models.video_file import VideoFile
import os


class VideoStreamingService:
    """Service for streaming video files with Range header support."""

    async def stream(self, video_file: VideoFile, request: Request = None) -> Response:
        """Stream a video file with Range header support.

        Args:
            video_file: VideoFile record to stream
            request: Optional FastAPI request for Range header

        Returns:
            Response with appropriate headers for video streaming (206 for partial content)
        """
        file_path = Path(video_file.file_path)

        if not file_path.exists():
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Video file not found on disk")

        file_size = file_path.stat().st_size

        # Check for Range header
        range_header = request.headers.get("range") if request else None

        if range_header:
            # Parse Range header (e.g., "bytes=0-1023")
            range_match = range_header.replace("bytes=", "").split("-")
            start = int(range_match[0]) if range_match[0] else 0
            end = int(range_match[1]) if range_match[1] else file_size - 1

            # Clamp values to file size
            if start >= file_size:
                from fastapi import HTTPException
                raise HTTPException(status_code=416, detail="Requested range not satisfiable")

            end = min(end, file_size - 1)
            chunk_size = end - start + 1

            # Read the requested chunk
            with open(file_path, "rb") as f:
                f.seek(start)
                data = f.read(chunk_size)

            return Response(
                content=data,
                status_code=206,
                headers={
                    "Content-Range": f"bytes {start}-{end}/{file_size}",
                    "Accept-Ranges": "bytes",
                    "Content-Length": str(chunk_size),
                    "Content-Type": video_file.mime_type or "video/mp4",
                }
            )

        # No Range header - return full file with Accept-Ranges header
        return FileResponse(
            path=file_path,
            media_type=video_file.mime_type or "video/mp4",
            filename=video_file.filename,
            headers={
                "Accept-Ranges": "bytes",
                "Content-Length": str(file_size),
            }
        )


video_streaming_service = VideoStreamingService()
