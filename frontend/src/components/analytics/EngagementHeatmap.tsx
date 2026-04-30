import { useRef, useEffect, useState } from 'react';
import type { HeatmapData } from '../../api/contentAnalytics';

interface Props {
  heatmapData: HeatmapData;
  width?: number;
  height?: number;
  showTooltip?: boolean;
}

export default function EngagementHeatmap({
  heatmapData,
  width = 800,
  height = 100,
  showTooltip = true,
}: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [tooltip, setTooltip] = useState<{
    x: number;
    y: number;
    timestamp: number;
    engagement: number;
  } | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || !heatmapData.samples.length) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear canvas
    ctx.fillStyle = '#1f2937';
    ctx.fillRect(0, 0, width, height);

    const samples = heatmapData.samples;
    const barWidth = width / samples.length;

    samples.forEach((sample, i) => {
      const engagement = Math.max(0, Math.min(100, sample.engagement_pct));
      const x = i * barWidth;
      const barHeight = height * (engagement / 100);

      // Color gradient: green (high) -> yellow -> red (low)
      let color: string;
      if (engagement >= 70) {
        color = '#22c55e'; // green
      } else if (engagement >= 40) {
        color = '#eab308'; // yellow
      } else {
        color = '#ef4444'; // red
      }

      ctx.fillStyle = color;
      ctx.fillRect(x, height - barHeight, barWidth - 1, barHeight);
    });

    // Draw timeline markers
    ctx.fillStyle = '#6b7280';
    ctx.font = '10px sans-serif';
    const duration = heatmapData.duration_seconds;
    const markers = [0, 0.25, 0.5, 0.75, 1];
    markers.forEach((m) => {
      const x = width * m;
      const seconds = Math.floor(duration * m);
      const minutes = Math.floor(seconds / 60);
      const secs = seconds % 60;
      ctx.fillText(`${minutes}:${secs.toString().padStart(2, '0')}`, x + 2, height - 5);
    });
  }, [heatmapData, width, height]);

  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!showTooltip || !heatmapData.samples.length) return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const sampleIndex = Math.floor((x / width) * heatmapData.samples.length);
    const sample = heatmapData.samples[sampleIndex];

    if (sample) {
      setTooltip({
        x: e.clientX - rect.left,
        y: e.clientY - rect.top,
        timestamp: sample.timestamp_seconds,
        engagement: sample.engagement_pct,
      });
    }
  };

  const handleMouseLeave = () => {
    setTooltip(null);
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="relative inline-block">
      <canvas
        ref={canvasRef}
        width={width}
        height={height}
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
        className="rounded cursor-crosshair"
      />
      {tooltip && (
        <div
          className="absolute pointer-events-none bg-gray-900 text-white px-2 py-1 rounded text-xs shadow-lg"
          style={{
            left: tooltip.x + 10,
            top: tooltip.y - 30,
          }}
        >
          <div>Time: {formatTime(tooltip.timestamp)}</div>
          <div>Engagement: {tooltip.engagement.toFixed(1)}%</div>
        </div>
      )}
    </div>
  );
}
