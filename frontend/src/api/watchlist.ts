import { fetchApi } from './auth';

export interface WatchlistCreate {
  name: string;
  description?: string;
  is_public?: boolean;
}

export interface WatchlistUpdate {
  name?: string;
  description?: string;
  is_public?: boolean;
}

export interface MovieInWatchlist {
  id: number;
  title: string;
  poster_url: string | null;
  position: number;
  added_at: string;
}

export interface WatchlistResponse {
  id: number;
  user_id: number;
  name: string;
  description: string | null;
  is_public: boolean;
  movie_count: number;
  created_at: string;
  updated_at: string;
}

export interface WatchlistDetailResponse {
  id: number;
  user_id: number;
  name: string;
  description: string | null;
  is_public: boolean;
  created_at: string;
  updated_at: string;
  movies: MovieInWatchlist[];
}

export interface WatchlistListResponse {
  watchlists: WatchlistResponse[];
  total: number;
}

export interface PublicWatchlistResponse {
  id: number;
  name: string;
  description: string | null;
  user_id: number;
  user_name: string | null;
  movie_count: number;
  created_at: string;
}

export interface PublicWatchlistDetailResponse {
  id: number;
  name: string;
  description: string | null;
  user_id: number;
  user_name: string | null;
  is_public: boolean;
  created_at: string;
  movies: MovieInWatchlist[];
}

export async function createWatchlist(data: WatchlistCreate): Promise<WatchlistResponse> {
  return fetchApi<WatchlistResponse>('/watchlists', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function getWatchlists(): Promise<WatchlistListResponse> {
  return fetchApi<WatchlistListResponse>('/watchlists');
}

export async function getWatchlist(id: number): Promise<WatchlistDetailResponse> {
  return fetchApi<WatchlistDetailResponse>(`/watchlists/${id}`);
}

export async function updateWatchlist(id: number, data: WatchlistUpdate): Promise<WatchlistResponse> {
  return fetchApi<WatchlistResponse>(`/watchlists/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  });
}

export async function deleteWatchlist(id: number): Promise<void> {
  await fetchApi(`/watchlists/${id}`, { method: 'DELETE' });
}

export async function addMovieToWatchlist(watchlistId: number, movieId: number): Promise<void> {
  await fetchApi(`/watchlists/${watchlistId}/movies`, {
    method: 'POST',
    body: JSON.stringify({ movie_id: movieId }),
  });
}

export async function addMoviesToWatchlist(watchlistId: number, movieIds: number[]): Promise<void> {
  await fetchApi(`/watchlists/${watchlistId}/movies/batch`, {
    method: 'POST',
    body: JSON.stringify({ movie_ids: movieIds }),
  });
}

export async function removeMovieFromWatchlist(watchlistId: number, movieId: number): Promise<void> {
  await fetchApi(`/watchlists/${watchlistId}/movies/${movieId}`, { method: 'DELETE' });
}

export async function getPublicWatchlists(skip = 0, limit = 20): Promise<PublicWatchlistResponse[]> {
  return fetchApi<PublicWatchlistResponse[]>(`/watchlists/public?skip=${skip}&limit=${limit}`);
}

export async function getPublicWatchlist(id: number): Promise<PublicWatchlistDetailResponse> {
  return fetchApi<PublicWatchlistDetailResponse>(`/watchlists/${id}/public`);
}
