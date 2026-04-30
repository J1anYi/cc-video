import { fetchApi } from './auth';
import type { Movie } from './types';

export interface TrendingMovie {
  movie: Movie;
  view_count: number;
}

export interface TrendingResponse {
  movies: TrendingMovie[];
}

export interface RelatedMoviesResponse {
  movies: Movie[];
}

export async function getTrending(): Promise<TrendingResponse> {
  return fetchApi<TrendingResponse>('/trending');
}

export async function getRelatedMovies(movieId: number): Promise<RelatedMoviesResponse> {
  return fetchApi<RelatedMoviesResponse>('/movies/' + movieId + '/related');
}
