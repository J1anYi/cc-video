import React from 'react';

export interface AudioTrack {
  id: number;
  language: string;
  title: string | null;
  is_default: boolean;
  is_original: boolean;
  channel_layout: string;
}

interface AudioTrackSelectorProps {
  tracks: AudioTrack[];
  currentTrack: number;
  onTrackChange: (trackId: number) => void;
}

export const AudioTrackSelector: React.FC<AudioTrackSelectorProps> = ({
  tracks,
  currentTrack,
  onTrackChange,
}) => {
  const [isOpen, setIsOpen] = React.useState(false);

  const getTrackLabel = (track: AudioTrack) => {
    if (track.title) return track.title;
    const langNames: Record<string, string> = {
      en: 'English', zh: 'Chinese', ja: 'Japanese', ko: 'Korean',
      es: 'Spanish', fr: 'French', de: 'German'
    };
    const name = langNames[track.language] || track.language.toUpperCase();
    const suffix = track.is_original ? ' (Original)' : '';
    const channels = track.channel_layout === '5.1' ? ' Surround' : 
                     track.channel_layout === '7.1' ? ' Surround 7.1' : '';
    return name + suffix + channels;
  };

  const currentTrackObj = tracks.find(t => t.id === currentTrack);

  return (
    <div style={{ position: 'relative', display: 'inline-block' }}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          padding: '0.5rem 1rem',
          background: 'rgba(0, 0, 0, 0.7)',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
          fontSize: '14px',
        }}
      >
        Audio: {currentTrackObj ? getTrackLabel(currentTrackObj) : 'Select'}
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
          {tracks.map((track) => (
            <button
              key={track.id}
              onClick={() => { onTrackChange(track.id); setIsOpen(false); }}
              style={{
                width: '100%',
                padding: '8px 16px',
                background: currentTrack === track.id ? 'rgba(255,255,255,0.1)' : 'none',
                border: 'none',
                color: 'white',
                cursor: 'pointer',
                textAlign: 'left' as const,
              }}
            >
              {getTrackLabel(track)}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};
