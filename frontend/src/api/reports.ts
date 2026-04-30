import { fetchApi } from './auth';

export type ContentType = 'review' | 'comment';
export type ReportStatus = 'pending' | 'dismissed' | 'actioned';

export interface Report {
  id: number;
  reporter_id: number;
  content_type: ContentType;
  content_id: number;
  reason: string;
  status: ReportStatus;
  created_at: string;
  reviewed_at: string | null;
}

export interface ReportListResponse {
  reports: Report[];
  total: number;
  page: number;
  limit: number;
}

export interface ReportStats {
  pending: number;
  dismissed: number;
  actioned: number;
  total: number;
}

export async function createReport(contentType: ContentType, contentId: number, reason: string): Promise<Report> {
  return fetchApi<Report>('/reports', {
    method: 'POST',
    body: JSON.stringify({
      content_type: contentType,
      content_id: contentId,
      reason,
    }),
  });
}

export async function getPendingReports(page: number = 1, limit: number = 20): Promise<ReportListResponse> {
  return fetchApi<ReportListResponse>(`/reports/admin?page=${page}&limit=${limit}`);
}

export async function getReportStats(): Promise<ReportStats> {
  return fetchApi<ReportStats>('/reports/admin/stats');
}

export async function dismissReport(reportId: number): Promise<Report> {
  return fetchApi<Report>(`/reports/admin/${reportId}/dismiss`, {
    method: 'PATCH',
  });
}

export async function actionReport(reportId: number, removeContent: boolean, warnUser: boolean): Promise<Report> {
  return fetchApi<Report>(`/reports/admin/${reportId}/action`, {
    method: 'PATCH',
    body: JSON.stringify({
      remove_content: removeContent,
      warn_user: warnUser,
    }),
  });
}
