import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../auth/AuthContext';
import { getAdminMovie, updateMovie, uploadVideo } from '../../api/admin';
import type { Movie } from '../../api/types';

export default function EditMovie() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [movie, setMovie] = useState<Movie | null>(null);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState<string>('DRAFT');
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const { user, logout } = useAuth();

  useEffect(() => {
    if (id) loadMovie(parseInt(id));
  }, [id]);

  const loadMovie = async (movieId: number) => {
    try {
      const data = await getAdminMovie(movieId);
      setMovie(data);
      setTitle(data.title);
      setDescription(data.description || '');
      setStatus(data.publication_status);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load movie');
    }
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await updateMovie(parseInt(id!), { title, description, publication_status: status as any });
      navigate('/admin/movies');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save');
    } finally {
      setSaving(false);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    try {
      await uploadVideo(parseInt(id!), file);
      alert('Video uploaded!');
      setFile(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  if (error && !movie) return <div style={styles.container}><div style={styles.error}>{error}</div></div>;

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <Link to="/admin/movies" style={styles.backLink}>Back</Link>
        <div style={styles.userSection}>
          <span>{user?.username}</span>
          <button onClick={logout} style={styles.logoutButton}>Logout</button>
        </div>
      </header>
      <h1 style={styles.title}>Edit Movie</h1>
      {error && <div style={styles.error}>{error}</div>}
      <div style={styles.form}>
        <div style={styles.field}>
          <label style={styles.label}>Title</label>
          <input value={title} onChange={(e) => setTitle(e.target.value)} style={styles.input} />
        </div>
        <div style={styles.field}>
          <label style={styles.label}>Description</label>
          <textarea value={description} onChange={(e) => setDescription(e.target.value)} style={styles.textarea} />
        </div>
        <div style={styles.field}>
          <label style={styles.label}>Status</label>
          <select value={status} onChange={(e) => setStatus(e.target.value)} style={styles.select}>
            <option value="DRAFT">Draft</option>
            <option value="PUBLISHED">Published</option>
            <option value="UNPUBLISHED">Unpublished</option>
            <option value="DISABLED">Disabled</option>
          </select>
        </div>
        <button onClick={handleSave} disabled={saving} style={styles.saveButton}>{saving ? 'Saving...' : 'Save'}</button>

        <h2 style={styles.subtitle}>Upload Video</h2>
        <input type="file" accept="video/*" onChange={(e) => setFile(e.target.files?.[0] || null)} style={styles.fileInput} />
        <button onClick={handleUpload} disabled={!file || uploading} style={styles.uploadButton}>{uploading ? 'Uploading...' : 'Upload Video'}</button>
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
  subtitle: { margin: '2rem 0 1rem', fontSize: '1.25rem' },
  error: { padding: '1rem', background: '#fee', color: '#c00', borderRadius: '4px', marginBottom: '1rem' },
  form: { display: 'flex', flexDirection: 'column', gap: '1rem' },
  field: { display: 'flex', flexDirection: 'column', gap: '0.5rem' },
  label: { fontWeight: '500' },
  input: { padding: '0.5rem', border: '1px solid #ddd', borderRadius: '4px' },
  textarea: { padding: '0.5rem', border: '1px solid #ddd', borderRadius: '4px', minHeight: '100px' },
  select: { padding: '0.5rem', border: '1px solid #ddd', borderRadius: '4px' },
  saveButton: { padding: '0.75rem', background: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  fileInput: { padding: '0.5rem' },
  uploadButton: { padding: '0.75rem', background: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
};
