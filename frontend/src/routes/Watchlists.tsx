import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getWatchlists, createWatchlist, deleteWatchlist, type WatchlistResponse, type WatchlistCreate } from '../api/watchlist';

export default function Watchlists() {
  const navigate = useNavigate();
  const [watchlists, setWatchlists] = useState<WatchlistResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newName, setNewName] = useState('');
  const [newDescription, setNewDescription] = useState('');
  const [newIsPublic, setNewIsPublic] = useState(false);

  useEffect(() => {
    loadWatchlists();
  }, []);

  const loadWatchlists = async () => {
    setIsLoading(true);
    try {
      const data = await getWatchlists();
      setWatchlists(data.watchlists);
    } catch (err) {
      setError('Failed to load watchlists');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreate = async () => {
    if (!newName.trim()) return;
    try {
      const data: WatchlistCreate = {
        name: newName,
        description: newDescription || undefined,
        is_public: newIsPublic,
      };
      const watchlist = await createWatchlist(data);
      setWatchlists([...watchlists, watchlist]);
      setShowCreateModal(false);
      setNewName('');
      setNewDescription('');
      setNewIsPublic(false);
    } catch (err) {
      setError('Failed to create watchlist');
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this watchlist?')) return;
    try {
      await deleteWatchlist(id);
      setWatchlists(watchlists.filter(w => w.id !== id));
    } catch (err) {
      setError('Failed to delete watchlist');
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
      <div style={styles.header}>
        <h1 style={styles.title}>My Watchlists</h1>
        <button onClick={() => setShowCreateModal(true)} style={styles.createButton}>
          Create Watchlist
        </button>
      </div>

      {error && <div style={styles.error}>{error}</div>}

      {watchlists.length === 0 ? (
        <div style={styles.emptyState}>
          <p>You haven't created any watchlists yet.</p>
          <button onClick={() => setShowCreateModal(true)} style={styles.createButton}>
            Create Your First Watchlist
          </button>
        </div>
      ) : (
        <div style={styles.grid}>
          {watchlists.map((watchlist) => (
            <div
              key={watchlist.id}
              style={styles.card}
              onClick={() => navigate(`/watchlists/${watchlist.id}`)}
            >
              <div style={styles.cardHeader}>
                <h3 style={styles.cardTitle}>{watchlist.name}</h3>
                <span style={watchlist.is_public ? styles.publicBadge : styles.privateBadge}>
                  {watchlist.is_public ? 'Public' : 'Private'}
                </span>
              </div>
              {watchlist.description && (
                <p style={styles.cardDescription}>{watchlist.description}</p>
              )}
              <div style={styles.cardFooter}>
                <span>{watchlist.movie_count} movies</span>
                <span>Created {formatDate(watchlist.created_at)}</span>
              </div>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleDelete(watchlist.id);
                }}
                style={styles.deleteButton}
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      )}

      <button onClick={() => navigate('/movies')} style={styles.backButton}>
        Back to Movies
      </button>

      {showCreateModal && (
        <div style={styles.modalOverlay}>
          <div style={styles.modal}>
            <h2 style={styles.modalTitle}>Create New Watchlist</h2>
            <div style={styles.formGroup}>
              <label style={styles.label}>Name *</label>
              <input
                type="text"
                value={newName}
                onChange={(e) => setNewName(e.target.value)}
                style={styles.input}
                placeholder="Enter watchlist name"
              />
            </div>
            <div style={styles.formGroup}>
              <label style={styles.label}>Description</label>
              <textarea
                value={newDescription}
                onChange={(e) => setNewDescription(e.target.value)}
                style={styles.textarea}
                placeholder="Optional description"
              />
            </div>
            <div style={styles.formGroup}>
              <label style={styles.checkboxLabel}>
                <input
                  type="checkbox"
                  checked={newIsPublic}
                  onChange={(e) => setNewIsPublic(e.target.checked)}
                />
                Make this watchlist public
              </label>
            </div>
            <div style={styles.modalButtons}>
              <button onClick={() => setShowCreateModal(false)} style={styles.cancelButton}>
                Cancel
              </button>
              <button onClick={handleCreate} style={styles.saveButton}>
                Create
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: { minHeight: '100vh', padding: '2rem', background: '#f5f5f5' },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem', maxWidth: '1200px', margin: '0 auto 2rem' },
  title: { margin: 0, fontSize: '2rem', color: '#333' },
  createButton: { padding: '0.75rem 1.5rem', background: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '1rem' },
  error: { padding: '1rem', background: '#fee', color: '#c00', borderRadius: '4px', marginBottom: '1rem', maxWidth: '1200px', margin: '0 auto 1rem' },
  emptyState: { textAlign: 'center', padding: '4rem', background: 'white', borderRadius: '8px', maxWidth: '600px', margin: '0 auto' },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1.5rem', maxWidth: '1200px', margin: '0 auto' },
  card: { background: 'white', padding: '1.5rem', borderRadius: '8px', cursor: 'pointer', transition: 'transform 0.2s', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' },
  cardHeader: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' },
  cardTitle: { margin: 0, fontSize: '1.25rem', color: '#333' },
  publicBadge: { padding: '0.25rem 0.5rem', background: '#d4edda', color: '#155724', borderRadius: '4px', fontSize: '0.75rem' },
  privateBadge: { padding: '0.25rem 0.5rem', background: '#f8d7da', color: '#721c24', borderRadius: '4px', fontSize: '0.75rem' },
  cardDescription: { color: '#666', fontSize: '0.9rem', marginBottom: '1rem' },
  cardFooter: { display: 'flex', justifyContent: 'space-between', color: '#888', fontSize: '0.85rem' },
  deleteButton: { marginTop: '1rem', padding: '0.5rem 1rem', background: '#dc3545', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', width: '100%' },
  backButton: { display: 'block', margin: '2rem auto 0', padding: '0.75rem 1.5rem', background: '#6c757d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  modalOverlay: { position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center' },
  modal: { background: 'white', padding: '2rem', borderRadius: '8px', width: '400px', maxWidth: '90%' },
  modalTitle: { margin: '0 0 1.5rem', fontSize: '1.5rem' },
  formGroup: { marginBottom: '1rem' },
  label: { display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' },
  input: { width: '100%', padding: '0.75rem', border: '1px solid #ddd', borderRadius: '4px', fontSize: '1rem', boxSizing: 'border-box' },
  textarea: { width: '100%', padding: '0.75rem', border: '1px solid #ddd', borderRadius: '4px', fontSize: '1rem', minHeight: '80px', resize: 'vertical', boxSizing: 'border-box' },
  checkboxLabel: { display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' },
  modalButtons: { display: 'flex', justifyContent: 'flex-end', gap: '1rem', marginTop: '1.5rem' },
  cancelButton: { padding: '0.75rem 1.5rem', background: '#6c757d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  saveButton: { padding: '0.75rem 1.5rem', background: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
};
