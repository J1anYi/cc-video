import { useState, useEffect, useRef, useCallback } from 'react';
import { useParams, Link, useSearchParams } from 'react-router-dom';
import Hls from 'hls.js';
import { useAuth } from '../auth/AuthContext';
import { getMovie } from '../api/movies';
import { updateWatchHistory } from '../api/history';
import { getMovieSubtitles } from '../api/subtitles';
import { QualitySelector, QualityOption } from '../components/VideoPlayer/QualitySelector';
import type { Movie, Subtitle } from '../api/types';

const API_BASE = 'http://localhost:8000';

export default function Playback() {
  const { id } = useParams<{ id: string }>();
  const [searchParams] = useSearchParams();
  const [movie, setMovie] = useState<Movie | null>(null);
  const [subtitles, setSubtitles] = useState<Subtitle[]>([]);
  const [selectedSubtitle, setSelectedSubtitle] = useState<Subtitle | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [qualities, setQualities] = useState<QualityOption[]>([]);
  const [currentQuality, setCurrentQuality] = useState('720p');
  const [isAuto, setIsAuto] = useState(true);
  const { user, logout } = useAuth();
  const videoRef = useRef<HTMLVideoElement>(null);
  const hlsRef = useRef<Hls | null>(null);

  useEffect(() => {
    if (id) loadMovie(parseInt(id));
    return () => {
      if (hlsRef.current) hlsRef.current.destroy();
    };
  }, [id]);

  const loadMovie = async (movieId: number) => {
    try {
      const [movieData, subtitleData] = await Promise.all([
        getMovie(movieId),
        getMovieSubtitles(movieId)
      ]);
      setMovie(movieData);
      setSubtitles(subtitleData.subtitles);
      if (subtitleData.subtitles.length > 0) {
        setSelectedSubtitle(subtitleData.subtitles[0]);
      }
      await initializeHls(movieId);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load movie');
    } finally {
      setIsLoading(false);
    }
  };

  const initializeHls = async (movieId: number) => {
    const video = videoRef.current;
    if (!video) return;

    if (Hls.isSupported()) {
      const hls = new Hls({ enableWorker: true });
      hlsRef.current = hls;
      hls.loadSource(API_BASE + '/api/hls/video/' + movieId + '/master.m3u8');
      hls.attachMedia(video);

      hls.on(Hls.Events.MANIFEST_PARSED, (_event, data) => {
        const qualityOptions: QualityOption[] = data.levels.map((level) => ({
          quality: level.name || String(level.height) + 'p',
          width: level.width,
          height: level.height,
          bitrate: level.bitrate,
        }));
        setQualities(qualityOptions);
        video.play().catch(() => {});
      });

      hls.on(Hls.Events.LEVEL_SWITCHED, (_event, data) => {
        const level = hls.levels[data.level];
        setCurrentQuality(level.name || String(level.height) + 'p');
      });
    } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
      video.src = API_BASE + '/api/hls/video/' + movieId + '/master.m3u8';
    } else {
      setError('HLS is not supported in this browser');
    }
  };

  const handleQualityChange = useCallback((quality: string) => {
    const hls = hlsRef.current;
    if (!hls) return;
    const levelIndex = hls.levels.findIndex(
      level => level.name === quality || String(level.height) + 'p' === quality
    );
    if (levelIndex !== -1) {
      hls.currentLevel = levelIndex;
      setIsAuto(false);
    }
  }, []);

  const handleAutoToggle = useCallback(() => {
    const hls = hlsRef.current;
    if (hls) {
      hls.currentLevel = -1;
      setIsAuto(true);
    }
  }, []);

  const getSubtitleUrl = (subtitle: Subtitle) => {
    const filename = subtitle.file_path.split('/').pop();
    return API_BASE + '/uploads/subtitles/' + filename;
  };

  if (isLoading) return <div style={styles.container}><p>Loading...</p></div>;
  if (error || !movie) return <div style={styles.container}><div style={styles.error}>{error || 'Not found'}</div></div>;

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <Link to="/movies">Back</Link>
        <div><span>{user?.username}</span><button onClick={logout}>Logout</button></div>
      </header>
      <h1>{movie.title}</h1>
      {movie.description && <p style={styles.desc}>{movie.description}</p>}
      <div style={styles.playerControls}>
        {qualities.length > 0 && (
          <QualitySelector
            qualities={qualities}
            currentQuality={currentQuality}
            onQualityChange={handleQualityChange}
            isAuto={isAuto}
            onAutoToggle={handleAutoToggle}
          />
        )}
      </div>
      <video ref={videoRef} controls style={styles.video}>
        {selectedSubtitle && (
          <track kind="subtitles" src={getSubtitleUrl(selectedSubtitle)} srcLang={selectedSubtitle.language} label={selectedSubtitle.language} default />
        )}
      </video>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: { maxWidth: '1000px', margin: '0 auto', padding: '1rem' },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' },
  desc: { color: '#666' },
  playerControls: { display: 'flex', gap: '1rem', marginBottom: '1rem' },
  video: { width: '100%', background: '#000' },
  error: { padding: '1rem', background: '#fee', color: '#c00' },
};
