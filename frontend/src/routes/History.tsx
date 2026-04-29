import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getWatchHistory } from '../api/history';
import type { WatchHistory as WatchHistoryType } from '../api/types';

export default function History() {
  const [history, setHistory] = useState<WatchHistoryType[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => { loadHistory(); }, []);

  const loadHistory = async () => {
    try { setHistory(await getWatchHistory()); } catch (e) { console.error(e); }
    finally { setIsLoading(false); }
  };

  if (isLoading) return <div style={styles.container}><p>Loading...</p></div>;

  return (
    <div style={styles.container}>
      <h1>Watch History</h1>
      {history.length === 0 ? <p>No movies watched. <Link to="/movies">Browse</Link></p> :
        <div style={styles.grid}>{history.map(e => e.movie && (
          <Link key={e.id} to={`/movies/${e.movie_id}?t=${e.progress}`} style={styles.card}>
            <h3>{e.movie.title}</h3>
            <div style={styles.progressContainer}><div style={{...styles.progressBar, width: `${e.progress}%`}} /></div>
            <span>{Math.round(e.progress)}% watched</span>
          </Link>
        ))}</div>}
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: { padding: '2rem', maxWidth: '1200px', margin: '0 auto' },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '1.5rem' },
  card: { background: 'white', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)', textDecoration: 'none', color: 'inherit', padding: '1rem' },
  progressContainer: { height: '4px', background: '#eee', borderRadius: '2px', margin: '0.75rem 0' },
  progressBar: { height: '100%', background: '#007bff', borderRadius: '2px' },
};
