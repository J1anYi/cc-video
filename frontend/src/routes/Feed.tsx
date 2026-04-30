import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { getActivityFeed } from '../api/activity';
import type { ActivityResponse } from '../api/activity';

export default function Feed() {
  const navigate = useNavigate();
  const [activities, setActivities] = useState<ActivityResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadFeed();
  }, []);

  const loadFeed = async () => {
    setIsLoading(true);
    try {
      const data = await getActivityFeed();
      setActivities(data.activities);
    } catch (err) {
      setError('Failed to load activity feed');
    } finally {
      setIsLoading(false);
    }
  };

  const formatActivity = (activity: ActivityResponse) => {
    switch (activity.activity_type) {
      case 'review_posted':
        return `wrote a review for`;
      case 'rating_added':
        return `rated`;
      default:
        return 'interacted with';
    }
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  };

  if (isLoading) {
    return <div style={styles.container}>Loading...</div>;
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Activity Feed</h1>

        {error && <div style={styles.error}>{error}</div>}

        {activities.length === 0 ? (
          <div style={styles.emptyState}>
            <p>No activities yet.</p>
            <p style={styles.hint}>Follow other users to see their reviews and ratings here!</p>
          </div>
        ) : (
          <div style={styles.activityList}>
            {activities.map((activity) => (
              <div key={activity.id} style={styles.activityItem}>
                <div style={styles.activityHeader}>
                  <Link to={`/users/${activity.user_id}`} style={styles.username}>
                    {activity.username || 'Anonymous'}
                  </Link>
                  <span style={styles.actionText}>{formatActivity(activity)}</span>
                  {activity.movie_id && activity.movie_title && (
                    <Link to={`/movies/${activity.movie_id}`} style={styles.movieTitle}>
                      {activity.movie_title}
                    </Link>
                  )}
                </div>
                <div style={styles.activityTime}>{formatDate(activity.created_at)}</div>
              </div>
            ))}
          </div>
        )}

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
  title: { margin: '0 0 1.5rem', fontSize: '1.5rem', color: '#333' },
  emptyState: { textAlign: 'center', padding: '2rem', color: '#666' },
  hint: { fontSize: '0.875rem', color: '#999' },
  activityList: { display: 'flex', flexDirection: 'column', gap: '1rem' },
  activityItem: { padding: '1rem', border: '1px solid #eee', borderRadius: '4px' },
  activityHeader: { display: 'flex', flexWrap: 'wrap', gap: '0.5rem', alignItems: 'center' },
  username: { fontWeight: 'bold', color: '#007bff', textDecoration: 'none' },
  actionText: { color: '#666' },
  movieTitle: { color: '#007bff', textDecoration: 'none', fontWeight: '500' },
  activityTime: { fontSize: '0.75rem', color: '#999', marginTop: '0.5rem' },
  backButton: { padding: '0.75rem', background: '#6c757d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', marginTop: '1.5rem' },
  error: { padding: '0.75rem', background: '#fee', color: '#c00', borderRadius: '4px', marginBottom: '1rem' },
};
