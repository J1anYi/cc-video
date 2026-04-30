import api from './index';
import { CDNProvider, CacheBehavior, InvalidationStatus } from './types';

export interface CDNConfigCreate {
  provider: CDNProvider;
  distribution_id?: string;
  domain_name?: string;
  origin_url: string;
  default_ttl?: number;
  max_ttl?: number;
  https_enabled?: boolean;
  compression_enabled?: boolean;
}

export interface CDNConfigResponse {
  id: number;
  tenant_id: number;
  provider: CDNProvider;
  distribution_id?: string;
  domain_name?: string;
  origin_url: string;
  default_ttl: number;
  https_enabled: boolean;
  is_active: boolean;
  created_at: string;
}

export interface CacheRuleCreate {
  path_pattern: string;
  content_type?: string;
  behavior?: CacheBehavior;
  ttl?: number;
  query_string_whitelist?: string;
  priority?: number;
}

export interface CacheRuleResponse {
  id: number;
  path_pattern: string;
  behavior: CacheBehavior;
  ttl: number;
  priority: number;
  is_active: boolean;
  created_at: string;
}

export interface InvalidationRequest {
  paths: string[];
}

export interface InvalidationResponse {
  invalidation_id: string;
  status: InvalidationStatus;
  paths: string;
  created_at: string;
}

export interface CDNMetricsResponse {
  timestamp: string;
  requests: number;
  hits: number;
  misses: number;
  bandwidth_bytes: number;
  bytes_saved: number;
  avg_latency_ms: number;
  hit_rate: number;
}

export interface CDNMetricsSummary {
  total_requests: number;
  total_hits: number;
  total_misses: number;
  total_bandwidth: number;
  total_bytes_saved: number;
  avg_latency_ms: number;
  avg_error_rate: number;
  hit_rate: number;
}

export const cdnApi = {
  configure: async (data: CDNConfigCreate): Promise<CDNConfigResponse> => {
    const response = await api.post('/cdn/configure', data);
    return response.data;
  },

  getConfig: async (): Promise<CDNConfigResponse | null> => {
    const response = await api.get('/cdn/config');
    return response.data;
  },

  createCacheRule: async (data: CacheRuleCreate): Promise<CacheRuleResponse> => {
    const response = await api.post('/cdn/cache-rules', data);
    return response.data;
  },

  getCacheRules: async (): Promise<CacheRuleResponse[]> => {
    const response = await api.get('/cdn/cache-rules');
    return response.data;
  },

  deleteCacheRule: async (ruleId: number): Promise<{ success: boolean }> => {
    const response = await api.delete(`/cdn/cache-rules/${ruleId}`);
    return response.data;
  },

  invalidateCache: async (data: InvalidationRequest): Promise<InvalidationResponse> => {
    const response = await api.post('/cdn/invalidate', data);
    return response.data;
  },

  getInvalidationStatus: async (invalidationId: string): Promise<InvalidationResponse> => {
    const response = await api.get(`/cdn/invalidate/${invalidationId}`);
    return response.data;
  },

  getMetrics: async (
    startTime?: string,
    endTime?: string
  ): Promise<CDNMetricsResponse[]> => {
    const params: Record<string, string> = {};
    if (startTime) params.start_time = startTime;
    if (endTime) params.end_time = endTime;
    const response = await api.get('/cdn/metrics', { params });
    return response.data;
  },

  getMetricsSummary: async (
    startTime?: string,
    endTime?: string
  ): Promise<CDNMetricsSummary> => {
    const params: Record<string, string> = {};
    if (startTime) params.start_time = startTime;
    if (endTime) params.end_time = endTime;
    const response = await api.get('/cdn/metrics/summary', { params });
    return response.data;
  },
};

export default cdnApi;
