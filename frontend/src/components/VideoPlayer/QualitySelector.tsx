import React from 'react';

export interface QualityOption {
  quality: string;
  width: number;
  height: number;
  bitrate: number;
}

interface QualitySelectorProps {
  qualities: QualityOption[];
  currentQuality: string;
  onQualityChange: (quality: string) => void;
  isAuto: boolean;
  onAutoToggle: () => void;
}

export const QualitySelector: React.FC<QualitySelectorProps> = ({
  qualities,
  currentQuality,
  onQualityChange,
  isAuto,
  onAutoToggle,
}) => {
  const [isOpen, setIsOpen] = React.useState(false);

  const qualityLabels: Record<string, string> = {
    '4K': '4K (2160p)',
    '1080p': 'Full HD (1080p)',
    '720p': 'HD (720p)',
    '480p': 'SD (480p)',
    '360p': 'Low (360p)',
  };

  const getCurrentLabel = () => {
    if (isAuto) return 'Auto';
    return qualityLabels[currentQuality] || currentQuality;
  };

  return (
    <div style={{ position: 'relative', display: 'inline-block' }}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          padding: '0.5rem 1rem',
          background: 'rgba(0, 0, 0, 0.7)',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
          fontSize: '14px',
        }}
      >
        <span>Auto</span>
        <span>{getCurrentLabel()}</span>
      </button>

      {isOpen && (
        <div style={{
          position: 'absolute',
          bottom: '100%',
          right: 0,
          marginBottom: '8px',
          background: 'rgba(0, 0, 0, 0.9)',
          borderRadius: '8px',
          padding: '8px 0',
          minWidth: '200px',
        }}>
          <button
            style={{
              width: '100%',
              padding: '8px 16px',
              background: isAuto ? 'rgba(255,255,255,0.1)' : 'none',
              border: 'none',
              color: 'white',
              cursor: 'pointer',
              textAlign: 'left' as const,
            }}
            onClick={() => { onAutoToggle(); setIsOpen(false); }}
          >
            Auto (Recommended)
          </button>
          {qualities.sort((a, b) => b.height - a.height).map((q) => (
            <button
              key={q.quality}
              style={{
                width: '100%',
                padding: '8px 16px',
                background: currentQuality === q.quality && !isAuto ? 'rgba(255,255,255,0.1)' : 'none',
                border: 'none',
                color: 'white',
                cursor: 'pointer',
                textAlign: 'left' as const,
              }}
              onClick={() => { onQualityChange(q.quality); setIsOpen(false); }}
            >
              {qualityLabels[q.quality] || q.quality}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};
