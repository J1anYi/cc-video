import { fetchApi } from './auth';

export interface MovieRatingStats {
  average_rating: number | null;
  rating_count: number;
  user_rating: number | null;
}

export interface RatingResponse {
  id: number;
  user_id: number;
  movie_id: number;
  rating: number;
  created_at: string;
  updated_at: string;
}

export async function setRating(movieId: number, rating: number): Promise<RatingResponse> {
  return fetchApi<RatingResponse>(`/movies/${movieId}/rating`, {
    method: 'POST',
    body: JSON.stringify({ rating }),
  });
}

export async function getMovieRating(movieId: number): Promise<MovieRatingStats> {
  return fetchApi<MovieRatingStats>(`/movies/${movieId}/rating`);
}

export async function deleteRating(movieId: number): Promise<void> {
  await fetchApi(`/movies/${movieId}/rating`, { method: 'DELETE' });
}
