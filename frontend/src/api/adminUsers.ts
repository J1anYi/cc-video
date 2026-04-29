import api from './client';

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

export const adminUsersApi = {
  getUsers: async (page: number = 1, limit: number = 20, search?: string): Promise<UserListResponse> => {
    const params = new URLSearchParams({
      page: page.toString(),
      limit: limit.toString(),
    });
    if (search) {
      params.append('search', search);
    }
    const response = await api.get(`/admin/users?${params.toString()}`);
    return response.data;
  },

  getUserDetails: async (userId: number): Promise<UserAdminView> => {
    const response = await api.get(`/admin/users/${userId}`);
    return response.data;
  },

  suspendUser: async (userId: number, suspend: boolean): Promise<UserAdminView> => {
    const response = await api.patch(`/admin/users/${userId}/suspend`, { suspend });
    return response.data;
  },

  deleteUser: async (userId: number): Promise<void> => {
    await api.delete(`/admin/users/${userId}`);
  },
};
