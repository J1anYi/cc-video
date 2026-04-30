import api from './index';

export enum EncryptionAlgorithm {
  AES_256_GCM = 'aes_256_gcm',
  AES_256_CBC = 'aes_256_cbc',
}

export enum KeyStatus {
  ACTIVE = 'active',
  EXPIRED = 'expired',
  COMPROMISED = 'compromised',
}

export interface EncryptionConfig {
  id: number;
  tenant_id: number;
  algorithm: EncryptionAlgorithm;
  key_rotation_days: number;
  encryption_at_rest: boolean;
  end_to_end_encryption: boolean;
  secure_key_delivery: boolean;
  is_active: boolean;
  created_at: string;
}

export interface EncryptionKey {
  id: number;
  key_id: string;
  content_id: number;
  content_type: string;
  algorithm: EncryptionAlgorithm;
  status: KeyStatus;
  version: number;
  created_at: string;
}

export interface KeyDelivery {
  delivery_token: string;
  key_id: string;
  algorithm: EncryptionAlgorithm;
  expires_at: string;
}

export interface EncryptionStatus {
  content_id: number;
  content_type: string;
  is_encrypted: boolean;
  algorithm?: EncryptionAlgorithm;
  key_status?: KeyStatus;
  last_rotated?: string;
}

export const encryptionApi = {
  configure: async (data: { algorithm?: EncryptionAlgorithm; key_rotation_days?: number; encryption_at_rest?: boolean; end_to_end_encryption?: boolean; secure_key_delivery?: boolean; key_delivery_ttl_seconds?: number }): Promise<EncryptionConfig> => {
    const response = await api.post('/encryption/config', data);
    return response.data;
  },

  getConfig: async (): Promise<EncryptionConfig> => {
    const response = await api.get('/encryption/config');
    return response.data;
  },

  generateKey: async (data: { content_id: number; content_type?: string; algorithm?: EncryptionAlgorithm }): Promise<EncryptionKey> => {
    const response = await api.post('/encryption/keys', data);
    return response.data;
  },

  deliverKey: async (data: { content_id: number; content_type?: string; session_id: string; device_id: string }): Promise<KeyDelivery> => {
    const response = await api.post('/encryption/deliver', data);
    return response.data;
  },

  getStatus: async (contentId: number, contentType?: string): Promise<EncryptionStatus> => {
    const response = await api.get(`/encryption/status/${contentId}`, { params: { content_type: contentType } });
    return response.data;
  },
};
