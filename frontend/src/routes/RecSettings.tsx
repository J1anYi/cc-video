import { useState, useEffect } from 'react';
import { recInsightsApi, RecPrefs } from '../api/recInsights';

export default function RecSettings() {
  const [prefs, setPrefs] = useState<RecPrefs | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => { loadPrefs(); }, []);

  const loadPrefs = async () => {
    setLoading(true);
    try { setPrefs(await recInsightsApi.getPrefs()); }
    catch (e) { console.error(e); }
    finally { setLoading(false); }
  };

  const updateWeight = async (key: string, value: number) => {
    if (!prefs) return;
    await recInsightsApi.updatePrefs({ [key]: value });
    setPrefs({ ...prefs, [key]: value });
  };

  if (loading || !prefs) return <div className="p-8 text-center text-gray-400">Loading...</div>;

  return (
    <div className="p-8 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold text-white mb-8">Recommendation Settings</h1>
      <div className="bg-gray-800 rounded-lg p-6 space-y-6">
        <div>
          <label className="text-gray-300 block mb-2">Recency Weight: {prefs.recency_weight}</label>
          <input type="range" min="0" max="1" step="0.1" value={prefs.recency_weight}
            onChange={(e) => updateWeight('recency_weight', parseFloat(e.target.value))}
            className="w-full" />
        </div>
        <div>
          <label className="text-gray-300 block mb-2">Social Weight: {prefs.social_weight}</label>
          <input type="range" min="0" max="1" step="0.1" value={prefs.social_weight}
            onChange={(e) => updateWeight('social_weight', parseFloat(e.target.value))}
            className="w-full" />
        </div>
        <div>
          <label className="text-gray-300 block mb-2">Popularity Weight: {prefs.popularity_weight}</label>
          <input type="range" min="0" max="1" step="0.1" value={prefs.popularity_weight}
            onChange={(e) => updateWeight('popularity_weight', parseFloat(e.target.value))}
            className="w-full" />
        </div>
      </div>
    </div>
  );
}
