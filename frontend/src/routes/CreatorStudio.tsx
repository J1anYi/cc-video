import React, { useState, useEffect } from 'react';
import { useAuth } from '../auth/AuthContext';
import api from '../api/axios';

export default function CreatorStudio() {
  const { user } = useAuth();
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('dashboard');

  useEffect(() => { fetchDashboard(); }, []);

  const fetchDashboard = async () => {
    try {
      const res = await api.get('/creator/dashboard');
      setDashboard(res.data);
    } catch (err) {} finally { setLoading(false); }
  };

  if (loading) return <div className="flex justify-center items-center h-64"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div></div>;

  if (!dashboard) return <CreateChannel onCreate={fetchDashboard} />;

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="bg-white rounded-lg shadow">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            {['dashboard', 'content', 'analytics', 'earnings', 'team'].map((tab) => (
              <button key={tab} onClick={() => setActiveTab(tab)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${activeTab === tab ? 'border-indigo-500 text-indigo-600' : 'border-transparent text-gray-500'}`}>
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
              </button>
            ))}
          </nav>
        </div>
        <div className="p-6">
          {activeTab === 'dashboard' && <DashboardTab dashboard={dashboard} />}
          {activeTab === 'content' && <ContentTab />}
          {activeTab === 'analytics' && <AnalyticsTab dashboard={dashboard} />}
          {activeTab === 'earnings' && <EarningsTab />}
          {activeTab === 'team' && <TeamTab />}
        </div>
      </div>
    </div>
  );
}

function CreateChannel({ onCreate }) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await api.post('/creator/profile', { channel_name: name, channel_description: description });
      onCreate();
    } catch (err) {}
  };

  return (
    <div className="max-w-md mx-auto mt-20 p-6 bg-white rounded-lg shadow">
      <h2 className="text-2xl font-bold mb-6">Create Your Channel</h2>
      <form onSubmit={handleCreate} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Channel Name</label>
          <input type="text" value={name} onChange={(e) => setName(e.target.value)} className="mt-1 block w-full rounded-md border-gray-300 shadow-sm" required />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Description</label>
          <textarea value={description} onChange={(e) => setDescription(e.target.value)} className="mt-1 block w-full rounded-md border-gray-300 shadow-sm" rows={3} />
        </div>
        <button type="submit" className="w-full py-2 px-4 bg-indigo-600 text-white rounded-md">Create Channel</button>
      </form>
    </div>
  );
}

function DashboardTab({ dashboard }) {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard title="Total Views" value={dashboard.total_views?.toLocaleString() || 0} />
        <StatCard title="Subscribers" value={dashboard.total_subscribers?.toLocaleString() || 0} />
        <StatCard title="Est. Revenue" value={`$${(dashboard.estimated_revenue || 0).toFixed(2)}`} />
        <StatCard title="Engagement" value={`${dashboard.engagement_rate || 0}%`} />
      </div>
      <div>
        <h3 className="text-lg font-medium mb-4">Recent Content</h3>
        <div className="space-y-2">
          {(dashboard.recent_content || []).map((content) => (
            <div key={content.id} className="p-4 bg-gray-50 rounded-lg flex justify-between items-center">
              <div>
                <p className="font-medium">{content.title}</p>
                <p className="text-sm text-gray-500">{content.status}</p>
              </div>
              <span className="text-sm text-gray-400">{new Date(content.created_at).toLocaleDateString()}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value }) {
  return (
    <div className="bg-gray-50 p-4 rounded-lg">
      <p className="text-sm text-gray-500">{title}</p>
      <p className="text-2xl font-bold">{value}</p>
    </div>
  );
}

function ContentTab() {
  const [contents, setContents] = useState([]);

  useEffect(() => { fetchContents(); }, []);

  const fetchContents = async () => {
    try {
      const res = await api.get('/creator/content');
      setContents(res.data);
    } catch (err) {}
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-medium">Your Content</h3>
        <button className="px-4 py-2 bg-indigo-600 text-white rounded-md">New Content</button>
      </div>
      <div className="space-y-2">
        {contents.map((content) => (
          <div key={content.id} className="p-4 bg-gray-50 rounded-lg flex justify-between items-center">
            <div>
              <p className="font-medium">{content.title}</p>
              <p className="text-sm text-gray-500">{content.status}</p>
            </div>
            <span className="text-sm text-gray-400">{new Date(content.created_at).toLocaleDateString()}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function AnalyticsTab({ dashboard }) {
  return (
    <div>
      <h3 className="text-lg font-medium mb-4">Analytics Overview</h3>
      <div className="grid grid-cols-2 gap-4">
        <div className="p-4 bg-gray-50 rounded-lg">
          <p className="text-sm text-gray-500">Total Views</p>
          <p className="text-3xl font-bold">{dashboard.total_views?.toLocaleString() || 0}</p>
        </div>
        <div className="p-4 bg-gray-50 rounded-lg">
          <p className="text-sm text-gray-500">Engagement Rate</p>
          <p className="text-3xl font-bold">{dashboard.engagement_rate || 0}%</p>
        </div>
      </div>
    </div>
  );
}

function EarningsTab() {
  return (
    <div>
      <h3 className="text-lg font-medium mb-4">Earnings</h3>
      <p className="text-gray-500">Earnings data will appear here once monetization is enabled.</p>
    </div>
  );
}

function TeamTab() {
  return (
    <div>
      <h3 className="text-lg font-medium mb-4">Team Members</h3>
      <p className="text-gray-500">Invite team members to collaborate on your channel.</p>
    </div>
  );
}
