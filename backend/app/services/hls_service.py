from pathlib import Path
from typing import List
import logging
from app.models.video_file import VideoFile
from app.models.video_quality import VideoQuality, QualityLevel

logger = logging.getLogger(__name__)

class HLSService:
    def __init__(self, storage_path: str = "uploads/hls"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def generate_master_playlist(self, video_file: VideoFile, qualities: List[VideoQuality]) -> str:
        lines = ["#EXTM3U", "#EXT-X-VERSION:6"]
        if video_file.is_hdr:
            lines.append("# HDR Content")
        for q in sorted(qualities, key=lambda x: x.bitrate, reverse=True):
            vr = "HDR" if video_file.is_hdr else "SDR"
            lines.append("#EXT-X-STREAM-INF:BANDWIDTH=" + str(q.bitrate) + ",RESOLUTION=" + str(q.width) + "x" + str(q.height) + ",VIDEO-RANGE=" + vr)
            lines.append(str(q.quality.value) + "/playlist.m3u8")
        return "\n".join(lines)

    def generate_media_playlist(self, segments_dir: Path, segment_duration: int = 6) -> str:
        lines = ["#EXTM3U", "#EXT-X-VERSION:3", "#EXT-X-TARGETDURATION:" + str(segment_duration), "#EXT-X-MEDIA-SEQUENCE:0", "#EXT-X-PLAYLIST-TYPE:VOD"]
        for f in sorted(segments_dir.glob("segment_*.ts")):
            lines.append("#EXTINF:" + str(segment_duration) + ".0,")
            lines.append(f.name)
        lines.append("#EXT-X-ENDLIST")
        return "\n".join(lines)

    def get_hls_directory(self, video_file_id: int) -> Path:
        return self.storage_path / str(video_file_id)

    def get_master_playlist_path(self, video_file_id: int) -> Path:
        return self.get_hls_directory(video_file_id) / "master.m3u8"

    def get_quality_directory(self, video_file_id: int, quality: QualityLevel) -> Path:
        return self.get_hls_directory(video_file_id) / quality.value

    def ensure_directories(self, video_file_id: int, qualities: List[QualityLevel]) -> dict:
        d = self.get_hls_directory(video_file_id)
        d.mkdir(parents=True, exist_ok=True)
        return {q: self.get_quality_directory(video_file_id, q) for q in qualities}

    def write_master_playlist(self, video_file: VideoFile, qualities: List[VideoQuality]) -> Path:
        p = self.get_master_playlist_path(video_file.id)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.generate_master_playlist(video_file, qualities))
        return p

    def write_media_playlist(self, video_file_id: int, quality: QualityLevel, segment_duration: int = 6) -> Path:
        d = self.get_quality_directory(video_file_id, quality)
        p = d / "playlist.m3u8"
        p.write_text(self.generate_media_playlist(d, segment_duration))
        return p

hls_service = HLSService()
