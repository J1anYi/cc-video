"""
HDR video detection and processing service.

Supports:
- HDR10 detection via color metadata
- HDR metadata extraction
- Tone mapping for SDR fallback
"""

import asyncio
import subprocess
import json
import logging
from pathlib import Path
from typing import Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class HDRMetadata:
    """HDR video metadata."""
    is_hdr: bool
    format: Optional[str] = None  # HDR10, HDR10+, Dolby Vision
    color_space: Optional[str] = None
    color_primaries: Optional[str] = None
    color_transfer: Optional[str] = None
    max_cll: Optional[int] = None  # Max content light level
    max_fall: Optional[int] = None  # Max frame average light level


class HDRService:
    """Service for HDR video detection and processing."""

    # HDR indicators
    HDR_TRANSFER_FUNCTIONS = {"smpte2084", "pq", "arib-std-b67"}
    HDR_COLOR_PRIMARIES = {"bt2020", "bt.2020"}
    HDR_COLOR_SPACES = {"bt2020nc", "bt2020c", "bt.2020"}

    async def detect_hdr(self, video_path: Path) -> HDRMetadata:
        """
        Detect if video has HDR content.

        Args:
            video_path: Path to video file

        Returns:
            HDRMetadata with detection results
        """
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_streams",
            "-select_streams", "v:0",
            str(video_path)
        ]

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await process.communicate()
            data = json.loads(stdout.decode())

            if not data.get("streams"):
                return HDRMetadata(is_hdr=False)

            stream = data["streams"][0]

            color_transfer = stream.get("color_transfer", "")
            color_primaries = stream.get("color_primaries", "")
            color_space = stream.get("color_space", "")

            # Check for HDR indicators
            is_hdr = self._is_hdr_stream(
                color_transfer, color_primaries, color_space
            )

            if is_hdr:
                hdr_format = self._determine_hdr_format(stream)
                max_cll, max_fall = self._extract_light_levels(stream)

                return HDRMetadata(
                    is_hdr=True,
                    format=hdr_format,
                    color_space=color_space,
                    color_primaries=color_primaries,
                    color_transfer=color_transfer,
                    max_cll=max_cll,
                    max_fall=max_fall
                )

            return HDRMetadata(
                is_hdr=False,
                color_space=color_space,
                color_primaries=color_primaries,
                color_transfer=color_transfer
            )

        except Exception as e:
            logger.error(f"Failed to detect HDR: {e}")
            return HDRMetadata(is_hdr=False)

    def _is_hdr_stream(
        self,
        color_transfer: str,
        color_primaries: str,
        color_space: str
    ) -> bool:
        """Check if stream parameters indicate HDR."""
        transfer_lower = color_transfer.lower()
        primaries_lower = color_primaries.lower()
        space_lower = color_space.lower()

        # HDR10 requires PQ transfer and BT.2020 primaries
        is_hdr10 = (
            transfer_lower in self.HDR_TRANSFER_FUNCTIONS and
            (primaries_lower in self.HDR_COLOR_PRIMARIES or
             space_lower in self.HDR_COLOR_SPACES)
        )

        return is_hdr10

    def _determine_hdr_format(self, stream: dict) -> str:
        """Determine specific HDR format."""
        # Check for HDR10+ (dynamic metadata)
        side_data_list = stream.get("side_data_list", [])
        for side_data in side_data_list:
            if side_data.get("side_data_type") == "HDR dynamic metadata":
                return "HDR10+"

        return "HDR10"

    def _extract_light_levels(
        self,
        stream: dict
    ) -> Tuple[Optional[int], Optional[int]]:
        """Extract MaxCLL and MaxFALL values."""
        max_cll = stream.get("max_cll")
        max_fall = stream.get("max_fall")

        return (
            int(max_cll) if max_cll else None,
            int(max_fall) if max_fall else None
        )

    def get_tone_mapping_filter(
        self,
        source_is_hdr: bool,
        target_nits: int = 100
    ) -> Optional[str]:
        """
        Get FFmpeg filter for tone mapping HDR to SDR.

        Args:
            source_is_hdr: Whether source is HDR
            target_nits: Target peak brightness

        Returns:
            FFmpeg filter string or None
        """
        if not source_is_hdr:
            return None

        # Use zscale for tone mapping (fast, good quality)
        return (
            f"zscale=t=linear:npl=100,"
            f"format=gbrpf32le,"
            f"zscale=p=bt709:t=bt709:m=bt709:r=full,"
            f"tonemap=hable:peak={target_nits},"
            f"zscale=t=bt709:m=bt709:r=full,"
            f"format=yuv420p"
        )

    def get_hdr_encoding_params(self, hdr_format: str) -> list:
        """
        Get FFmpeg encoding parameters for HDR output.

        Args:
            hdr_format: HDR format (HDR10, HDR10+)

        Returns:
            List of FFmpeg parameters
        """
        params = [
            "-color_primaries", "bt2020",
            "-color_trc", "smpte2084",
            "-colorspace", "bt2020nc",
            "-color_range", "tv",
        ]

        return params


hdr_service = HDRService()
