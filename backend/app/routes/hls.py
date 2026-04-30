"""
HLS streaming routes for adaptive bitrate video playback.
"""

from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.dependencies import get_db
from app.models.video_file import VideoFile
from app.models.video_quality import VideoQuality, QualityLevel
from app.models.movie import Movie, PublicationStatus
from app.services.hls_service import hls_service
from app.schemas.video_quality import VideoQualityResponse, VideoQualitiesListResponse

router = APIRouter(prefix="/api/hls", tags=["hls"])


@router.get("/video/{video_file_id}/master.m3u8")
async def get_master_playlist(
    video_file_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get HLS master playlist for adaptive streaming."""
    result = await db.execute(select(VideoFile).where(VideoFile.id == video_file_id))
    video_file = result.scalar_one_or_none()
    
    if not video_file:
        raise HTTPException(status_code=404, detail="Video file not found")
    
    # Get all quality variants
    result = await db.execute(
        select(VideoQuality).where(VideoQuality.video_file_id == video_file_id)
    )
    qualities = result.scalars().all()
    
    if not qualities:
        raise HTTPException(status_code=404, detail="No quality variants available")
    
    # Generate master playlist
    playlist_content = hls_service.generate_master_playlist(video_file, qualities)
    
    return Response(
        content=playlist_content,
        media_type="application/vnd.apple.mpegurl",
        headers={
            "Cache-Control": "no-cache",
            "Access-Control-Allow-Origin": "*",
        }
    )


@router.get("/video/{video_file_id}/{quality}/playlist.m3u8")
async def get_quality_playlist(
    video_file_id: int,
    quality: QualityLevel,
    db: AsyncSession = Depends(get_db)
):
    """Get HLS media playlist for a specific quality."""
    result = await db.execute(
        select(VideoQuality).where(
            VideoQuality.video_file_id == video_file_id,
            VideoQuality.quality == quality
        )
    )
    quality_record = result.scalar_one_or_none()
    
    if not quality_record:
        raise HTTPException(status_code=404, detail="Quality variant not found")
    
    playlist_path = Path(quality_record.segments_dir) / "playlist.m3u8"
    
    if not playlist_path.exists():
        raise HTTPException(status_code=404, detail="Playlist file not found")
    
    with open(playlist_path, "r") as f:
        content = f.read()
    
    return Response(
        content=content,
        media_type="application/vnd.apple.mpegurl",
        headers={
            "Cache-Control": "no-cache",
            "Access-Control-Allow-Origin": "*",
        }
    )


@router.get("/video/{video_file_id}/{quality}/{segment}")
async def get_hls_segment(
    video_file_id: int,
    quality: QualityLevel,
    segment: str,
    db: AsyncSession = Depends(get_db)
):
    """Get HLS segment file."""
    # Validate segment name format
    if not segment.endswith(".ts") or not segment.startswith("segment_"):
        raise HTTPException(status_code=400, detail="Invalid segment name")
    
    result = await db.execute(
        select(VideoQuality).where(
            VideoQuality.video_file_id == video_file_id,
            VideoQuality.quality == quality
        )
    )
    quality_record = result.scalar_one_or_none()
    
    if not quality_record:
        raise HTTPException(status_code=404, detail="Quality variant not found")
    
    segment_path = Path(quality_record.segments_dir) / segment
    
    if not segment_path.exists():
        raise HTTPException(status_code=404, detail="Segment not found")
    
    return FileResponse(
        path=segment_path,
        media_type="video/MP2T",
        headers={
            "Cache-Control": "public, max-age=31536000",
            "Access-Control-Allow-Origin": "*",
        }
    )


@router.get("/video/{video_file_id}/qualities", response_model=VideoQualitiesListResponse)
async def get_available_qualities(
    video_file_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get available quality variants for a video."""
    result = await db.execute(select(VideoFile).where(VideoFile.id == video_file_id))
    video_file = result.scalar_one_or_none()
    
    if not video_file:
        raise HTTPException(status_code=404, detail="Video file not found")
    
    result = await db.execute(
        select(VideoQuality).where(VideoQuality.video_file_id == video_file_id)
    )
    qualities = result.scalars().all()
    
    return VideoQualitiesListResponse(
        video_file_id=video_file_id,
        qualities=[
            VideoQualityResponse(
                quality=q.quality.value,
                width=q.width,
                height=q.height,
                bitrate=q.bitrate,
                resolution=q.resolution
            )
            for q in qualities
        ]
    )
