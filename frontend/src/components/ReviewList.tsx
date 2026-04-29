import { useState, useEffect } from 'react';
import { getMovieReviews, createReview, deleteReview } from '../api/reviews';
import type { ReviewResponse } from '../api/reviews';
import { useAuth } from '../auth/AuthContext';

interface ReviewListProps {
  movieId: number;
}

export default function ReviewList({ movieId }: ReviewListProps) {
  const [reviews, setReviews] = useState<ReviewResponse[]>([]);
  const [total, setTotal] = useState(0);
  const [newReview, setNewReview] = useState('');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const { user } = useAuth();

  useEffect(() => {
    loadReviews();
  }, [movieId]);

  const loadReviews = async () => {
    try {
      const data = await getMovieReviews(movieId);
      setReviews(data.reviews);
      setTotal(data.total);
    } catch (err) {
      console.error('Failed to load reviews:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newReview.trim()) return;
    setSubmitting(true);
    try {
      await createReview(movieId, newReview.trim());
      setNewReview('');
      await loadReviews();
    } catch (err) {
      console.error('Failed to create review:', err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (reviewId: number) => {
    try {
      await deleteReview(reviewId);
      await loadReviews();
    } catch (err) {
      console.error('Failed to delete review:', err);
    }
  };

  if (loading) return <div>Loading reviews...</div>;

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>Reviews ({total})</h3>

      {user && (
        <form onSubmit={handleSubmit} style={styles.form}>
          <textarea
            value={newReview}
            onChange={(e) => setNewReview(e.target.value)}
            placeholder="Write a review..."
            style={styles.textarea}
            rows={3}
          />
          <button type="submit" disabled={submitting || !newReview.trim()} style={styles.submitButton}>
            Submit Review
          </button>
        </form>
      )}

      {reviews.length === 0 ? (
        <p style={styles.empty}>No reviews yet. Be the first to review!</p>
      ) : (
        <div style={styles.list}>
          {reviews.map((review) => (
            <div key={review.id} style={styles.review}>
              <div style={styles.reviewHeader}>
                <span style={styles.username}>{review.username}</span>
                <span style={styles.date}>{new Date(review.created_at).toLocaleDateString()}</span>
                {user?.id === review.user_id && (
                  <button onClick={() => handleDelete(review.id)} style={styles.deleteButton}>
                    Delete
                  </button>
                )}
              </div>
              <p style={styles.content}>{review.content}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: { marginTop: '2rem' },
  title: { fontSize: '1.25rem', marginBottom: '1rem' },
  form: { marginBottom: '1.5rem' },
  textarea: { width: '100%', padding: '0.75rem', border: '1px solid #ddd', borderRadius: '4px', fontSize: '1rem', resize: 'vertical' as const },
  submitButton: { marginTop: '0.5rem', padding: '0.5rem 1rem', background: '#1976d2', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  empty: { color: '#666', textAlign: 'center', padding: '2rem' },
  list: { display: 'flex', flexDirection: 'column', gap: '1rem' },
  review: { padding: '1rem', border: '1px solid #eee', borderRadius: '8px', background: '#fafafa' },
  reviewHeader: { display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.5rem' },
  username: { fontWeight: 'bold' },
  date: { color: '#999', fontSize: '0.875rem' },
  deleteButton: { marginLeft: 'auto', padding: '0.25rem 0.5rem', background: '#f44336', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '0.75rem' },
  content: { margin: 0, lineHeight: 1.6 },
};
