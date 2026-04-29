import { useState, useEffect } from 'react';
import { getMovieRating, setRating, deleteRating } from '../api/ratings';
import type { MovieRatingStats } from '../api/ratings';
import { useAuth } from '../auth/AuthContext';

interface RatingProps {
  movieId: number;
}

export default function Rating({ movieId }: RatingProps) {
  const [stats, setStats] = useState<MovieRatingStats | null>(null);
  const [hoveredRating, setHoveredRating] = useState(0);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    loadRating();
  }, [movieId, user]);

  const loadRating = async () => {
    try {
      const data = await getMovieRating(movieId);
      setStats(data);
    } catch (err) {
      console.error('Failed to load rating:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRate = async (rating: number) => {
    if (!user) return;
    try {
      await setRating(movieId, rating);
      await loadRating();
    } catch (err) {
      console.error('Failed to set rating:', err);
    }
  };

  const handleClear = async () => {
    if (!user) return;
    try {
      await deleteRating(movieId);
      await loadRating();
    } catch (err) {
      console.error('Failed to delete rating:', err);
    }
  };

  if (loading) return <div>Loading rating...</div>;

  return (
    <div style={styles.container}>
      <div style={styles.stars}>
        {[1, 2, 3, 4, 5].map((star) => (
          <span
            key={star}
            style={{
              ...styles.star,
              color: (hoveredRating || stats?.user_rating || 0) >= star ? '#ffc107' : '#e0e0e0',
              cursor: user ? 'pointer' : 'default',
            }}
            onMouseEnter={() => user && setHoveredRating(star)}
            onMouseLeave={() => setHoveredRating(0)}
            onClick={() => handleRate(star)}
          >
            ★
          </span>
        ))}
        {stats?.user_rating && user && (
          <button onClick={handleClear} style={styles.clearButton}>Clear</button>
        )}
      </div>
      {stats && (
        <div style={styles.stats}>
          {stats.average_rating && (
            <span>{stats.average_rating.toFixed(1)} avg</span>
          )}
          <span style={styles.count}>({stats.rating_count} rating{stats.rating_count !== 1 ? 's' : ''})</span>
        </div>
      )}
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: { display: 'flex', flexDirection: 'column', gap: '0.5rem' },
  stars: { display: 'flex', alignItems: 'center', gap: '0.25rem' },
  star: { fontSize: '1.5rem', transition: 'color 0.15s' },
  clearButton: { marginLeft: '0.5rem', padding: '0.25rem 0.5rem', background: '#e0e0e0', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '0.75rem' },
  stats: { display: 'flex', gap: '0.5rem', fontSize: '0.875rem', color: '#666' },
  count: { color: '#999' },
};
