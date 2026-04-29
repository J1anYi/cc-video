import type { WatchHistory } from './types';
import { fetchApi } from './auth';

export async function getWatchHistory(): Promise<WatchHistory[]> {
  return fetchApi<WatchHistory[]>('/history');
}

export async function updateWatchHistory(movieId: number, progress: number): Promise<WatchHistory> {
  return fetchApi<WatchHistory>('/history', {
    method: 'POST',
    body: JSON.stringify({ movie_id: movieId, progress }),
  });
}

export async function getHistoryEntry(movieId: number): Promise<WatchHistory> {
  return fetchApi<WatchHistory>(`/history/${movieId}`);
}
