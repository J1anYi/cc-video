import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../auth/AuthContext';
import { getAdminMovies, deleteMovie } from '../../api/admin';
import type { Movie } from '../../api/types';

export default function AdminMovies() {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const { user, logout } = useAuth();

  useEffect(() => { loadMovies(); }, []);

  const loadMovies = async () => {
    try {
      const response = await getAdminMovies();
      setMovies(response.movies);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load movies');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Delete this movie?')) return;
    try {
      await deleteMovie(id);
      setMovies(movies.filter((m) => m.id !== id));
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to delete');
    }
  };

  const getStatusStyle = (status: string): React.CSSProperties => ({
    background: { PUBLISHED: '#28a745', DRAFT: '#6c757d', UNPUBLISHED: '#ffc107', DISABLED: '#dc3545' }[status] || '#6c757d',
    padding: '0.25rem 0.5rem', borderRadius: '4px', color: 'white', fontSize: '0.75rem',
  });

  if (isLoading) return <div style={styles.container}><p>Loading...</p></div>;

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.title}>Admin - Movies</h1>
        <div style={styles.userSection}>
          <span>{user?.username}</span>
          <button onClick={logout} style={styles.logoutButton}>Logout</button>
        </div>
      </header>
      {error && <div style={styles.error}>{error}</div>}
      <div style={styles.toolbar}>
        <Link to="/admin/movies/new" style={styles.createButton}>Create Movie</Link>
        <Link to="/movies" style={styles.link}>View Catalog</Link>
      </div>
      {movies.length === 0 ? <p style={styles.empty}>No movies yet.</p> : (
        <table style={styles.table}>
          <thead><tr><th style={styles.th}>ID</th><th style={styles.th}>Title</th><th style={styles.th}>Status</th><th style={styles.th}>Actions</th></tr></thead>
          <tbody>{movies.map((m) => (
            <tr key={m.id}>
              <td style={styles.td}>{m.id}</td>
              <td style={styles.td}>{m.title}</td>
              <td style={styles.td}><span style={getStatusStyle(m.publication_status)}>{m.publication_status}</span></td>
              <td style={styles.td}>
                <Link to={`/admin/movies/${m.id}`} style={styles.editLink}>Edit</Link>
                <button onClick={() => handleDelete(m.id)} style={styles.deleteButton}>Delete</button>
              </td>
            </tr>
          ))}</tbody>
        </table>
      )}
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: { maxWidth: '1200px', margin: '0 auto', padding: '1rem' },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', padding: '1rem 0', borderBottom: '1px solid #eee' },
  title: { margin: 0, fontSize: '1.5rem' },
  userSection: { display: 'flex', alignItems: 'center', gap: '1rem' },
  logoutButton: { padding: '0.5rem 1rem', background: '#6c757d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  error: { padding: '1rem', background: '#fee', color: '#c00', borderRadius: '4px', marginBottom: '1rem' },
  toolbar: { display: 'flex', gap: '1rem', marginBottom: '1rem' },
  createButton: { padding: '0.5rem 1rem', background: '#28a745', color: 'white', textDecoration: 'none', borderRadius: '4px' },
  link: { color: '#007bff', textDecoration: 'none', lineHeight: '2rem' },
  empty: { textAlign: 'center', color: '#666', padding: '2rem' },
  table: { width: '100%', borderCollapse: 'collapse' },
  th: { textAlign: 'left', padding: '0.75rem', borderBottom: '2px solid #eee' },
  td: { padding: '0.75rem', borderBottom: '1px solid #eee' },
  editLink: { color: '#007bff', marginRight: '0.5rem', textDecoration: 'none' },
  deleteButton: { padding: '0.25rem 0.5rem', background: '#dc3545', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
};
