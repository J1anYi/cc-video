import { useState, useEffect } from 'react';
import { reportsApi, Report, ReportStats } from '../../api/reports';

export default function AdminReports() {
  const [reports, setReports] = useState<Report[]>([]);
  const [stats, setStats] = useState<ReportStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [reportsRes, statsRes] = await Promise.all([
        reportsApi.getPendingReports(page, 20),
        reportsApi.getReportStats(),
      ]);
      setReports(reportsRes.reports);
      setTotalPages(Math.ceil(reportsRes.total / 20));
      setStats(statsRes);
    } catch (err) {
      console.error('Failed to load reports:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchData(); }, [page]);

  const handleDismiss = async (reportId: number) => {
    if (!confirm('Dismiss this report?')) return;
    await reportsApi.dismissReport(reportId);
    fetchData();
  };

  const handleAction = async (reportId: number) => {
    const warnUser = confirm('Issue warning to content author?');
    if (!confirm('Remove reported content?')) return;
    await reportsApi.actionReport(reportId, true, warnUser);
    fetchData();
  };

  if (loading) return <div className="p-8 text-center">Loading...</div>;

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Content Moderation</h1>

      {stats && (
        <div className="grid grid-cols-4 gap-4 mb-6">
          <div className="bg-yellow-100 p-4 rounded">
            <div className="text-2xl font-bold">{stats.pending}</div>
            <div>Pending</div>
          </div>
          <div className="bg-green-100 p-4 rounded">
            <div className="text-2xl font-bold">{stats.dismissed}</div>
            <div>Dismissed</div>
          </div>
          <div className="bg-red-100 p-4 rounded">
            <div className="text-2xl font-bold">{stats.actioned}</div>
            <div>Actioned</div>
          </div>
          <div className="bg-gray-100 p-4 rounded">
            <div className="text-2xl font-bold">{stats.total}</div>
            <div>Total</div>
          </div>
        </div>
      )}

      <div className="bg-white rounded-lg shadow">
        {reports.length === 0 ? (
          <div className="p-8 text-center text-gray-500">No pending reports</div>
        ) : (
          reports.map((report) => (
            <div key={report.id} className="p-4 border-b">
              <div className="flex justify-between items-start">
                <div>
                  <span className="font-medium capitalize">{report.content_type}</span>
                  <span className="text-gray-500"> #{report.content_id}</span>
                  <p className="text-sm text-gray-600 mt-1">{report.reason}</p>
                  <p className="text-xs text-gray-400 mt-1">
                    Reported: {new Date(report.created_at).toLocaleString()}
                  </p>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleDismiss(report.id)}
                    className="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300"
                  >
                    Dismiss
                  </button>
                  <button
                    onClick={() => handleAction(report.id)}
                    className="px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700"
                  >
                    Take Action
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {totalPages > 1 && (
        <div className="flex justify-center mt-4 gap-2">
          <button
            onClick={() => setPage(p => Math.max(1, p - 1))}
            disabled={page === 1}
            className="px-4 py-2 border rounded disabled:opacity-50"
          >
            Previous
          </button>
          <span className="px-4 py-2">Page {page} of {totalPages}</span>
          <button
            onClick={() => setPage(p => Math.min(totalPages, p + 1))}
            disabled={page === totalPages}
            className="px-4 py-2 border rounded disabled:opacity-50"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}
