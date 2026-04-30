"""
Video transcoding service for generating HLS quality variants.
"""

import asyncio
import subprocess
import json
import logging
from pathlib import Path
from typing import List, Optional, Tuple
from dataclasses import dataclass

from app.models.video_quality import QualityLevel, QUALITY_RESOLUTIONS, QUALITY_BITRATES

logger = logging.getLogger(__name__)


@dataclass
class TranscodingResult:
    """Result of a transcoding job."""
    success: bool
    quality: QualityLevel
    segments_dir: Optional[Path] = None
    playlist_path: Optional[Path] = None
    total_size: int = 0
    error: Optional[str] = None


class TranscodingService:
    """Service for video transcoding and HLS generation."""

    def __init__(self, hls_storage_path: str = "uploads/hls"):
        self.hls_storage_path = Path(hls_storage_path)
        self.segment_duration = 6
        self._hardware_accel_available = None

    def detect_hardware_acceleration(self) -> Optional[str]:
        if self._hardware_accel_available is not None:
            return self._hardware_accel_available
        try:
            result = subprocess.run(["ffmpeg", "-encoders"], capture_output=True, text=True, timeout=10)
            if "h264_nvenc" in result.stdout:
                self._hardware_accel_available = "nvenc"
                return "nvenc"
            if "h264_qsv" in result.stdout:
                self._hardware_accel_available = "qsv"
                return "qsv"
        except Exception as e:
            logger.warning(f"Failed to detect hardware acceleration: {e}")
        self._hardware_accel_available = None
        return None

    def get_encoder_settings(self, quality: QualityLevel) -> Tuple[str, List[str]]:
        accel = self.detect_hardware_acceleration()
        if accel == "nvenc":
            return "h264_nvenc", ["-preset", "p4", "-rc", "vbr", "-cq", "23"]
        elif accel == "qsv":
            return "h264_qsv", ["-preset", "medium", "-global_quality", "23"]
        return "libx264", ["-preset", "medium", "-crf", "23"]

    def get_target_qualities(self, source_width: int, source_height: int) -> List[QualityLevel]:
        qualities = [QualityLevel.QUALITY_480P, QualityLevel.QUALITY_720P]
        if source_height >= 1080:
            qualities.append(QualityLevel.QUALITY_1080P)
        if source_height >= 2160:
            qualities.append(QualityLevel.QUALITY_4K)
        return qualities

    async def transcode_to_hls(self, source_path: Path, output_dir: Path, quality: QualityLevel) -> TranscodingResult:
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            width, height = QUALITY_RESOLUTIONS[quality]
            bitrate = QUALITY_BITRATES[quality]
            encoder, extra_flags = self.get_encoder_settings(quality)
            scale_filter = f"scale=-2:{height}"
            playlist_path = output_dir / "playlist.m3u8"
            segment_pattern = output_dir / "segment_%03d.ts"
            cmd = [
                "ffmpeg", "-i", str(source_path), "-vf", scale_filter, "-c:v", encoder,
                *extra_flags, "-b:v", str(bitrate), "-maxrate", str(int(bitrate * 1.5)),
                "-bufsize", str(int(bitrate * 2)), "-c:a", "aac", "-b:a", "128k",
                "-f", "hls", "-hls_time", str(self.segment_duration), "-hls_list_size", "0",
                "-hls_segment_filename", str(segment_pattern), str(playlist_path)
            ]
            logger.info(f"Starting transcoding for {quality.value}")
            process = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await process.communicate()
            if process.returncode != 0:
                return TranscodingResult(success=False, quality=quality, error=stderr.decode() if stderr else "Unknown error")
            total_size = sum(f.stat().st_size for f in output_dir.glob("*.ts"))
            return TranscodingResult(success=True, quality=quality, segments_dir=output_dir, playlist_path=playlist_path, total_size=total_size)
        except Exception as e:
            return TranscodingResult(success=False, quality=quality, error=str(e))

    async def get_video_resolution(self, video_path: Path) -> Tuple[int, int]:
        cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", "-select_streams", "v:0", str(video_path)]
        try:
            process = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, _ = await process.communicate()
            data = json.loads(stdout.decode())
            return int(data["streams"][0]["width"]), int(data["streams"][0]["height"])
        except Exception as e:
            logger.error(f"Failed to get video resolution: {e}")
            return 1920, 1080


transcoding_service = TranscodingService()
