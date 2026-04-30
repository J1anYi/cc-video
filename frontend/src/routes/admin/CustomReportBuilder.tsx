import { useState, useEffect } from 'react';
import { getReports, createReport, executeReport, exportReport, scheduleReport, shareReport, getDashboardConfig, updateDashboardConfig } from '../../api/customReports';

export default function CustomReportBuilder() {
  const [reports, setReports] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [selectedReport, setSelectedReport] = useState<any>(null);
  const [result, setResult] = useState<any>(null);
  const [dashboardConfig, setDashboardConfig] = useState<any>(null);
  
  const [newReport, setNewReport] = useState({
    name: '',
    report_type: 'content',
    data_source: 'movies',
    description: '',
    is_public: false
  });

  useEffect(() => { loadReports(); loadDashboardConfig(); }, []);

  const loadReports = async () => {
    try {
      setLoading(true);
      const data = await getReports();
      setReports(data);
    } finally { setLoading(false); }
  };

  const loadDashboardConfig = async () => {
    try {
      const config = await getDashboardConfig();
      setDashboardConfig(config);
    } catch (e) {}
  };

  const handleCreate = async () => {
    await createReport(newReport);
    setShowCreate(false);
    setNewReport({ name: '', report_type: 'content', data_source: 'movies', description: '', is_public: false });
    loadReports();
  };

  const handleExecute = async (id: number) => {
    const res = await executeReport(id);
    setResult(res);
    setSelectedReport(id);
  };

  const handleExport = async (id: number, format: string) => {
    const res = await exportReport(id, format);
    if (format === 'csv') {
      const blob = new Blob([res.content], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'report.csv';
      a.click();
    } else {
      alert(`${format.toUpperCase()} export: ${res.content}`);
    }
  };

  if (loading) return <div className="p-8 text-gray-400">Loading reports...</div>;

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Custom Report Builder</h1>
        <button onClick={() => setShowCreate(true)} className="bg-blue-600 px-4 py-2 rounded-lg">Create Report</button>
      </div>

      {showCreate && (
        <div className="bg-gray-800 p-6 rounded-lg mb-8">
          <h2 className="text-xl font-semibold mb-4">New Report</h2>
          <div className="grid grid-cols-2 gap-4">
            <input placeholder="Report Name" value={newReport.name} onChange={e => setNewReport({...newReport, name: e.target.value})} className="bg-gray-700 p-2 rounded" />
            <select value={newReport.report_type} onChange={e => setNewReport({...newReport, report_type: e.target.value})} className="bg-gray-700 p-2 rounded">
              <option value="content">Content</option>
              <option value="user">User</option>
              <option value="revenue">Revenue</option>
            </select>
            <input placeholder="Description" value={newReport.description} onChange={e => setNewReport({...newReport, description: e.target.value})} className="bg-gray-700 p-2 rounded" />
            <label className="flex items-center gap-2">
              <input type="checkbox" checked={newReport.is_public} onChange={e => setNewReport({...newReport, is_public: e.target.checked})} />
              Public
            </label>
          </div>
          <div className="mt-4 flex gap-2">
            <button onClick={handleCreate} className="bg-green-600 px-4 py-2 rounded">Create</button>
            <button onClick={() => setShowCreate(false)} className="bg-gray-600 px-4 py-2 rounded">Cancel</button>
          </div>
        </div>
      )}

      {result && selectedReport && (
        <div className="bg-gray-800 p-6 rounded-lg mb-8">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Report Results</h2>
            <div className="flex gap-2">
              <button onClick={() => handleExport(selectedReport, 'csv')} className="bg-blue-600 px-3 py-1 rounded text-sm">CSV</button>
              <button onClick={() => handleExport(selectedReport, 'xlsx')} className="bg-blue-600 px-3 py-1 rounded text-sm">Excel</button>
              <button onClick={() => handleExport(selectedReport, 'pdf')} className="bg-blue-600 px-3 py-1 rounded text-sm">PDF</button>
            </div>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-700">
                  {result.data?.columns?.map((c: string, i: number) => (
                    <th key={i} className="text-left p-2">{c}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {result.data?.rows?.map((row: any[], i: number) => (
                  <tr key={i} className="border-b border-gray-700">
                    {row.map((cell, j) => (
                      <td key={j} className="p-2">{cell}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="text-sm text-gray-400 mt-2">Total rows: {result.row_count}</div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {reports.map(r => (
          <div key={r.id} className="bg-gray-800 p-4 rounded-lg">
            <div className="font-bold text-lg">{r.name}</div>
            <div className="text-sm text-gray-400 capitalize">{r.report_type}</div>
            <div className="text-xs text-gray-500">{r.is_public ? 'Public' : 'Private'}</div>
            <div className="mt-3 flex gap-2">
              <button onClick={() => handleExecute(r.id)} className="bg-green-600 px-3 py-1 rounded text-sm">Run</button>
              <button onClick={() => handleExport(r.id, 'csv')} className="bg-blue-600 px-3 py-1 rounded text-sm">Export</button>
            </div>
          </div>
        ))}
      </div>

      {dashboardConfig && (
        <div className="mt-8 bg-gray-800 p-6 rounded-lg">
          <h2 className="text-xl font-semibold mb-4">Dashboard Configuration</h2>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm text-gray-400">Theme</label>
              <select value={dashboardConfig.theme} onChange={e => setDashboardConfig({...dashboardConfig, theme: e.target.value})} className="bg-gray-700 p-2 rounded w-full">
                <option value="dark">Dark</option>
                <option value="light">Light</option>
              </select>
            </div>
            <div>
              <label className="text-sm text-gray-400">Refresh Interval (seconds)</label>
              <input type="number" value={dashboardConfig.refresh_interval} onChange={e => setDashboardConfig({...dashboardConfig, refresh_interval: parseInt(e.target.value)})} className="bg-gray-700 p-2 rounded w-full" />
            </div>
          </div>
          <button onClick={async () => { await updateDashboardConfig(dashboardConfig); alert('Config saved'); }} className="mt-4 bg-blue-600 px-4 py-2 rounded">Save Configuration</button>
        </div>
      )}
    </div>
  );
}
