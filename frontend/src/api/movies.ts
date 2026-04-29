import type { Movie, MovieListResponse } from './types';
import { fetchApi } from './auth';

export interface MovieSearchParams {
  q?: string;
  category?: string;
}

// User Movies API
export async function getMovies(params?: MovieSearchParams): Promise<MovieListResponse> {
  const searchParams = new URLSearchParams();
  if (params?.q) searchParams.append('q', params.q);
  if (params?.category) searchParams.append('category', params.category);

  const queryString = searchParams.toString();
  const url = queryString ? `/movies?${queryString}` : '/movies';

  return fetchApi<MovieListResponse>(url);
}

export async function getMovie(id: number): Promise<Movie> {
  return fetchApi<Movie>(`/movies/${id}`);
}

export async function getCategories(): Promise<string[]> {
  return fetchApi<string[]>('/categories');
}

export function getStreamUrl(movieId: number): string {
  const token = localStorage.getItem('token');
  return `/api/v1/movies/${movieId}/stream?token=${token}`;
}
