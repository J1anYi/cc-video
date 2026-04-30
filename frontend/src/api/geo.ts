import api from './index';

export enum GeoRuleType {
  ALLOW = 'allow',
  BLOCK = 'block',
}

export enum GeoAction {
  ALLOW = 'allow',
  BLOCK = 'block',
  REDIRECT = 'redirect',
}

export interface GeoConfig {
  id: number;
  tenant_id: number;
  enabled: boolean;
  default_action: GeoAction;
  vpn_detection_enabled: boolean;
  proxy_detection_enabled: boolean;
  bypass_prevention_enabled: boolean;
  redirect_url?: string;
  created_at: string;
}

export interface GeoRule {
  id: number;
  content_id?: number;
  content_type: string;
  rule_type: GeoRuleType;
  country_code?: string;
  region_code?: string;
  action: GeoAction;
  priority: number;
  is_active: boolean;
  created_at: string;
}

export interface AccessCheckResponse {
  allowed: boolean;
  action: GeoAction;
  country_code?: string;
  region_code?: string;
  is_vpn: boolean;
  is_proxy: boolean;
  block_reason?: string;
}

export interface VPNDetection {
  ip_address: string;
  is_vpn: boolean;
  is_proxy: boolean;
  is_tor: boolean;
  confidence_score: number;
  provider_name?: string;
}

export const geoApi = {
  configure: async (data: {
    enabled?: boolean;
    default_action?: GeoAction;
    vpn_detection_enabled?: boolean;
    vpn_action?: GeoAction;
    proxy_detection_enabled?: boolean;
    proxy_action?: GeoAction;
    bypass_prevention_enabled?: boolean;
    redirect_url?: string;
  }): Promise<GeoConfig> => {
    const response = await api.post('/geo/config', data);
    return response.data;
  },

  getConfig: async (): Promise<GeoConfig> => {
    const response = await api.get('/geo/config');
    return response.data;
  },

  createRule: async (data: {
    rule_type: GeoRuleType;
    action: GeoAction;
    country_code?: string;
    region_code?: string;
    content_id?: number;
    content_type?: string;
    priority?: number;
  }): Promise<GeoRule> => {
    const response = await api.post('/geo/rules', data);
    return response.data;
  },

  listRules: async (): Promise<GeoRule[]> => {
    const response = await api.get('/geo/rules');
    return response.data;
  },

  checkAccess: async (data: {
    ip_address: string;
    content_id?: number;
    content_type?: string;
  }): Promise<AccessCheckResponse> => {
    const response = await api.post('/geo/check', data);
    return response.data;
  },

  detectVPN: async (ipAddress: string): Promise<VPNDetection> => {
    const response = await api.get(`/geo/vpn-detect/${ipAddress}`);
    return response.data;
  },

  addWhitelist: async (data: {
    country_code: string;
    region_code?: string;
    content_id?: number;
    content_type?: string;
    notes?: string;
  }): Promise<{ id: number; country_code: string }> => {
    const response = await api.post('/geo/whitelist', data);
    return response.data;
  },

  addBlacklist: async (data: {
    country_code: string;
    region_code?: string;
    content_id?: number;
    content_type?: string;
    reason?: string;
  }): Promise<{ id: number; country_code: string }> => {
    const response = await api.post('/geo/blacklist', data);
    return response.data;
  },
};
