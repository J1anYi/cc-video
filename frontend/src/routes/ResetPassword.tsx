import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import { confirmPasswordReset } from '../api/passwordReset';

export default function ResetPassword() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const tokenParam = searchParams.get('token');
    if (!tokenParam) {
      setError('Invalid reset link. Please request a new password reset.');
    } else {
      setToken(tokenParam);
    }
  }, [searchParams]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Validate passwords
    if (password.length < 6) {
      setError('Password must be at least 6 characters long');
      return;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (!token) {
      setError('Invalid reset token');
      return;
    }

    setIsLoading(true);

    try {
      await confirmPasswordReset(token, password);
      setSuccess(true);
      setTimeout(() => navigate('/login'), 3000);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to reset password');
    } finally {
      setIsLoading(false);
    }
  };

  if (success) {
    return (
      <div style={styles.container}>
        <div style={styles.card}>
          <h1 style={styles.title}>CC Video</h1>
          <h2 style={styles.subtitle}>Password Reset</h2>
          <p style={styles.successText}>
            Your password has been reset successfully!
            Redirecting to login page...
          </p>
          <Link to="/login" style={styles.link}>Go to Login</Link>
        </div>
      </div>
    );
  }

  if (!token) {
    return (
      <div style={styles.container}>
        <div style={styles.card}>
          <h1 style={styles.title}>CC Video</h1>
          <h2 style={styles.subtitle}>Invalid Link</h2>
          <p style={styles.errorText}>
            This password reset link is invalid or has expired.
          </p>
          <Link to="/forgot-password" style={styles.link}>Request New Reset Link</Link>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>CC Video</h1>
        <h2 style={styles.subtitle}>Reset Password</h2>

        {error && <div style={styles.error}>{error}</div>}

        <form onSubmit={handleSubmit} style={styles.form}>
          <div style={styles.field}>
            <label style={styles.label}>New Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={styles.input}
              required
              placeholder="Enter new password (min 6 characters)"
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
              placeholder="Confirm new password"
            />
          </div>

          <button type="submit" style={styles.button} disabled={isLoading}>
            {isLoading ? 'Resetting...' : 'Reset Password'}
          </button>
        </form>

        <p style={styles.footer}>
          <Link to="/login" style={styles.link}>Back to Login</Link>
        </p>
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: '#f5f5f5',
  },
  card: {
    background: 'white',
    padding: '2rem',
    borderRadius: '8px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
    width: '100%',
    maxWidth: '400px',
  },
  title: {
    margin: '0 0 0.5rem',
    fontSize: '2rem',
    textAlign: 'center',
    color: '#333',
  },
  subtitle: {
    margin: '0 0 1.5rem',
    fontSize: '1rem',
    textAlign: 'center',
    color: '#666',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '1rem',
  },
  field: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.5rem',
  },
  label: {
    fontSize: '0.875rem',
    fontWeight: '500',
    color: '#333',
  },
  input: {
    padding: '0.75rem',
    border: '1px solid #ddd',
    borderRadius: '4px',
    fontSize: '1rem',
  },
  button: {
    padding: '0.75rem',
    background: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    fontSize: '1rem',
    cursor: 'pointer',
    marginTop: '0.5rem',
  },
  error: {
    padding: '0.75rem',
    background: '#fee',
    color: '#c00',
    borderRadius: '4px',
    marginBottom: '1rem',
  },
  successText: {
    textAlign: 'center',
    color: '#28a745',
    marginBottom: '1rem',
    lineHeight: '1.5',
  },
  errorText: {
    textAlign: 'center',
    color: '#c00',
    marginBottom: '1rem',
    lineHeight: '1.5',
  },
  footer: {
    marginTop: '1rem',
    textAlign: 'center',
    color: '#666',
    fontSize: '0.875rem',
  },
  link: {
    color: '#007bff',
    textDecoration: 'none',
  },
};
