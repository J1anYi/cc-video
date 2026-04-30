import { fetchApi } from './auth';

export interface ReviewResponse {
  id: number;
  user_id: number;
  movie_id: number;
  username: string;
  content: string;
  created_at: string;
  updated_at: string;
}

export interface ReviewListResponse {
  reviews: ReviewResponse[];
  total: number;
}

export async function createReview(movieId: number, content: string): Promise<ReviewResponse> {
  return fetchApi<ReviewResponse>(`/movies/${movieId}/reviews`, {
    method: 'POST',
    body: JSON.stringify({ content }),
  });
}

export async function getMovieReviews(movieId: number, skip = 0, limit = 20): Promise<ReviewListResponse> {
  return fetchApi<ReviewListResponse>(`/movies/${movieId}/reviews?skip=${skip}&limit=${limit}`);
}

export async function updateReview(reviewId: number, content: string): Promise<ReviewResponse> {
  return fetchApi<ReviewResponse>(`/reviews/${reviewId}`, {
    method: 'PUT',
    body: JSON.stringify({ content }),
  });
}

export async function deleteReview(reviewId: number): Promise<void> {
  await fetchApi(`/reviews/${reviewId}`, { method: 'DELETE' });
}
