import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { getWatchlist, updateWatchlist, removeMovieFromWatchlist, type WatchlistDetailResponse, type MovieInWatchlist } from '../api/watchlist';

export default function WatchlistDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [watchlist, setWatchlist] = useState<WatchlistDetailResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [editName, setEditName] = useState('');
  const [editDescription, setEditDescription] = useState('');
  const [editIsPublic, setEditIsPublic] = useState(false);

  useEffect(() => {
    loadWatchlist();
  }, [id]);

  const loadWatchlist = async () => {
    if (!id) return;
    setIsLoading(true);
    try {
      const data = await getWatchlist(parseInt(id));
      setWatchlist(data);
      setEditName(data.name);
      setEditDescription(data.description || '');
      setEditIsPublic(data.is_public);
    } catch (err) {
      setError('Failed to load watchlist');
    } finally {
      setIsLoading(false);
    }
  };

  const handleUpdate = async () => {
    if (!id || !watchlist) return;
    try {
      const updated = await updateWatchlist(parseInt(id), {
        name: editName,
        description: editDescription || undefined,
        is_public: editIsPublic,
      });
      setWatchlist({ ...watchlist, name: updated.name, description: updated.description, is_public: updated.is_public });
      setIsEditing(false);
    } catch (err) {
      setError('Failed to update watchlist');
    }
  };

  const handleRemoveMovie = async (movieId: number) => {
    if (!id || !watchlist) return;
    try {
      await removeMovieFromWatchlist(parseInt(id), movieId);
      setWatchlist({
        ...watchlist,
        movies: watchlist.movies.filter(m => m.id !== movieId),
      });
    } catch (err) {
      setError('Failed to remove movie from watchlist');
    }
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString();
  };

  if (isLoading) {
    return <div style={styles.container}>Loading...</div>;
  }

  if (!watchlist) {
    return <div style={styles.container}>Watchlist not found</div>;
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        {isEditing ? (
          <div style={styles.editForm}>
            <input
              type="text"
              value={editName}
              onChange={(e) => setEditName(e.target.value)}
              style={styles.input}
              placeholder="Watchlist name"
            />
            <textarea
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              style={styles.textarea}
              placeholder="Description (optional)"
            />
            <label style={styles.checkboxLabel}>
              <input
                type="checkbox"
                checked={editIsPublic}
                onChange={(e) => setEditIsPublic(e.target.checked)}
              />
              Public watchlist
            </label>
            <div style={styles.editButtons}>
              <button onClick={() => setIsEditing(false)} style={styles.cancelButton}>
                Cancel
              </button>
              <button onClick={handleUpdate} style={styles.saveButton}>
                Save
              </button>
            </div>
          </div>
        ) : (
          <>
            <div>
              <h1 style={styles.title}>{watchlist.name}</h1>
              {watchlist.description && (
                <p style={styles.description}>{watchlist.description}</p>
              )}
              <div style={styles.meta}>
                <span style={watchlist.is_public ? styles.publicBadge : styles.privateBadge}>
                  {watchlist.is_public ? 'Public' : 'Private'}
                </span>
                <span>Created {formatDate(watchlist.created_at)}</span>
              </div>
            </div>
            <button onClick={() => setIsEditing(true)} style={styles.editButton}>
              Edit
            </button>
          </>
        )}
      </div>

      {error && <div style={styles.error}>{error}</div>}

      <h2 style={styles.sectionTitle}>Movies ({watchlist.movies.length})</h2>

      {watchlist.movies.length === 0 ? (
        <div style={styles.emptyState}>
          <p>No movies in this watchlist yet.</p>
          <button onClick={() => navigate('/movies')} style={styles.browseButton}>
            Browse Movies
          </button>
        </div>
      ) : (
        <div style={styles.movieGrid}>
          {watchlist.movies.map((movie) => (
            <MovieCard
              key={movie.id}
              movie={movie}
              onRemove={() => handleRemoveMovie(movie.id)}
              onClick={() => navigate(`/movies/${movie.id}`)}
            />
          ))}
        </div>
      )}

      <button onClick={() => navigate('/watchlists')} style={styles.backButton}>
        Back to Watchlists
      </button>
    </div>
  );
}

