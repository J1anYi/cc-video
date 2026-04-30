import { fetchApi } from './auth';
import type { SubtitleListResponse } from './types';

export async function getMovieSubtitles(movieId: number): Promise<SubtitleListResponse> {
  return fetchApi(`/movies/${movieId}/subtitles`);
}
