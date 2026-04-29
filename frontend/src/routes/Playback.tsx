import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useAuth } from '../auth/AuthContext';
import { getMovie, getStreamUrl } from '../api/movies';
import type { Movie } from '../api/types';

export default function Playback() {
  const { id } = useParams<{ id: string }>();
  const [movie, setMovie] = useState<Movie | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const { user, logout } = useAuth();

  useEffect(() => {
    if (id) {
      loadMovie(parseInt(id));
    }
  }, [id]);

  const loadMovie = async (movieId: number) => {
    try {
      const data = await getMovie(movieId);
      setMovie(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load movie');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <div style={styles.container}><p>Loading movie...</p></div>;
  }

  if (error || !movie) {
    return (
      <div style={styles.container}>
        <div style={styles.error}>{error || 'Movie not found'}</div>
        <Link to="/movies" style={styles.backLink}>Back to Catalog</Link>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <Link to="/movies" style={styles.backLink}>Back to Catalog</Link>
        <div style={styles.userSection}>
          <span>{user?.username}</span>
          <button onClick={logout} style={styles.logoutButton}>Logout</button>
        </div>
      </header>

      <h1 style={styles.title}>{movie.title}</h1>
      {movie.description && <p style={styles.description}>{movie.description}</p>}

      <div style={styles.videoContainer}>
        <video controls style={styles.video} src={getStreamUrl(movie.id)}>
          Your browser does not support video playback.
        </video>
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: { maxWidth: '1000px', margin: '0 auto', padding: '1rem' },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', padding: '1rem 0', borderBottom: '1px solid #eee' },
  backLink: { color: '#007bff', textDecoration: 'none' },
  userSection: { display: 'flex', alignItems: 'center', gap: '1rem' },
  logoutButton: { padding: '0.5rem 1rem', background: '#6c757d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  title: { margin: '0 0 0.5rem', fontSize: '1.5rem' },
  description: { margin: '0 0 1.5rem', color: '#666' },
  videoContainer: { background: '#000', borderRadius: '8px', overflow: 'hidden' },
  video: { width: '100%', display: 'block' },
  error: { padding: '1rem', background: '#fee', color: '#c00', borderRadius: '4px', marginBottom: '1rem' },
};
