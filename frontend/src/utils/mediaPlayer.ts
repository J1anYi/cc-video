// Advanced media player utilities

export interface VideoQuality {
  id: string;
  label: string;
  resolution: number;
  bitrate: number;
  url: string;
}

export interface AudioTrack {
  id: string;
  language: string;
  label: string;
  enabled: boolean;
}

export interface Chapter {
  id: number;
  title: string;
  startTime: number;
  endTime: number;
}

export const PLAYBACK_SPEEDS = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2];

export function isPictureInPictureSupported(): boolean {
  return 'pictureInPictureEnabled' in document && document.pictureInPictureEnabled;
}

export async function togglePictureInPicture(video: HTMLVideoElement): Promise<void> {
  if (document.pictureInPictureElement) {
    await document.exitPictureInPicture();
  } else if (document.pictureInPictureEnabled) {
    await video.requestPictureInPicture();
  }
}

export function setPlaybackSpeed(video: HTMLVideoElement, speed: number): void {
  video.playbackRate = speed;
}

export function getPlaybackSpeed(video: HTMLVideoElement): number {
  return video.playbackRate;
}

export function formatChapterTime(seconds: number): string {
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, '0')}`;
}

export function getCurrentChapter(time: number, chapters: Chapter[]): Chapter | null {
  for (const chapter of chapters) {
    if (time >= chapter.startTime && time < chapter.endTime) {
      return chapter;
    }
  }
  return null;
}

export function getAutoQuality(bandwidth: number, qualities: VideoQuality[]): VideoQuality {
  // Select quality based on available bandwidth
  const sorted = [...qualities].sort((a, b) => a.bitrate - b.bitrate);
  for (const quality of sorted) {
    if (quality.bitrate <= bandwidth) {
      return quality;
    }
  }
  return sorted[0]; // Lowest quality fallback
}
