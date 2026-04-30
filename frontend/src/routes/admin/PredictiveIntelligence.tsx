import { useState, useEffect } from 'react';
import { getDemandForecast, getPricingSuggestions, getContentGaps } from '../../api/predictions';

export default function PredictiveIntelligence() {
  const [demand, setDemand] = useState<any>(null);
  const [pricing, setPricing] = useState<any>(null);
  const [gaps, setGaps] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => { loadAll(); }, []);

  const loadAll = async () => {
    try {
      setLoading(true);
      const [d, p, g] = await Promise.all([getDemandForecast(30), getPricingSuggestions(), getContentGaps()]);
      setDemand(d);
      setPricing(p);
      setGaps(g);
    } finally { setLoading(false); }
  };

  if (loading) return <div className="p-8 text-gray-400">Loading predictions...</div>;

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Predictive Intelligence</h1>

      {demand && (
        <section className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Demand Forecast (30 Days)</h2>
          <div className="bg-gray-800 p-4 rounded-lg">
            <div className="text-2xl font-bold">{demand.total_predicted_views.toLocaleString()}</div>
            <div className="text-gray-400">Predicted Views</div>
          </div>
        </section>
      )}

      {pricing && (
        <section className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Pricing Suggestions</h2>
          <div className="grid grid-cols-3 gap-4">
            {pricing.suggestions.map((s: any) => (
              <div key={s.plan} className="bg-gray-800 p-4 rounded-lg">
                <div className="text-lg font-bold capitalize">{s.plan}</div>
                <div className="text-sm text-gray-400">${s.current_price} → ${s.suggested_price}</div>
              </div>
            ))}
          </div>
        </section>
      )}

      {gaps && (
        <section className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Content Gap Analysis</h2>
          <div className="grid grid-cols-4 gap-4">
            {gaps.gaps.slice(0, 8).map((g: any) => (
              <div key={g.genre} className="bg-gray-800 p-4 rounded-lg">
                <div className="font-bold">{g.genre}</div>
                <div className="text-sm text-gray-400">Gap: {(g.gap_score * 100).toFixed(0)}%</div>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
