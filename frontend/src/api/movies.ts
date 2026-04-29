import type { Movie, MovieListResponse } from './types';
import { fetchApi } from './auth';

export interface MovieSearchParams {
  q?: string;
  category?: string;
  min_rating?: number;
  year_from?: number;
  year_to?: number;
  duration_from?: number;
  duration_to?: number;
  sort_by?: 'rating' | 'year' | 'title' | 'created_at';
  sort_order?: 'asc' | 'desc';
}

// User Movies API
export async function getMovies(params?: MovieSearchParams): Promise<MovieListResponse> {
  const searchParams = new URLSearchParams();
  if (params?.q) searchParams.append('q', params.q);
  if (params?.category) searchParams.append('category', params.category);
  if (params?.min_rating !== undefined) searchParams.append('min_rating', params.min_rating.toString());
  if (params?.year_from !== undefined) searchParams.append('year_from', params.year_from.toString());
  if (params?.year_to !== undefined) searchParams.append('year_to', params.year_to.toString());
  if (params?.duration_from !== undefined) searchParams.append('duration_from', params.duration_from.toString());
  if (params?.duration_to !== undefined) searchParams.append('duration_to', params.duration_to.toString());
  if (params?.sort_by) searchParams.append('sort_by', params.sort_by);
  if (params?.sort_order) searchParams.append('sort_order', params.sort_order);

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
