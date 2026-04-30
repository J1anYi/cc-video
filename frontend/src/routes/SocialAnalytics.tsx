import { useState, useEffect } from 'react';
import { socialAnalyticsApi, SocialAnalytics } from '../api/socialAnalytics';

export default function SocialAnalyticsPage() {
  const [data, setData] = useState<SocialAnalytics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => { loadAnalytics(); }, []);

  const loadAnalytics = async (refresh = false) => {
    setLoading(true);
    try {
      const result = refresh ? await socialAnalyticsApi.refresh() : await socialAnalyticsApi.getAnalytics();
      setData(result);
    } catch (e) { console.error(e); }
    finally { setLoading(false); }
  };

  if (loading || !data) return <div className="p-8 text-center text-gray-400">Loading...</div>;

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-white">Social Analytics</h1>
        <button onClick={() => loadAnalytics(true)} className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded text-sm">Refresh</button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-gray-800 rounded-lg p-4">
          <div className="text-3xl font-bold text-blue-400">{data.influence_score}</div>
          <div className="text-gray-400 text-sm">Influence Score</div>
        </div>
        <div className="bg-gray-800 rounded-lg p-4">
          <div className="text-3xl font-bold text-green-400">{data.followers}</div>
          <div className="text-gray-400 text-sm">Followers</div>
        </div>
        <div className="bg-gray-800 rounded-lg p-4">
          <div className="text-3xl font-bold text-purple-400">{data.following}</div>
          <div className="text-gray-400 text-sm">Following</div>
        </div>
        <div className="bg-gray-800 rounded-lg p-4">
          <div className="text-3xl font-bold text-yellow-400">{data.review_stats.total_helpful_votes}</div>
          <div className="text-gray-400 text-sm">Helpful Votes</div>
        </div>
      </div>

      <div className="bg-gray-800 rounded-lg p-6 mb-8">
        <h2 className="text-xl font-semibold text-white mb-4">Top Reviews</h2>
        {data.top_reviews.length > 0 ? (
          <div className="space-y-2">
            {data.top_reviews.map((r, i) => (
              <div key={r.review_id} className="flex justify-between p-2 hover:bg-gray-700 rounded">
                <span className="text-gray-300">{r.content}</span>
                <span className="text-yellow-400">{r.helpful_votes} helpful</span>
              </div>
            ))}
          </div>
        ) : <div className="text-gray-500">No reviews yet</div>}
      </div>
    </div>
  );
}
