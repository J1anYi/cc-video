import { fetchApi } from './auth';

export interface PasswordResetResponse {
  message: string;
}

export async function requestPasswordReset(email: string): Promise<PasswordResetResponse> {
  return fetchApi<PasswordResetResponse>('/auth/password-reset', {
    method: 'POST',
    body: JSON.stringify({ email }),
  });
}

export async function confirmPasswordReset(token: string, newPassword: string): Promise<PasswordResetResponse> {
  return fetchApi<PasswordResetResponse>('/auth/password-reset/confirm', {
    method: 'POST',
    body: JSON.stringify({
      token,
      new_password: newPassword,
    }),
  });
}
