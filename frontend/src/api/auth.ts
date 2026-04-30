import type { User, LoginRequest, LoginResponse } from './types';

const API_BASE = '/api/v1';

export function getToken(): string | null {
  return localStorage.getItem('token');
}

export function setToken(token: string): void {
  localStorage.setItem('token', token);
}

export function clearToken(): void {
  localStorage.removeItem('token');
  localStorage.removeItem('tenant_id');
}

export function getTenantId(): number | null {
  const stored = localStorage.getItem('tenant_id');
  return stored ? parseInt(stored, 10) : null;
}

export function setTenantId(tenantId: number | null): void {
  if (tenantId) {
    localStorage.setItem('tenant_id', String(tenantId));
  } else {
    localStorage.removeItem('tenant_id');
  }
}

function parseTenantFromToken(token: string): number | null {
  try {
    const payload = token.split('.')[1];
    const decoded = JSON.parse(atob(payload));
    return decoded.tenant_id ?? null;
  } catch {
    return null;
  }
}

export async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();
  const tenantId = getTenantId();

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    (headers as Record<string, string>)['Authorization'] = 'Bearer ' + token;
  }

  if (tenantId) {
    (headers as Record<string, string>)['X-Tenant-ID'] = String(tenantId);
  }

  const response = await fetch(API_BASE + endpoint, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    clearToken();
    window.location.href = '/login';
    throw new Error('Unauthorized');
  }

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || 'Request failed');
  }

  const text = await response.text();
  return text ? JSON.parse(text) : (null as T);
}

export async function login(data: LoginRequest): Promise<LoginResponse> {
  const formData = new FormData();
  formData.append('username', data.username);
  formData.append('password', data.password);

  const response = await fetch(API_BASE + '/auth/login', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Login failed' }));
    throw new Error(error.detail || 'Login failed');
  }

  const result: LoginResponse = await response.json();
  setToken(result.access_token);
  
  const tenantId = parseTenantFromToken(result.access_token);
  if (tenantId) {
    setTenantId(tenantId);
  }
  
  return result;
}

export async function register(email: string, password: string): Promise<LoginResponse> {
  const response = await fetch(API_BASE + '/auth/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Registration failed' }));
    throw new Error(error.detail || 'Registration failed');
  }

  const result: LoginResponse = await response.json();
  setToken(result.access_token);
  
  const tenantId = parseTenantFromToken(result.access_token);
  if (tenantId) {
    setTenantId(tenantId);
  }
  
  return result;
}

export async function logout(): Promise<void> {
  try {
    await fetchApi('/auth/logout', { method: 'POST' });
  } finally {
    clearToken();
  }
}

export async function getCurrentUser(): Promise<User> {
  return fetchApi<User>('/auth/me');
}
