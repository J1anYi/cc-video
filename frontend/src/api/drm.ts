import api from './index';

export enum DRMProvider {
  WIDEVINE = 'widevine',
  PLAYREADY = 'playready',
  FAIRPLAY = 'fairplay',
}

export enum DeviceType {
  WEB = 'web',
  IOS = 'ios',
  ANDROID = 'android',
  SMART_TV = 'smart_tv',
  UNKNOWN = 'unknown',
}

export interface DRMConfig {
  id: number;
  tenant_id: number;
  provider: DRMProvider;
  widevine_license_url?: string;
  playready_license_url?: string;
  fairplay_license_url?: string;
  max_devices_per_user: number;
  offline_playback_enabled: boolean;
  offline_duration_hours: number;
  key_rotation_days: number;
  is_active: boolean;
  created_at: string;
}

export interface DRMKey {
  id: number;
  key_id: string;
  content_id: number;
  content_type: string;
  provider: DRMProvider;
  status: string;
  created_at: string;
  expires_at?: string;
}

export interface License {
  license_token: string;
  key_id: string;
  provider: DRMProvider;
  content_id: number;
  issued_at: string;
  expires_at: string;
}

export interface Device {
  id: number;
  device_id: string;
  device_name?: string;
  device_type: DeviceType;
  drm_provider: DRMProvider;
  is_active: boolean;
  last_used_at?: string;
  created_at: string;
}

export interface OfflineToken {
  token: string;
  content_id: number;
  device_id: number;
  expires_at: string;
  encrypted_key: string;
}

export const drmApi = {
  configure: async (data: {
    provider: DRMProvider;
    widevine_license_url?: string;
    widevine_provider_id?: string;
    playready_license_url?: string;
    playready_key_id?: string;
    fairplay_license_url?: string;
    fairplay_cert_url?: string;
    max_devices_per_user?: number;
    offline_playback_enabled?: boolean;
    offline_duration_hours?: number;
    key_rotation_days?: number;
  }): Promise<DRMConfig> => {
    const response = await api.post('/drm/config', data);
    return response.data;
  },

  getConfig: async (): Promise<DRMConfig> => {
    const response = await api.get('/drm/config');
    return response.data;
  },

  generateKey: async (data: {
    content_id: number;
    content_type?: string;
    provider: DRMProvider;
  }): Promise<DRMKey> => {
    const response = await api.post('/drm/keys', data);
    return response.data;
  },

  issueLicense: async (data: {
    content_id: number;
    content_type?: string;
    device_id: string;
    provider: DRMProvider;
  }): Promise<License> => {
    const response = await api.post('/drm/license', data);
    return response.data;
  },

  registerDevice: async (data: {
    device_id: string;
    device_name?: string;
    device_type?: DeviceType;
    drm_provider: DRMProvider;
  }): Promise<Device> => {
    const response = await api.post('/drm/devices', data);
    return response.data;
  },

  listDevices: async (): Promise<Device[]> => {
    const response = await api.get('/drm/devices');
    return response.data;
  },

  removeDevice: async (deviceId: number): Promise<void> => {
    await api.delete(`/drm/devices/${deviceId}`);
  },

  generateOfflineToken: async (data: {
    content_id: number;
    content_type?: string;
    device_id: string;
    provider: DRMProvider;
  }): Promise<OfflineToken> => {
    const response = await api.post('/drm/offline-token', data);
    return response.data;
  },

  rotateKeys: async (data: {
    content_id: number;
    content_type?: string;
  }): Promise<{ old_key_id: string; new_key_id: string; rotated_at: string }> => {
    const response = await api.post('/drm/rotate-keys', data);
    return response.data;
  },
};
