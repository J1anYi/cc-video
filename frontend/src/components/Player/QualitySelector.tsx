import React, { useState, useEffect } from 'react';
import { streamingApi, StreamVariant, QualityPreferences } from '../../api/streaming';

interface QualitySelectorProps {
  movieId: number;
  currentQuality?: string;
  onQualityChange?: (quality: string, hlsUrl: string) => void;
}

export const QualitySelector: React.FC<QualitySelectorProps> = ({
  movieId,
  currentQuality = 'auto',
  onQualityChange,
}) => {
  const [variants, setVariants] = useState<StreamVariant[]>([]);
  const [preferences, setPreferences] = useState<QualityPreferences | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [variantsData, prefsData] = await Promise.all([
          streamingApi.getMovieVariants(movieId),
          streamingApi.getPreferences(),
        ]);
        setVariants(variantsData);
        setPreferences(prefsData);
      } catch (error) {
        console.error('Failed to fetch quality data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [movieId]);

  const handleQualityChange = async (quality: string) => {
    const variant = variants.find(v => v.quality === quality);
    if (variant) {
      onQualityChange?.(quality, variant.hls_url);
    } else if (quality === 'auto') {
      onQualityChange?.('auto', '');
    }
  };

  if (loading) return null;

  return (
    <div className="quality-selector">
      <select
        value={currentQuality}
        onChange={(e) => handleQualityChange(e.target.value)}
        className="quality-select"
      >
        <option value="auto">Auto</option>
        {variants.map((v) => (
          <option key={v.id} value={v.quality}>
            {v.quality.toUpperCase()} ({v.resolution})
          </option>
        ))}
      </select>
    </div>
  );
};

export const BandwidthIndicator: React.FC = () => {
  const [bandwidth, setBandwidth] = useState<number>(0);
  const [recommended, setRecommended] = useState<string>('');

  useEffect(() => {
    const measureBandwidth = async () => {
      try {
        const stats = await streamingApi.getBandwidthStats();
        setBandwidth(stats.avg_bandwidth_kbps);
        if (stats.avg_bandwidth_kbps > 0) {
          const rec = await streamingApi.getRecommendedQuality(stats.avg_bandwidth_kbps);
          setRecommended(rec);
        }
      } catch (error) {
        console.error('Failed to get bandwidth:', error);
      }
    };
    measureBandwidth();
  }, []);

  const formatBandwidth = (kbps: number) => {
    if (kbps >= 1000) {
      return (kbps / 1000).toFixed(1) + ' Mbps';
    }
    return kbps + ' kbps';
  };

  return (
    <div className="bandwidth-indicator">
      <span className="bandwidth-value">{formatBandwidth(bandwidth)}</span>
      {recommended && (
        <span className="recommended-quality">Recommended: {recommended.toUpperCase()}</span>
      )}
    </div>
  );
};
