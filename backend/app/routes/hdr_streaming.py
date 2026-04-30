from fastapi import APIRouter
from typing import Dict, Any
from app.services.hdr_streaming import hdr_streaming_service

router = APIRouter(prefix="/api/hdr", tags=["hdr-streaming"])

@router.post("/encode/{video_id}")
async def encode_4k(video_id: str) -> Dict[str, Any]:
    return await hdr_streaming_service.encode_4k(video_id)

@router.post("/abr/{video_id}")
async def create_abr(video_id: str) -> Dict[str, Any]:
    return await hdr_streaming_service.create_abr_stream(video_id)

@router.post("/metadata/{video_id}")
async def inject_metadata(video_id: str) -> Dict[str, Any]:
    return await hdr_streaming_service.inject_metadata(video_id)

@router.get("/detect/{client_id}")
async def detect_hdr(client_id: str) -> Dict[str, Any]:
    return await hdr_streaming_service.detect_hdr_support(client_id)

@router.get("/bandwidth/{session_id}")
async def estimate_bandwidth(session_id: str) -> Dict[str, Any]:
    return await hdr_streaming_service.estimate_bandwidth(session_id)
