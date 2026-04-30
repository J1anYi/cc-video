import api from './axios';

export const enable2FA = async () => {
  const res = await api.post('/security/2fa/enable');
  return res.data;
};

export const verify2FA = async (code: string) => {
  const res = await api.post('/security/2fa/verify', { code });
  return res.data;
};

export const disable2FA = async () => {
  const res = await api.post('/security/2fa/disable');
  return res.data;
};

export const get2FAStatus = async () => {
  const res = await api.get('/security/2fa');
  return res.data;
};

export const getAuditLogs = async (limit: number = 100, action?: string) => {
  const params = new URLSearchParams({ limit: limit.toString() });
  if (action) params.append('action', action);
  const res = await api.get(`/security/audit-logs?${params}`);
  return res.data;
};

export const exportUserData = async () => {
  const res = await api.post('/security/gdpr/export');
  return res.data;
};

export const requestDataDeletion = async () => {
  const res = await api.post('/security/gdpr/deletion-request');
  return res.data;
};
