import api from './client';

export interface MarketplaceListing {
  id: number;
  movie_id: number;
  seller_id: number;
  title: string;
  description?: string;
  tags?: string;
  pricing_type: string;
  base_price: number;
  currency: string;
  status: string;
  view_count: number;
  purchase_count: number;
  created_at: string;
  pricing_tiers?: PricingTier[];
  previews?: ContentPreview[];
  stats?: ListingStats;
}

export interface PricingTier {
  id: number;
  name: string;
  price: number;
  duration_days?: number;
  features?: Record<string, any>;
}

export interface ContentPreview {
  id: number;
  preview_type: string;
  video_url: string;
  thumbnail_url?: string;
  duration_seconds: number;
}

export interface ListingStats {
  view_count: number;
  purchase_count: number;
  review_count: number;
  avg_rating: number;
}

export interface License {
  id: number;
  listing_id: number;
  license_type: string;
  price_paid: number;
  currency: string;
  valid_from: string;
  valid_until?: string;
  status: string;
}

export interface MarketplaceReview {
  id: number;
  listing_id: number;
  user_id: number;
  rating: number;
  title?: string;
  content?: string;
  helpful_count: number;
  created_at: string;
}

export interface ListingFilters {
  skip?: number;
  limit?: number;
  search?: string;
  pricing_type?: string;
  min_price?: number;
  max_price?: number;
  seller_id?: number;
}

export const marketplaceApi = {
  getListings: async (filters?: ListingFilters): Promise<{ listings: MarketplaceListing[] }> => {
    const params = new URLSearchParams();
    if (filters?.skip) params.append('skip', filters.skip.toString());
    if (filters?.limit) params.append('limit', filters.limit.toString());
    if (filters?.search) params.append('search', filters.search);
    if (filters?.pricing_type) params.append('pricing_type', filters.pricing_type);
    if (filters?.min_price !== undefined) params.append('min_price', filters.min_price.toString());
    if (filters?.max_price !== undefined) params.append('max_price', filters.max_price.toString());
    if (filters?.seller_id) params.append('seller_id', filters.seller_id.toString());
    
    const response = await api.get(`/marketplace?${params.toString()}`);
    return response.data;
  },

  getListing: async (id: number): Promise<MarketplaceListing> => {
    const response = await api.get(`/marketplace/${id}`);
    return response.data;
  },

  createListing: async (data: {
    movie_id: number;
    title: string;
    description?: string;
    tags?: string;
    pricing_type?: string;
    base_price?: number;
    currency?: string;
  }): Promise<{ id: number; movie_id: number; title: string; status: string }> => {
    const response = await api.post('/marketplace', data);
    return response.data;
  },

  updateListing: async (id: number, data: Partial<{
    title: string;
    description: string;
    tags: string;
    pricing_type: string;
    base_price: number;
    status: string;
  }>): Promise<{ message: string; id: number }> => {
    const response = await api.put(`/marketplace/${id}`, data);
    return response.data;
  },

  deleteListing: async (id: number): Promise<{ message: string }> => {
    const response = await api.delete(`/marketplace/${id}`);
    return response.data;
  },

  addPricingTier: async (listingId: number, data: {
    name: string;
    price: number;
    duration_days?: number;
    features?: Record<string, any>;
  }): Promise<{ id: number; name: string; price: number }> => {
    const response = await api.post(`/marketplace/${listingId}/tiers`, data);
    return response.data;
  },

  addPreview: async (listingId: number, data: {
    preview_type: string;
    video_url: string;
    thumbnail_url?: string;
    duration_seconds?: number;
  }): Promise<{ id: number; preview_type: string }> => {
    const response = await api.post(`/marketplace/${listingId}/previews`, data);
    return response.data;
  },

  purchaseLicense: async (listingId: number, data?: {
    tier_id?: number;
    transaction_id?: string;
  }): Promise<{
    license_id: number;
    license_type: string;
    price_paid: number;
    valid_until?: string;
  }> => {
    const response = await api.post(`/marketplace/${listingId}/purchase`, data || {});
    return response.data;
  },

  getMyLicenses: async (): Promise<{ licenses: License[] }> => {
    const response = await api.get('/marketplace/licenses/me');
    return response.data;
  },

  addReview: async (listingId: number, data: {
    rating: number;
    title?: string;
    content?: string;
  }): Promise<{ id: number; rating: number }> => {
    const response = await api.post(`/marketplace/${listingId}/reviews`, data);
    return response.data;
  },

  getReviews: async (listingId: number, skip?: number, limit?: number): Promise<{ reviews: MarketplaceReview[] }> => {
    const params = new URLSearchParams();
    if (skip) params.append('skip', skip.toString());
    if (limit) params.append('limit', limit.toString());
    
    const response = await api.get(`/marketplace/${listingId}/reviews?${params.toString()}`);
    return response.data;
  },
};

export default marketplaceApi;
