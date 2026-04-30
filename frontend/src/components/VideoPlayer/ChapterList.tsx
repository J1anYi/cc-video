import React from 'react';

export interface Chapter {
  id: number;
  title: string;
  start_time: number;
  thumbnail_path: string | null;
}

interface ChapterListProps {
  chapters: Chapter[];
  currentTime: number;
  onChapterClick: (time: number) => void;
}

export const ChapterList: React.FC<ChapterListProps> = ({
  chapters,
  currentTime,
  onChapterClick,
}) => {
  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return String(m) + ':' + String(s).padStart(2, '0');
  };

  const isCurrentChapter = (chapter: Chapter, index: number) => {
    const nextChapter = chapters[index + 1];
    return currentTime >= chapter.start_time && 
           (!nextChapter || currentTime < nextChapter.start_time);
  };

  return (
    <div style={{ background: '#1a1a1a', borderRadius: '8px', padding: '8px' }}>
      <h4 style={{ margin: '0 0 8px 0', color: 'white' }}>Chapters</h4>
      {chapters.map((chapter, index) => (
        <button
          key={chapter.id}
          onClick={() => onChapterClick(chapter.start_time)}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            width: '100%',
            padding: '8px',
            background: isCurrentChapter(chapter, index) ? '#333' : 'transparent',
            border: isCurrentChapter(chapter, index) ? '1px solid #4CAF50' : 'none',
            borderRadius: '4px',
            color: 'white',
            cursor: 'pointer',
            textAlign: 'left' as const,
            marginBottom: '4px',
          }}
        >
          <div>
            <div style={{ fontWeight: 500 }}>{chapter.title}</div>
            <div style={{ fontSize: '12px', color: '#888' }}>{formatTime(chapter.start_time)}</div>
          </div>
        </button>
      ))}
    </div>
  );
};
