import { fetchApi } from './auth';

export interface BlockedUser {
  id: number;
  display_name: string;
  blocked_at: string;
}

export interface BlockStatus {
  is_blocked: boolean;
}

export async function blockUser(userId: number): Promise<BlockStatus> {
  return fetchApi<BlockStatus>(`/users/${userId}/block`, { method: 'POST' });
}

export async function unblockUser(userId: number): Promise<BlockStatus> {
  return fetchApi<BlockStatus>(`/users/${userId}/block`, { method: 'DELETE' });
}

export async function getBlockStatus(userId: number): Promise<BlockStatus> {
  return fetchApi<BlockStatus>(`/users/${userId}/block/status`);
}

export async function getBlockedUsers(): Promise<BlockedUser[]> {
  return fetchApi<BlockedUser[]>('/users/blocked');
}
