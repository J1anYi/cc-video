import type { Favorite, FavoriteStatus } from './types';
import { fetchApi } from './auth';

export async function getFavorites(): Promise<Favorite[]> {
  return fetchApi<Favorite[]>('/favorites');
}

export async function addFavorite(movieId: number): Promise<Favorite> {
  return fetchApi<Favorite>(`/favorites?movie_id=${movieId}`, {
    method: 'POST',
  });
}

export async function removeFavorite(movieId: number): Promise<void> {
  await fetchApi(`/favorites/${movieId}`, {
    method: 'DELETE',
  });
}

export async function getFavoriteStatus(movieId: number): Promise<FavoriteStatus> {
  return fetchApi<FavoriteStatus>(`/favorites/${movieId}/status`);
}
