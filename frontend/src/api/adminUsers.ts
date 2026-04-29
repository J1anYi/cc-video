import { fetchApi } from './auth';

export interface UserAdminView {
  id: number;
  email: string;
  display_name: string | null;
  role: string;
  is_active: boolean;
  is_suspended: boolean;
  deleted_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface UserListResponse {
  users: UserAdminView[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}

export async function getUsers(page: number = 1, limit: number = 20, search?: string): Promise<UserListResponse> {
  const params = new URLSearchParams({
    page: page.toString(),
    limit: limit.toString(),
  });
  if (search) {
    params.append('search', search);
  }
  return fetchApi<UserListResponse>(`/admin/users?${params.toString()}`);
}

export async function getUserDetails(userId: number): Promise<UserAdminView> {
  return fetchApi<UserAdminView>(`/admin/users/${userId}`);
}

export async function suspendUser(userId: number, suspend: boolean): Promise<UserAdminView> {
  return fetchApi<UserAdminView>(`/admin/users/${userId}/suspend`, {
    method: 'PATCH',
    body: JSON.stringify({ suspend }),
  });
}

export async function deleteUser(userId: number): Promise<void> {
  return fetchApi<void>(`/admin/users/${userId}`, {
    method: 'DELETE',
  });
}
