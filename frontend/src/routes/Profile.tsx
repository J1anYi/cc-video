import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchApi } from '../api/auth';

interface UserProfile {
  id: number;
  email: string;
  display_name: string | null;
  role: string;
  created_at: string;
}

export default function Profile() {
  const navigate = useNavigate();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [displayName, setDisplayName] = useState('');
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const data = await fetchApi<UserProfile>('/users/me');
      setProfile(data);
      setDisplayName(data.display_name || '');
    } catch (err) {
      setError('Failed to load profile');
    }
  };

  const handleUpdateProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setIsLoading(true);

    try {
      await fetchApi('/users/me', {
        method: 'PUT',
        body: JSON.stringify({ display_name: displayName }),
      });
      setSuccess('Profile updated successfully');
      loadProfile();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update profile');
    } finally {
      setIsLoading(false);
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (newPassword !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (newPassword.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    setIsLoading(true);

    try {
      await fetchApi('/users/me/password', {
        method: 'POST',
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
        }),
      });
      setSuccess('Password changed successfully');
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to change password');
    } finally {
      setIsLoading(false);
    }
  };

  if (!profile) {
    return <div style={styles.container}>Loading...</div>;
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Profile</h1>

        {error && <div style={styles.error}>{error}</div>}
        {success && <div style={styles.success}>{success}</div>}

        <div style={styles.section}>
          <h2 style={styles.subtitle}>Account Information</h2>
          <p><strong>Email:</strong> {profile.email}</p>
          <p><strong>Role:</strong> {profile.role}</p>
        </div>

        <form onSubmit={handleUpdateProfile} style={styles.form}>
          <h2 style={styles.subtitle}>Update Display Name</h2>
          <div style={styles.field}>
            <label style={styles.label}>Display Name</label>
            <input
              type="text"
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              style={styles.input}
              placeholder="Enter display name"
            />
          </div>
          <button type="submit" style={styles.button} disabled={isLoading}>
            {isLoading ? 'Saving...' : 'Save Display Name'}
          </button>
        </form>

        <form onSubmit={handleChangePassword} style={styles.form}>
          <h2 style={styles.subtitle}>Change Password</h2>
          <div style={styles.field}>
            <label style={styles.label}>Current Password</label>
            <input
              type="password"
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              style={styles.input}
              required
            />
          </div>
          <div style={styles.field}>
            <label style={styles.label}>New Password</label>
            <input
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              style={styles.input}
              required
            />
          </div>
          <div style={styles.field}>
            <label style={styles.label}>Confirm Password</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              style={styles.input}
              required
            />
          </div>
          <button type="submit" style={styles.button} disabled={isLoading}>
            {isLoading ? 'Changing...' : 'Change Password'}
          </button>
        </form>

        <button onClick={() => navigate('/movies')} style={styles.backButton}>
          Back to Movies
        </button>
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: { minHeight: '100vh', padding: '2rem', background: '#f5f5f5' },
  card: { background: 'white', padding: '2rem', borderRadius: '8px', maxWidth: '600px', margin: '0 auto' },
  title: { margin: '0 0 1rem', fontSize: '1.5rem', color: '#333' },
  subtitle: { margin: '1.5rem 0 1rem', fontSize: '1.1rem', color: '#666' },
  section: { marginBottom: '1rem' },
  form: { display: 'flex', flexDirection: 'column', gap: '1rem', marginBottom: '1rem' },
  field: { display: 'flex', flexDirection: 'column', gap: '0.5rem' },
  label: { fontSize: '0.875rem', fontWeight: '500', color: '#333' },
  input: { padding: '0.75rem', border: '1px solid #ddd', borderRadius: '4px', fontSize: '1rem' },
  button: { padding: '0.75rem', background: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  backButton: { padding: '0.75rem', background: '#6c757d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', marginTop: '1rem' },
  error: { padding: '0.75rem', background: '#fee', color: '#c00', borderRadius: '4px', marginBottom: '1rem' },
  success: { padding: '0.75rem', background: '#d4edda', color: '#155724', borderRadius: '4px', marginBottom: '1rem' },
};
