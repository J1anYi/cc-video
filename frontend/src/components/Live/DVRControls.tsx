import React, { useState, useEffect } from 'react';
import { livestreamApi, DVRSegment } from '../../api/livestream';

interface DVRControlsProps {
  streamId: number;
}

export const DVRControls: React.FC<DVRControlsProps> = ({ streamId }) => {
  const [segments, setSegments] = useState<DVRSegment[]>([]);
  const [currentTime, setCurrentTime] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSegments = async () => {
      try {
        const data = await livestreamApi.getDVRSegments(streamId);
        setSegments(data);
      } catch (error) {
        console.error('Failed to fetch DVR segments:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchSegments();
  }, [streamId]);

  const totalDuration = segments.reduce((acc, s) => acc + s.segment_duration, 0);

  const handleSeek = (time: number) => {
    setCurrentTime(time);
  };

  if (loading) return <div>Loading DVR controls...</div>;

  return (
    <div className="dvr-controls">
      <h3>DVR Controls</h3>
      <div className="timeline">
        <input
          type="range"
          min={0}
          max={totalDuration}
          value={currentTime}
          onChange={(e) => handleSeek(Number(e.target.value))}
        />
      </div>
      <div className="segment-list">
        {segments.map((segment, index) => (
          <div key={segment.id} className="segment">
            <span>Segment {index + 1}</span>
            <span>{segment.segment_duration}s</span>
            <button onClick={() => window.open(segment.segment_url, '_blank')}>
              View
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};
