import type { Movie, MovieListResponse } from './types';
import { fetchApi } from './auth';

// User Movies API
export async function getMovies(): Promise<MovieListResponse> {
  return fetchApi<MovieListResponse>('/movies');
}

export async function getMovie(id: number): Promise<Movie> {
  return fetchApi<Movie>(`/movies/${id}`);
}

export function getStreamUrl(movieId: number): string {
  const token = localStorage.getItem('token');
  return `/api/v1/movies/${movieId}/stream?token=${token}`;
}
