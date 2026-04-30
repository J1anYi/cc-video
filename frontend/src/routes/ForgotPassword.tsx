import { useState } from 'react';
import { Link } from 'react-router-dom';
import { requestPasswordReset } from '../api/passwordReset';

export default function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await requestPasswordReset(email);
      setSuccess(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to request password reset');
    } finally {
      setIsLoading(false);
    }
  };

  if (success) {
    return (
      <div style={styles.container}>
        <div style={styles.card}>
          <h1 style={styles.title}>CC Video</h1>
          <h2 style={styles.subtitle}>Check Your Email</h2>
          <p style={styles.successText}>
            If the email exists in our system, a password reset link has been sent.
            Please check your inbox and follow the instructions.
          </p>
          <Link to="/login" style={styles.link}>Back to Login</Link>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>CC Video</h1>
        <h2 style={styles.subtitle}>Forgot Password</h2>

        {error && <div style={styles.error}>{error}</div>}

        <form onSubmit={handleSubmit} style={styles.form}>
          <div style={styles.field}>
            <label style={styles.label}>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={styles.input}
              required
              placeholder="Enter your email address"
            />
          </div>

          <button type="submit" style={styles.button} disabled={isLoading}>
            {isLoading ? 'Sending...' : 'Send Reset Link'}
          </button>
        </form>

        <p style={styles.footer}>
          Remember your password? <Link to="/login" style={styles.link}>Login</Link>
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
    color: '#666',
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
