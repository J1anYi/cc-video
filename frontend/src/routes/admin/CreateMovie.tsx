import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../auth/AuthContext';
import { createMovie } from '../../api/admin';

export default function CreateMovie() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleSave = async () => {
    if (!title.trim()) {
      setError('Title is required');
      return;
    }
    setSaving(true);
    try {
      const movie = await createMovie({ title, description, publication_status: 'DRAFT' });
      navigate(`/admin/movies/${movie.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <Link to="/admin/movies" style={styles.backLink}>Back</Link>
        <div style={styles.userSection}>
          <span>{user?.username}</span>
          <button onClick={logout} style={styles.logoutButton}>Logout</button>
        </div>
      </header>
      <h1 style={styles.title}>Create Movie</h1>
      {error && <div style={styles.error}>{error}</div>}
      <div style={styles.form}>
        <div style={styles.field}>
          <label style={styles.label}>Title *</label>
          <input value={title} onChange={(e) => setTitle(e.target.value)} style={styles.input} placeholder="Movie title" />
        </div>
        <div style={styles.field}>
          <label style={styles.label}>Description</label>
          <textarea value={description} onChange={(e) => setDescription(e.target.value)} style={styles.textarea} placeholder="Movie description" />
        </div>
        <button onClick={handleSave} disabled={saving} style={styles.saveButton}>{saving ? 'Creating...' : 'Create Movie'}</button>
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: { maxWidth: '800px', margin: '0 auto', padding: '1rem' },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', padding: '1rem 0', borderBottom: '1px solid #eee' },
  backLink: { color: '#007bff', textDecoration: 'none' },
  userSection: { display: 'flex', alignItems: 'center', gap: '1rem' },
  logoutButton: { padding: '0.5rem 1rem', background: '#6c757d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  title: { margin: '0 0 1rem' },
  error: { padding: '1rem', background: '#fee', color: '#c00', borderRadius: '4px', marginBottom: '1rem' },
  form: { display: 'flex', flexDirection: 'column', gap: '1rem' },
  field: { display: 'flex', flexDirection: 'column', gap: '0.5rem' },
  label: { fontWeight: '500' },
  input: { padding: '0.5rem', border: '1px solid #ddd', borderRadius: '4px' },
  textarea: { padding: '0.5rem', border: '1px solid #ddd', borderRadius: '4px', minHeight: '100px' },
  saveButton: { padding: '0.75rem', background: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
};
