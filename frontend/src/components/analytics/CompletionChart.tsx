import { useRef, useEffect } from 'react';
import type { CompletionAnalysis } from '../../api/contentAnalytics';

interface Props {
  completionData: CompletionAnalysis;
  width?: number;
  height?: number;
}

export default function CompletionChart({
  completionData,
  width = 800,
  height = 250,
}: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear canvas
    ctx.fillStyle = '#1f2937';
    ctx.fillRect(0, 0, width, height);

    const padding = { top: 20, right: 20, bottom: 40, left: 50 };
    const chartWidth = width - padding.left - padding.right;
    const chartHeight = height - padding.top - padding.bottom;

    // Draw axes
    ctx.strokeStyle = '#4b5563';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(padding.left, padding.top);
    ctx.lineTo(padding.left, height - padding.bottom);
    ctx.lineTo(width - padding.right, height - padding.bottom);
    ctx.stroke();

    // Draw Y-axis labels (0-100%)
    ctx.fillStyle = '#9ca3af';
    ctx.font = '10px sans-serif';
    ctx.textAlign = 'right';
    for (let i = 0; i <= 100; i += 25) {
      const y = padding.top + chartHeight * (1 - i / 100);
      ctx.fillText(`${i}%`, padding.left - 5, y + 4);

      // Grid line
      ctx.strokeStyle = '#374151';
      ctx.beginPath();
      ctx.moveTo(padding.left, y);
      ctx.lineTo(width - padding.right, y);
      ctx.stroke();
    }

    // Draw retention curve
    const dropOffs = completionData.drop_off_points;
    if (dropOffs.length > 0) {
      ctx.strokeStyle = '#3b82f6';
      ctx.lineWidth = 2;
      ctx.beginPath();

      // Start at 100%
      ctx.moveTo(padding.left, padding.top);

      // Draw curve through drop-off points
      dropOffs.forEach((point, i) => {
        const x = padding.left + (chartWidth * (i + 1)) / dropOffs.length;
        const retention = 100 - point.drop_pct;
        const y = padding.top + chartHeight * (1 - retention / 100);

        if (i === 0) {
          ctx.lineTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      });

      ctx.stroke();

      // Draw drop-off markers
      dropOffs.forEach((point, i) => {
        const x = padding.left + (chartWidth * (i + 1)) / dropOffs.length;
        const retention = 100 - point.drop_pct;
        const y = padding.top + chartHeight * (1 - retention / 100);

        // Marker dot
        ctx.fillStyle = '#ef4444';
        ctx.beginPath();
        ctx.arc(x, y, 4, 0, Math.PI * 2);
        ctx.fill();

        // Drop percentage label
        ctx.fillStyle = '#fca5a5';
        ctx.font = '9px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(`-${point.drop_pct.toFixed(0)}%`, x, y - 10);
      });
    }

    // Draw completion rate line
    const completionY = padding.top + chartHeight * (1 - completionData.completion_rate / 100);
    ctx.strokeStyle = '#22c55e';
    ctx.lineWidth = 1;
    ctx.setLineDash([5, 5]);
    ctx.beginPath();
    ctx.moveTo(padding.left, completionY);
    ctx.lineTo(width - padding.right, completionY);
    ctx.stroke();
    ctx.setLineDash([]);

    // Label completion rate
    ctx.fillStyle = '#86efac';
    ctx.font = '11px sans-serif';
    ctx.textAlign = 'right';
    ctx.fillText(
      `Avg: ${completionData.completion_rate.toFixed(1)}%`,
      width - padding.right - 5,
      completionY - 5
    );

    // X-axis label
    ctx.fillStyle = '#9ca3af';
    ctx.font = '11px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Video Progress (%)', width / 2, height - 5);

  }, [completionData, width, height]);

  return (
    <div className="inline-block">
      <canvas ref={canvasRef} width={width} height={height} className="rounded" />
    </div>
  );
}
