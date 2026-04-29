import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getPublicProfile } from '../api/profile';
import type { PublicProfileResponse } from '../api/profile';
import { getFollowStatus, followUser, unfollowUser } from '../api/follow';
import { useAuth } from '../auth/AuthContext';

export default function UserProfile() {
  const { userId } = useParams<{ userId: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [profile, setProfile] = useState<PublicProfileResponse | null>(null);
  const [isFollowing, setIsFollowing] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (userId) {
      loadProfile();
    }
  }, [userId]);

  const loadProfile = async () => {
    if (!userId) return;
    setIsLoading(true);
    try {
      const [profileData, followStatus] = await Promise.all([
        getPublicProfile(parseInt(userId)),
        getFollowStatus(parseInt(userId)),
      ]);
      setProfile(profileData);
      setIsFollowing(followStatus.is_following);
    } catch (err) {
      setError('Failed to load profile');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFollowToggle = async () => {
    if (!userId) return;
    try {
      if (isFollowing) {
        await unfollowUser(parseInt(userId));
        setIsFollowing(false);
        if (profile) {
          setProfile({
            ...profile,
            followers_count: profile.followers_count - 1,
          });
        }
      } else {
        await followUser(parseInt(userId));
        setIsFollowing(true);
        if (profile) {
          setProfile({
            ...profile,
            followers_count: profile.followers_count + 1,
          });
        }
      }
    } catch (err) {
      setError('Failed to update follow status');
    }
  };

  if (isLoading) {
    return <div style={styles.container}>Loading...</div>;
  }

  if (!profile) {
    return <div style={styles.container}>User not found</div>;
  }

  const isOwnProfile = user?.id === parseInt(userId || '0');

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        {error && <div style={styles.error}>{error}</div>}

        <div style={styles.header}>
          <h1 style={styles.title}>{profile.display_name || 'Anonymous User'}</h1>
          {!isOwnProfile && (
            <button
              onClick={handleFollowToggle}
              style={{
                ...styles.followButton,
                background: isFollowing ? '#6c757d' : '#007bff',
              }}
            >
              {isFollowing ? 'Unfollow' : 'Follow'}
            </button>
          )}
        </div>

        <div style={styles.stats}>
          <div style={styles.statItem}>
            <span style={styles.statNumber}>{profile.followers_count}</span>
            <span style={styles.statLabel}>Followers</span>
          </div>
          <div style={styles.statItem}>
            <span style={styles.statNumber}>{profile.following_count}</span>
            <span style={styles.statLabel}>Following</span>
          </div>
          <div style={styles.statItem}>
            <span style={styles.statNumber}>{profile.review_count}</span>
            <span style={styles.statLabel}>Reviews</span>
          </div>
          <div style={styles.statItem}>
            <span style={styles.statNumber}>{profile.rating_count}</span>
            <span style={styles.statLabel}>Ratings</span>
          </div>
        </div>

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
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' },
  title: { margin: 0, fontSize: '1.5rem', color: '#333' },
  followButton: { padding: '0.5rem 1.5rem', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  stats: { display: 'flex', gap: '2rem', marginBottom: '1.5rem' },
  statItem: { display: 'flex', flexDirection: 'column', alignItems: 'center' },
  statNumber: { fontSize: '1.5rem', fontWeight: 'bold', color: '#333' },
  statLabel: { fontSize: '0.875rem', color: '#666' },
  backButton: { padding: '0.75rem', background: '#6c757d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  error: { padding: '0.75rem', background: '#fee', color: '#c00', borderRadius: '4px', marginBottom: '1rem' },
};
