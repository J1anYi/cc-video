import { fetchApi } from './auth';

export interface ActivityResponse {
  id: number;
  user_id: number;
  username: string | null;
  activity_type: string;
  movie_id: number | null;
  movie_title: string | null;
  reference_id: number | null;
  created_at: string;
}

export interface ActivityListResponse {
  activities: ActivityResponse[];
  total: number;
}

export async function getActivityFeed(skip = 0, limit = 20): Promise<ActivityListResponse> {
  return fetchApi<ActivityListResponse>(`/feed?skip=${skip}&limit=${limit}`);
}
