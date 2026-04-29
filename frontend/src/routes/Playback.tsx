import { useState, useEffect, useRef } from 'react';
import { useParams, Link, useSearchParams } from 'react-router-dom';
import { useAuth } from '../auth/AuthContext';
import { getMovie, getStreamUrl } from '../api/movies';
import { updateWatchHistory } from '../api/history';
import type { Movie } from '../api/types';

export default function Playback() {
  const { id } = useParams<{ id: string }>();
  const [searchParams] = useSearchParams();
  const [movie, setMovie] = useState<Movie | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const { user, logout } = useAuth();
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    if (id) loadMovie(parseInt(id));
    return () => { if (movie) saveProgress(); };
  }, [id]);

  const loadMovie = async (movieId: number) => {
    try {
      const data = await getMovie(movieId);
      setMovie(data);
      const progress = searchParams.get('t');
      if (progress && videoRef.current) {
        videoRef.current.addEventListener('loadedmetadata', () => {
          const startPercent = parseInt(progress);
          videoRef.current!.currentTime = videoRef.current!.duration * (startPercent / 100);
        });
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load movie');
    } finally {
      setIsLoading(false);
    }
  };

  const saveProgress = async () => {
    if (!videoRef.current || !movie) return;
    const progress = Math.round((videoRef.current.currentTime / videoRef.current.duration) * 100);
    if (progress > 0) await updateWatchHistory(movie.id, progress);
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
      <video ref={videoRef} controls style={styles.video} src={getStreamUrl(movie.id)} onPause={saveProgress} onEnded={saveProgress} />
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: { maxWidth: '1000px', margin: '0 auto', padding: '1rem' },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' },
  desc: { color: '#666' },
  video: { width: '100%', background: '#000' },
  error: { padding: '1rem', background: '#fee', color: '#c00' },
};
