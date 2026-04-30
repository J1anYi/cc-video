import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../auth/AuthContext';
import { getMovies, getCategories } from '../api/movies';
import { getFavoriteStatus, addFavorite, removeFavorite } from '../api/favorites';
import { getRecommendations } from '../api/recommendations';
import { getTrending } from '../api/trending';
import type { Movie } from '../api/types';
import type { RecommendationsResponse } from '../api/recommendations';
import type { TrendingResponse } from '../api/trending';
import type { MovieSearchParams } from '../api/movies';
import ContinueWatching from '../components/ContinueWatching';
import Recommendations from '../components/Recommendations';
import Trending from '../components/Trending';

export default function Catalog() {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [recommendations, setRecommendations] = useState<RecommendationsResponse | null>(null);
  const [trending, setTrending] = useState<TrendingResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const { user, logout } = useAuth();

  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');
  const [favoriteStatus, setFavoriteStatus] = useState<Record<number, boolean>>({});

  // Advanced filters
  const [showFilters, setShowFilters] = useState(false);
  const [yearFrom, setYearFrom] = useState('');
  const [yearTo, setYearTo] = useState('');
  const [durationFrom, setDurationFrom] = useState('');
  const [durationTo, setDurationTo] = useState('');
  const [sortBy, setSortBy] = useState<'rating' | 'year' | 'title' | 'created_at'>('created_at');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedSearch(searchTerm), 300);
    return () => clearTimeout(timer);
  }, [searchTerm]);

  useEffect(() => { loadCategories(); loadRecommendations(); loadTrending(); }, []);
  useEffect(() => { loadMovies(); }, [debouncedSearch, selectedCategory, yearFrom, yearTo, durationFrom, durationTo, sortBy, sortOrder]);

  const loadCategories = async () => {
    try { setCategories(await getCategories()); } catch (err) { console.error(err); }
  };

  const loadRecommendations = async () => {
    try {
      const recs = await getRecommendations();
      setRecommendations(recs);
    } catch (err) {
      console.error('Failed to load recommendations:', err);
    }
  };

  const loadTrending = async () => {
    try {
      const t = await getTrending();
      setTrending(t);
    } catch (err) {
      console.error('Failed to load trending:', err);
    }
  };

  const loadMovies = async () => {
    setIsLoading(true);
    try {
      const params: MovieSearchParams = {
        q: debouncedSearch || undefined,
        category: selectedCategory || undefined,
        year_from: yearFrom ? parseInt(yearFrom) : undefined,
        year_to: yearTo ? parseInt(yearTo) : undefined,
        duration_from: durationFrom ? parseInt(durationFrom) : undefined,
        duration_to: durationTo ? parseInt(durationTo) : undefined,
        sort_by: sortBy,
        sort_order: sortOrder,
      };
      const response = await getMovies(params);
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

  const clearFilters = () => {
    setSearchTerm('');
    setSelectedCategory('');
    setYearFrom('');
    setYearTo('');
    setDurationFrom('');
    setDurationTo('');
    setSortBy('created_at');
    setSortOrder('desc');
  };

  const hasActiveFilters = searchTerm || selectedCategory || yearFrom || yearTo || durationFrom || durationTo;

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

      {!hasActiveFilters && trending && (
        <Trending items={trending.movies} />
      )}

      {!hasActiveFilters && recommendations && (
        <>
          <ContinueWatching items={recommendations.continue_watching} />
          <Recommendations items={recommendations.recommendations} />
        </>
      )}

      <div style={styles.filterSection}>
        <input type="text" placeholder="Search movies..." value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)} style={styles.searchInput} />
        <select value={selectedCategory} onChange={(e) => setSelectedCategory(e.target.value)} style={styles.categorySelect}>
          <option value="">All Categories</option>
          {categories.map((cat) => (<option key={cat} value={cat}>{cat}</option>))}
        </select>
        <button onClick={() => setShowFilters(!showFilters)} style={styles.filterToggle}>
          {showFilters ? 'Hide Filters' : 'More Filters'}
        </button>
        {hasActiveFilters && <button onClick={clearFilters} style={styles.clearButton}>Clear All</button>}
      </div>

      {showFilters && (
        <div style={styles.advancedFilters}>
          <div style={styles.filterRow}>
            <label style={styles.filterLabel}>Year:</label>
            <input type="number" placeholder="From" value={yearFrom}
              onChange={(e) => setYearFrom(e.target.value)} style={styles.filterInput} min="1900" max="2030" />
            <span>to</span>
            <input type="number" placeholder="To" value={yearTo}
              onChange={(e) => setYearTo(e.target.value)} style={styles.filterInput} min="1900" max="2030" />
          </div>
          <div style={styles.filterRow}>
            <label style={styles.filterLabel}>Duration (min):</label>
            <input type="number" placeholder="From" value={durationFrom}
              onChange={(e) => setDurationFrom(e.target.value)} style={styles.filterInput} min="1" max="600" />
            <span>to</span>
            <input type="number" placeholder="To" value={durationTo}
              onChange={(e) => setDurationTo(e.target.value)} style={styles.filterInput} min="1" max="600" />
          </div>
          <div style={styles.filterRow}>
            <label style={styles.filterLabel}>Sort by:</label>
            <select value={sortBy} onChange={(e) => setSortBy(e.target.value as any)} style={styles.filterSelect}>
              <option value="created_at">Newest</option>
              <option value="title">Title</option>
              <option value="year">Year</option>
              <option value="rating">Rating</option>
            </select>
            <select value={sortOrder} onChange={(e) => setSortOrder(e.target.value as any)} style={styles.filterSelect}>
              <option value="desc">Descending</option>
              <option value="asc">Ascending</option>
            </select>
          </div>
        </div>
      )}

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
              {movie.poster_path ? (
                <img
                  src={`http://localhost:8000${movie.poster_path}`}
                  alt={movie.title}
                  style={styles.posterImage}
                />
              ) : (
                <div style={styles.posterPlaceholder}>🎬</div>
              )}
              <div style={styles.cardContent}>
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
                <div style={styles.cardMeta}>
                  {movie.category && <span style={styles.cardCategory}>{movie.category}</span>}
                  {movie.release_year && <span style={styles.cardYear}>{movie.release_year}</span>}
                  {movie.duration_minutes && <span style={styles.cardDuration}>{movie.duration_minutes} min</span>}
                </div>
                <p style={styles.cardDescription}>{movie.description || 'No description'}</p>
              </div>
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
  filterSection: { display: 'flex', gap: '1rem', marginBottom: '1.5rem', flexWrap: 'wrap', alignItems: 'center' },
  searchInput: { flex: 1, minWidth: '200px', padding: '0.75rem', border: '1px solid #ddd', borderRadius: '4px', fontSize: '1rem' },
  categorySelect: { padding: '0.75rem', border: '1px solid #ddd', borderRadius: '4px', fontSize: '1rem', minWidth: '150px' },
  filterToggle: { padding: '0.75rem 1rem', background: '#1976d2', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  clearButton: { padding: '0.75rem 1rem', background: '#e0e0e0', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  advancedFilters: { background: '#f5f5f5', padding: '1rem', borderRadius: '4px', marginBottom: '1.5rem' },
  filterRow: { display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' },
  filterLabel: { minWidth: '100px', fontWeight: 500 },
  filterInput: { padding: '0.5rem', border: '1px solid #ddd', borderRadius: '4px', width: '100px' },
  filterSelect: { padding: '0.5rem', border: '1px solid #ddd', borderRadius: '4px' },
  error: { padding: '1rem', background: '#fee', color: '#c00', borderRadius: '4px', marginBottom: '1rem' },
  resultsCount: { color: '#666', marginBottom: '1rem' },
  loading: { textAlign: 'center', padding: '2rem', color: '#666' },
  empty: { textAlign: 'center', color: '#666', padding: '2rem' },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '1.5rem' },
  card: { background: 'white', borderRadius: '8px', overflow: 'hidden', boxShadow: '0 2px 8px rgba(0,0,0,0.1)', textDecoration: 'none', color: 'inherit' },
  posterImage: { width: '100%', height: '180px', objectFit: 'cover' },
  posterPlaceholder: { width: '100%', height: '180px', background: '#e0e0e0', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '3rem' },
  cardContent: { padding: '1rem' },
  cardHeader: { display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '0.5rem' },
  cardTitle: { margin: 0, fontSize: '1.25rem', flex: 1 },
  favoriteButton: { background: 'none', border: 'none', fontSize: '1.25rem', cursor: 'pointer', padding: '0.25rem' },
  cardMeta: { display: 'flex', gap: '0.5rem', marginBottom: '0.5rem', flexWrap: 'wrap' },
  cardCategory: { display: 'inline-block', padding: '0.25rem 0.5rem', background: '#e3f2fd', color: '#1976d2', borderRadius: '4px', fontSize: '0.75rem' },
  cardYear: { color: '#666', fontSize: '0.875rem' },
  cardDuration: { color: '#666', fontSize: '0.875rem' },
  cardDescription: { margin: 0, color: '#666', fontSize: '0.875rem', lineHeight: 1.5 },
};
