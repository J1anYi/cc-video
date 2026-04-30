import { fetchApi } from './auth';
import type { Movie } from './types';

export interface RecommendedMovie {
  movie: Movie;
  reason: string;
}

export interface ContinueWatchingItem {
  movie: Movie;
  progress: number;
  last_watched_at: string;
}

export interface RecommendationsResponse {
  recommendations: RecommendedMovie[];
  continue_watching: ContinueWatchingItem[];
}

export async function getRecommendations(): Promise<RecommendationsResponse> {
  return fetchApi<RecommendationsResponse>('/recommendations');
}
