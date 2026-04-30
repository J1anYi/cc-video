import api from './axios';

export const createReport = async (data: {
  name: string;
  report_type: string;
  data_source: string;
  description?: string;
  filters?: Record<string, any>;
  columns?: string[];
  is_public?: boolean;
}) => {
  const res = await api.post('/admin/reports', data);
  return res.data;
};

export const getReports = async () => {
  const res = await api.get('/admin/reports');
  return res.data;
};

export const getReport = async (id: number) => {
  const res = await api.get(`/admin/reports/${id}`);
  return res.data;
};

export const executeReport = async (id: number) => {
  const res = await api.post(`/admin/reports/${id}/execute`);
  return res.data;
};

export const exportReport = async (id: number, format: string = 'pdf') => {
  const res = await api.get(`/admin/reports/${id}/export?format=${format}`);
  return res.data;
};

export const scheduleReport = async (id: number, data: { frequency: string; recipients: string[]; format?: string }) => {
  const res = await api.post(`/admin/reports/${id}/schedule`, data);
  return res.data;
};

export const shareReport = async (id: number, data: { shared_with_user_id?: number; permission: string }) => {
  const res = await api.post(`/admin/reports/${id}/share`, data);
  return res.data;
};

export const getDashboardConfig = async () => {
  const res = await api.get('/admin/reports/dashboard/config');
  return res.data;
};

export const updateDashboardConfig = async (data: {
  layout?: Record<string, any>;
  widgets?: string[];
  filters?: Record<string, any>;
  refresh_interval?: number;
  theme?: string;
}) => {
  const res = await api.put('/admin/reports/dashboard/config', data);
  return res.data;
};
