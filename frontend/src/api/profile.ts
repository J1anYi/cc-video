import { fetchApi } from './auth';

export interface PublicProfileResponse {
  id: number;
  display_name: string | null;
  followers_count: number;
  following_count: number;
  review_count: number;
  rating_count: number;
}

export async function getPublicProfile(userId: number): Promise<PublicProfileResponse> {
  return fetchApi<PublicProfileResponse>(`/users/${userId}/profile`);
}
