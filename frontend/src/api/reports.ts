import api from './client';

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

export const reportsApi = {
  createReport: async (contentType: ContentType, contentId: number, reason: string): Promise<Report> => {
    const response = await api.post('/reports', {
      content_type: contentType,
      content_id: contentId,
      reason,
    });
    return response.data;
  },

  getPendingReports: async (page: number = 1, limit: number = 20): Promise<ReportListResponse> => {
    const response = await api.get(`/reports/admin?page=${page}&limit=${limit}`);
    return response.data;
  },

  getReportStats: async (): Promise<ReportStats> => {
    const response = await api.get('/reports/admin/stats');
    return response.data;
  },

  dismissReport: async (reportId: number): Promise<Report> => {
    const response = await api.patch(`/reports/admin/${reportId}/dismiss`);
    return response.data;
  },

  actionReport: async (reportId: number, removeContent: boolean, warnUser: boolean): Promise<Report> => {
    const response = await api.patch(`/reports/admin/${reportId}/action`, {
      remove_content: removeContent,
      warn_user: warnUser,
    });
    return response.data;
  },
};
