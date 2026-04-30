import { useState, useEffect } from 'react';
import { get2FAStatus, enable2FA, disable2FA, getAuditLogs, exportUserData, requestDataDeletion } from '../../api/security';

export default function SecuritySettings() {
  const [twoFAEnabled, setTwoFAEnabled] = useState(false);
  const [secret, setSecret] = useState('');
  const [verifyCode, setVerifyCode] = useState('');
  const [auditLogs, setAuditLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => { loadSecurityData(); }, []);

  const loadSecurityData = async () => {
    try {
      setLoading(true);
      const [status, logs] = await Promise.all([get2FAStatus(), getAuditLogs(50)]);
      setTwoFAEnabled(status.enabled);
      setAuditLogs(logs);
    } finally { setLoading(false); }
  };

  const handleEnable2FA = async () => {
    const result = await enable2FA();
    setSecret(result.secret);
    setTwoFAEnabled(true);
  };

  const handleDisable2FA = async () => {
    await disable2FA();
    setTwoFAEnabled(false);
    setSecret('');
  };

  const handleExport = async () => {
    const data = await exportUserData();
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'user-data-export.json';
    a.click();
  };

  if (loading) return <div className="p-8 text-gray-400">Loading security settings...</div>;

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Security Settings</h1>

      <section className="bg-gray-800 p-6 rounded-lg mb-8">
        <h2 className="text-xl font-semibold mb-4">Two-Factor Authentication</h2>
        <div className="flex items-center gap-4">
          <span className={twoFAEnabled ? 'text-green-400' : 'text-red-400'}>
            Status: {twoFAEnabled ? 'Enabled' : 'Disabled'}
          </span>
          {twoFAEnabled ? (
            <button onClick={handleDisable2FA} className="bg-red-600 px-4 py-2 rounded">Disable 2FA</button>
          ) : (
            <button onClick={handleEnable2FA} className="bg-green-600 px-4 py-2 rounded">Enable 2FA</button>
          )}
        </div>
        {secret && <div className="mt-4 text-sm text-gray-400">Secret: {secret}</div>}
      </section>

      <section className="bg-gray-800 p-6 rounded-lg mb-8">
        <h2 className="text-xl font-semibold mb-4">GDPR Data Rights</h2>
        <div className="flex gap-4">
          <button onClick={handleExport} className="bg-blue-600 px-4 py-2 rounded">Export My Data</button>
          <button onClick={() => requestDataDeletion()} className="bg-red-600 px-4 py-2 rounded">Request Deletion</button>
        </div>
      </section>

      <section className="bg-gray-800 p-6 rounded-lg">
        <h2 className="text-xl font-semibold mb-4">Audit Logs</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-700">
                <th className="text-left p-2">Action</th>
                <th className="text-left p-2">Resource</th>
                <th className="text-left p-2">IP</th>
                <th className="text-left p-2">Time</th>
              </tr>
            </thead>
            <tbody>
              {auditLogs.slice(0, 20).map((log) => (
                <tr key={log.id} className="border-b border-gray-700">
                  <td className="p-2">{log.action}</td>
                  <td className="p-2">{log.resource_type} #{log.resource_id}</td>
                  <td className="p-2">{log.ip_address}</td>
                  <td className="p-2">{new Date(log.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
