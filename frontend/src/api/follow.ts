import { fetchApi } from './auth';

export interface FollowResponse {
  id: number;
  follower_id: number;
  following_id: number;
  created_at: string;
}

export interface UserBrief {
  id: number;
  email: string;
  display_name: string | null;
}

export interface FollowerResponse {
  id: number;
  follower: UserBrief;
  created_at: string;
}

export interface FollowingResponse {
  id: number;
  following: UserBrief;
  created_at: string;
}

export interface FollowStatusResponse {
  is_following: boolean;
}

export interface FollowCountsResponse {
  followers_count: number;
  following_count: number;
}

export async function followUser(userId: number): Promise<FollowResponse> {
  return fetchApi<FollowResponse>(`/users/${userId}/follow`, {
    method: 'POST',
  });
}

export async function unfollowUser(userId: number): Promise<void> {
  await fetchApi(`/users/${userId}/follow`, { method: 'DELETE' });
}

export async function getFollowers(userId: number, skip = 0, limit = 50): Promise<FollowerResponse[]> {
  return fetchApi<FollowerResponse[]>(`/users/${userId}/followers?skip=${skip}&limit=${limit}`);
}

export async function getFollowing(userId: number, skip = 0, limit = 50): Promise<FollowingResponse[]> {
  return fetchApi<FollowingResponse[]>(`/users/${userId}/following?skip=${skip}&limit=${limit}`);
}

export async function getFollowStatus(userId: number): Promise<FollowStatusResponse> {
  return fetchApi<FollowStatusResponse>(`/users/${userId}/follow/status`);
}

export async function getFollowCounts(userId: number): Promise<FollowCountsResponse> {
  return fetchApi<FollowCountsResponse>(`/users/${userId}/follow/counts`);
}
