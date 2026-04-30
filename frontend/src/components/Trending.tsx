import { Link } from 'react-router-dom';
import type { TrendingMovie } from '../api/trending';

interface TrendingProps {
  items: TrendingMovie[];
}

export default function Trending({ items }: TrendingProps) {
  if (items.length === 0) return null;
  return (
    <section style={{ marginBottom: '2rem' }}>
      <h2 style={{ fontSize: '1.25rem', marginBottom: '1rem' }}>Trending</h2>
      <div style={{ display: 'flex', gap: '1rem', overflowX: 'auto' }}>
        {items.map((item) => (
          <Link key={item.movie.id} to={'/movies/' + item.movie.id}
            style={{ flex: '0 0 200px', background: 'white', borderRadius: '8px', overflow: 'hidden', textDecoration: 'none', color: 'inherit' }}>
            {item.movie.poster_path ? (
              <img src={'http://localhost:8000' + item.movie.poster_path} alt={item.movie.title} style={{ width: '100%', height: '120px', objectFit: 'cover' }} />
            ) : (<div style={{ width: '100%', height: '120px', background: '#e0e0e0', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>🎬</div>)}
            <div style={{ padding: '0.75rem' }}>
              <h3 style={{ margin: 0, fontSize: '0.875rem' }}>{item.movie.title}</h3>
              <span style={{ fontSize: '0.75rem', color: '#666' }}>{item.view_count} views</span>
            </div>
          </Link>
        ))}
      </div>
    </section>
  );
}
