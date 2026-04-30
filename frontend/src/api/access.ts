import api from './index';

export enum AccessLevel {
  FULL = 'full',
  LIMITED = 'limited',
  PREVIEW = 'preview',
  NONE = 'none',
}

export enum PermissionType {
  VIEW = 'view',
  DOWNLOAD = 'download',
  SHARE = 'share',
}

export interface AccessPolicy {
  id: number;
  tenant_id: number;
  name: string;
  description?: string;
  default_level: AccessLevel;
  max_devices: number;
  max_concurrent_streams: number;
  is_active: boolean;
  created_at: string;
}

export interface ContentPermission {
  id: number;
  content_id: number;
  content_type: string;
  user_id?: number;
  permission_type: PermissionType;
  access_level: AccessLevel;
  created_at: string;
  expires_at?: string;
}

export interface AccessCheckResponse {
  allowed: boolean;
  access_level: AccessLevel;
  reason?: string;
  session_token?: string;
}

export interface StreamSession {
  id: number;
  content_id: number;
  content_type: string;
  device_id: string;
  started_at: string;
  is_active: boolean;
}

export const accessApi = {
  createPolicy: async (data: { name: string; description?: string; default_level?: AccessLevel; max_devices?: number; max_concurrent_streams?: number }): Promise<AccessPolicy> => {
    const response = await api.post('/access/policies', data);
    return response.data;
  },

  listPolicies: async (): Promise<AccessPolicy[]> => {
    const response = await api.get('/access/policies');
    return response.data;
  },

  setPermission: async (data: { content_id: number; content_type?: string; user_id?: number; role_id?: number; permission_type?: PermissionType; access_level?: AccessLevel; expires_at?: string }): Promise<ContentPermission> => {
    const response = await api.post('/access/permissions', data);
    return response.data;
  },

  checkAccess: async (data: { content_id: number; content_type?: string; device_id: string; permission_type?: PermissionType }): Promise<AccessCheckResponse> => {
    const response = await api.post('/access/check', data);
    return response.data;
  },

  listSessions: async (): Promise<StreamSession[]> => {
    const response = await api.get('/access/sessions');
    return response.data;
  },

  terminateSession: async (sessionId: number): Promise<void> => {
    await api.delete(`/access/sessions/${sessionId}`);
  },
};
