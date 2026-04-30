import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getPublicWatchlists, type PublicWatchlistResponse } from '../api/watchlist';

export default function PublicWatchlists() {
  const navigate = useNavigate();
  const [watchlists, setWatchlists] = useState<PublicWatchlistResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadWatchlists();
  }, []);

  const loadWatchlists = async () => {
    setIsLoading(true);
    try {
      const data = await getPublicWatchlists();
      setWatchlists(data);
    } catch (err) {
      setError('Failed to load public watchlists');
    } finally {
      setIsLoading(false);
    }
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString();
  };

  if (isLoading) {
    return <div style={styles.container}>Loading...</div>;
  }

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Discover Watchlists</h1>
      {error && <div style={styles.error}>{error}</div>}

      {watchlists.length === 0 ? (
        <div style={styles.emptyState}>
          <p>No public watchlists yet.</p>
        </div>
      ) : (
        <div style={styles.grid}>
          {watchlists.map((watchlist) => (
            <div
              key={watchlist.id}
              style={styles.card}
              onClick={() => navigate(`/watchlists/${watchlist.id}/public`)}
            >
              <h3 style={styles.cardTitle}>{watchlist.name}</h3>
              {watchlist.description && (
                <p style={styles.cardDescription}>{watchlist.description}</p>
              )}
              <div style={styles.cardFooter}>
                <span>by {watchlist.user_name || 'Unknown'}</span>
                <span>{watchlist.movie_count} movies</span>
              </div>
              <div style={styles.cardDate}>Created {formatDate(watchlist.created_at)}</div>
            </div>
          ))}
        </div>
      )}

      <button onClick={() => navigate('/movies')} style={styles.backButton}>
        Back to Movies
      </button>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: { minHeight: '100vh', padding: '2rem', background: '#f5f5f5' },
  title: { margin: '0 0 2rem', fontSize: '2rem', color: '#333', textAlign: 'center' },
  error: { padding: '1rem', background: '#fee', color: '#c00', borderRadius: '4px', marginBottom: '1rem' },
  emptyState: { textAlign: 'center', padding: '4rem', background: 'white', borderRadius: '8px' },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1.5rem', maxWidth: '1200px', margin: '0 auto' },
  card: { background: 'white', padding: '1.5rem', borderRadius: '8px', cursor: 'pointer', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' },
  cardTitle: { margin: '0 0 0.5rem', fontSize: '1.25rem', color: '#333' },
  cardDescription: { color: '#666', fontSize: '0.9rem', marginBottom: '1rem' },
  cardFooter: { display: 'flex', justifyContent: 'space-between', color: '#888', fontSize: '0.85rem', marginBottom: '0.5rem' },
  cardDate: { color: '#999', fontSize: '0.75rem' },
  backButton: { display: 'block', margin: '2rem auto 0', padding: '0.75rem 1.5rem', background: '#6c757d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
};
