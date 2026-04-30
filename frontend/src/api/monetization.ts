import api from './client';

export interface CreatorEarnings {
  total_gross: number;
  total_fees: number;
  total_net: number;
  available_balance: number;
  earnings_count: number;
}

export interface Payout {
  id: number;
  amount: number;
  status: string;
}

export interface Tip {
  id: number;
  amount: number;
  message?: string;
  created_at: string;
}

export interface CreatorTier {
  id: number;
  name: string;
  price: number;
  billing_period: string;
  subscriber_count: number;
}

export const monetizationApi = {
  getEarnings: async (creatorId: number, startDate?: string, endDate?: string): Promise<CreatorEarnings> => {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    const response = await api.get(`/creators/${creatorId}/earnings?${params.toString()}`);
    return response.data;
  },

  requestPayout: async (creatorId: number, data: { amount: number; payment_method: string; payment_details?: any }): Promise<Payout> => {
    const response = await api.post(`/creators/${creatorId}/payouts`, data);
    return response.data;
  },

  sendTip: async (creatorId: number, data: { amount: number; message?: string; currency?: string }): Promise<Tip> => {
    const response = await api.post(`/creators/${creatorId}/tips`, data);
    return response.data;
  },

  getTips: async (creatorId: number, skip?: number, limit?: number): Promise<{ tips: Tip[] }> => {
    const params = new URLSearchParams();
    if (skip) params.append('skip', skip.toString());
    if (limit) params.append('limit', limit.toString());
    const response = await api.get(`/creators/${creatorId}/tips?${params.toString()}`);
    return response.data;
  },

  createTier: async (creatorId: number, data: { name: string; price: number; description?: string; benefits?: any; billing_period?: string }): Promise<CreatorTier> => {
    const response = await api.post(`/creators/${creatorId}/tiers`, data);
    return response.data;
  },

  getTiers: async (creatorId: number): Promise<{ tiers: CreatorTier[] }> => {
    const response = await api.get(`/creators/${creatorId}/tiers`);
    return response.data;
  },

  subscribe: async (creatorId: number, tierId: number): Promise<{ id: number; tier_id: number; status: string }> => {
    const response = await api.post(`/creators/${creatorId}/subscribe?tier_id=${tierId}`);
    return response.data;
  },

  createPremiumContent: async (data: { movie_id: number; title: string; price: number; description?: string; access_type?: string }): Promise<{ id: number; title: string; price: number }> => {
    const response = await api.post('/creators/premium-content', data);
    return response.data;
  },

  checkPremiumAccess: async (contentId: number): Promise<{ has_access: boolean }> => {
    const response = await api.get(`/creators/premium-content/${contentId}/access`);
    return response.data;
  },
};

export default monetizationApi;
