import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../auth/AuthContext';
import { getMovies, getCategories } from '../api/movies';
import { getFavoriteStatus, addFavorite, removeFavorite } from '../api/favorites';
import type { Movie } from '../api/types';

export default function Catalog() {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const { user, logout } = useAuth();

  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');
  const [favoriteStatus, setFavoriteStatus] = useState<Record<number, boolean>>({});

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedSearch(searchTerm), 300);
    return () => clearTimeout(timer);
  }, [searchTerm]);

  useEffect(() => { loadCategories(); }, []);
  useEffect(() => { loadMovies(); }, [debouncedSearch, selectedCategory]);

  const loadCategories = async () => {
    try { setCategories(await getCategories()); } catch (err) { console.error(err); }
  };

  const loadMovies = async () => {
    setIsLoading(true);
    try {
      const response = await getMovies({
        q: debouncedSearch || undefined,
        category: selectedCategory || undefined,
      });
      setMovies(response.movies);
      loadFavoriteStatuses(response.movies.map(m => m.id));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load movies');
    } finally { setIsLoading(false); }
  };

  const loadFavoriteStatuses = async (movieIds: number[]) => {
    const statuses: Record<number, boolean> = {};
    for (const id of movieIds) {
      try {
        const status = await getFavoriteStatus(id);
        statuses[id] = status.is_favorite;
      } catch {
        statuses[id] = false;
      }
    }
    setFavoriteStatus(statuses);
  };

  const toggleFavorite = async (movieId: number, e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    try {
      if (favoriteStatus[movieId]) {
        await removeFavorite(movieId);
        setFavoriteStatus(prev => ({ ...prev, [movieId]: false }));
      } else {
        await addFavorite(movieId);
        setFavoriteStatus(prev => ({ ...prev, [movieId]: true }));
      }
    } catch (err) {
      console.error('Failed to toggle favorite:', err);
    }
  };

  const clearFilters = () => { setSearchTerm(''); setSelectedCategory(''); };
  const hasActiveFilters = searchTerm || selectedCategory;

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.title}>CC Video</h1>
        <div style={styles.userSection}>
          <Link to="/favorites" style={styles.navLink}>Favorites</Link>
          <Link to="/history" style={styles.navLink}>History</Link>
          <span>Welcome, {user?.username}</span>
          <button onClick={logout} style={styles.logoutButton}>Logout</button>
        </div>
      </header>

      <div style={styles.filterSection}>
        <input type="text" placeholder="Search movies..." value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)} style={styles.searchInput} />
        <select value={selectedCategory} onChange={(e) => setSelectedCategory(e.target.value)} style={styles.categorySelect}>
          <option value="">All Categories</option>
          {categories.map((cat) => (<option key={cat} value={cat}>{cat}</option>))}
        </select>
        {hasActiveFilters && <button onClick={clearFilters} style={styles.clearButton}>Clear</button>}
      </div>

      {error && <div style={styles.error}>{error}</div>}
      {hasActiveFilters && !isLoading && <p style={styles.resultsCount}>{movies.length} result{movies.length !== 1 ? 's' : ''}</p>}

      {isLoading ? <p style={styles.loading}>Loading...</p> : movies.length === 0 ? (
        <div style={styles.empty}>
          <p>No movies found.</p>
          {hasActiveFilters && <button onClick={clearFilters} style={styles.clearButton}>Clear Filters</button>}
        </div>
      ) : (
        <div style={styles.grid}>
          {movies.map((movie) => (
            <Link key={movie.id} to={`/movies/${movie.id}`} style={styles.card}>
              <div style={styles.cardHeader}>
                <h2 style={styles.cardTitle}>{movie.title}</h2>
                <button
                  onClick={(e) => toggleFavorite(movie.id, e)}
                  style={styles.favoriteButton}
                  title={favoriteStatus[movie.id] ? 'Remove from favorites' : 'Add to favorites'}
                >
                  {favoriteStatus[movie.id] ? '❤️' : '🤍'}
                </button>
              </div>
              {movie.category && <span style={styles.cardCategory}>{movie.category}</span>}
              <p style={styles.cardDescription}>{movie.description || 'No description'}</p>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: { maxWidth: '1200px', margin: '0 auto', padding: '1rem' },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', padding: '1rem 0', borderBottom: '1px solid #eee' },
  title: { margin: 0, fontSize: '1.5rem' },
  userSection: { display: 'flex', alignItems: 'center', gap: '1rem' },
  navLink: { color: '#666', textDecoration: 'none' },
  logoutButton: { padding: '0.5rem 1rem', background: '#6c757d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  filterSection: { display: 'flex', gap: '1rem', marginBottom: '1.5rem', flexWrap: 'wrap' },
  searchInput: { flex: 1, minWidth: '200px', padding: '0.75rem', border: '1px solid #ddd', borderRadius: '4px', fontSize: '1rem' },
  categorySelect: { padding: '0.75rem', border: '1px solid #ddd', borderRadius: '4px', fontSize: '1rem', minWidth: '150px' },
  clearButton: { padding: '0.75rem 1rem', background: '#e0e0e0', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  error: { padding: '1rem', background: '#fee', color: '#c00', borderRadius: '4px', marginBottom: '1rem' },
  resultsCount: { color: '#666', marginBottom: '1rem' },
  loading: { textAlign: 'center', padding: '2rem', color: '#666' },
  empty: { textAlign: 'center', color: '#666', padding: '2rem' },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '1.5rem' },
  card: { background: 'white', borderRadius: '8px', padding: '1.5rem', boxShadow: '0 2px 8px rgba(0,0,0,0.1)', textDecoration: 'none', color: 'inherit' },
  cardHeader: { display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '0.5rem' },
  cardTitle: { margin: 0, fontSize: '1.25rem', flex: 1 },
  favoriteButton: { background: 'none', border: 'none', fontSize: '1.25rem', cursor: 'pointer', padding: '0.25rem' },
  cardCategory: { display: 'inline-block', padding: '0.25rem 0.5rem', background: '#e3f2fd', color: '#1976d2', borderRadius: '4px', fontSize: '0.75rem', marginBottom: '0.5rem' },
  cardDescription: { margin: 0, color: '#666', fontSize: '0.875rem', lineHeight: 1.5 },
};
