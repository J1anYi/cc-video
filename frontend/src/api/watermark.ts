import api from './index';

export enum WatermarkType {
  VISIBLE = 'visible',
  FORENSIC = 'forensic',
  USER_SPECIFIC = 'user_specific',
}

export enum WatermarkPosition {
  TOP_LEFT = 'top_left',
  TOP_RIGHT = 'top_right',
  BOTTOM_LEFT = 'bottom_left',
  BOTTOM_RIGHT = 'bottom_right',
  CENTER = 'center',
  CUSTOM = 'custom',
}

export interface WatermarkConfig {
  id: number;
  tenant_id: number;
  default_type: WatermarkType;
  default_position: WatermarkPosition;
  default_opacity: number;
  default_scale: number;
  forensic_enabled: boolean;
  user_watermark_enabled: boolean;
  is_active: boolean;
  created_at: string;
}

export interface Watermark {
  id: number;
  name: string;
  type: WatermarkType;
  image_path?: string;
  text_content?: string;
  position: WatermarkPosition;
  opacity: number;
  scale: number;
  status: string;
  created_at: string;
}

export interface ForensicResponse {
  pattern_id: string;
  embedded_data: string;
  content_id: number;
  created_at: string;
}

export interface TraceResponse {
  found: boolean;
  source_user_id?: number;
  source_session_id?: string;
  confidence_score: number;
  trace_id: number;
}

export const watermarkApi = {
  configure: async (data: {
    default_type?: WatermarkType;
    default_position?: WatermarkPosition;
    default_opacity?: number;
    default_scale?: number;
    custom_x?: number;
    custom_y?: number;
    forensic_enabled?: boolean;
    forensic_strength?: number;
    user_watermark_enabled?: boolean;
  }): Promise<WatermarkConfig> => {
    const response = await api.post('/watermarks/config', data);
    return response.data;
  },

  getConfig: async (): Promise<WatermarkConfig> => {
    const response = await api.get('/watermarks/config');
    return response.data;
  },

  create: async (data: {
    name: string;
    type: WatermarkType;
    image_path?: string;
    text_content?: string;
    position?: WatermarkPosition;
    opacity?: number;
    scale?: number;
  }): Promise<Watermark> => {
    const response = await api.post('/watermarks', data);
    return response.data;
  },

  list: async (): Promise<Watermark[]> => {
    const response = await api.get('/watermarks');
    return response.data;
  },

  apply: async (data: {
    content_id: number;
    content_type?: string;
    watermark_id?: number;
    session_id: string;
    user_specific_text?: string;
  }): Promise<{ session_id: number; watermark_data: string }> => {
    const response = await api.post('/watermarks/apply', data);
    return response.data;
  },

  generateForensic: async (data: {
    content_id: number;
    content_type?: string;
    session_id: string;
    strength?: number;
  }): Promise<ForensicResponse> => {
    const response = await api.post('/watermarks/forensic', data);
    return response.data;
  },

  trace: async (data: {
    sample_data: string;
    content_id?: number;
  }): Promise<TraceResponse> => {
    const response = await api.post('/watermarks/trace', data);
    return response.data;
  },
};