function MovieCard({ movie, onRemove, onClick }: { movie: MovieInWatchlist; onRemove: () => void; onClick: () => void }) {
  return (
    <div style={styles.movieCard} onClick={onClick}>
      <div style={styles.moviePoster}>
        {movie.poster_url ? (
          <img src={movie.poster_url} alt={movie.title} style={styles.posterImage} />
        ) : (
          <div style={styles.noPoster}>No Poster</div>
        )}
      </div>
      <div style={styles.movieInfo}>
        <h3 style={styles.movieTitle}>{movie.title}</h3>
        <button
          onClick={(e) => {
            e.stopPropagation();
            onRemove();
          }}
          style={styles.removeButton}
        >
          Remove
        </button>
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: { minHeight: '100vh', padding: '2rem', background: '#f5f5f5' },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '2rem', maxWidth: '1200px', margin: '0 auto 2rem', background: 'white', padding: '1.5rem', borderRadius: '8px' },
  title: { margin: 0, fontSize: '2rem', color: '#333' },
  description: { color: '#666', marginTop: '0.5rem', marginBottom: '0.5rem' },
  meta: { display: 'flex', alignItems: 'center', gap: '1rem', marginTop: '0.5rem' },
  publicBadge: { padding: '0.25rem 0.5rem', background: '#d4edda', color: '#155724', borderRadius: '4px', fontSize: '0.75rem' },
  privateBadge: { padding: '0.25rem 0.5rem', background: '#f8d7da', color: '#721c24', borderRadius: '4px', fontSize: '0.75rem' },
  editButton: { padding: '0.75rem 1.5rem', background: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  editForm: { width: '100%' },
  input: { width: '100%', padding: '0.75rem', border: '1px solid #ddd', borderRadius: '4px', fontSize: '1rem', marginBottom: '0.5rem', boxSizing: 'border-box' },
  textarea: { width: '100%', padding: '0.75rem', border: '1px solid #ddd', borderRadius: '4px', fontSize: '1rem', minHeight: '80px', marginBottom: '0.5rem', boxSizing: 'border-box' },
  checkboxLabel: { display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' },
  editButtons: { display: 'flex', justifyContent: 'flex-end', gap: '1rem' },
  cancelButton: { padding: '0.5rem 1rem', background: '#6c757d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  saveButton: { padding: '0.5rem 1rem', background: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  error: { padding: '1rem', background: '#fee', color: '#c00', borderRadius: '4px', marginBottom: '1rem', maxWidth: '1200px', margin: '0 auto 1rem' },
  sectionTitle: { fontSize: '1.5rem', marginBottom: '1rem', maxWidth: '1200px', margin: '0 auto 1rem' },
  emptyState: { textAlign: 'center', padding: '4rem', background: 'white', borderRadius: '8px', maxWidth: '600px', margin: '0 auto' },
  browseButton: { padding: '0.75rem 1.5rem', background: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', marginTop: '1rem' },
  movieGrid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: '1.5rem', maxWidth: '1200px', margin: '0 auto' },
  movieCard: { background: 'white', borderRadius: '8px', overflow: 'hidden', cursor: 'pointer', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' },
  moviePoster: { aspectRatio: '2/3', background: '#eee' },
  posterImage: { width: '100%', height: '100%', objectFit: 'cover' },
  noPoster: { display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: '#999' },
  movieInfo: { padding: '1rem' },
  movieTitle: { margin: 0, fontSize: '0.9rem', color: '#333', marginBottom: '0.5rem' },
  removeButton: { width: '100%', padding: '0.5rem', background: '#dc3545', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '0.85rem' },
  backButton: { display: 'block', margin: '2rem auto 0', padding: '0.75rem 1.5rem', background: '#6c757d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
};
