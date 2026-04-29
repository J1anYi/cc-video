import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getFavorites, removeFavorite } from '../api/favorites';
import type { Favorite } from '../api/types';

export default function Favorites() {
  const [favorites, setFavorites] = useState<Favorite[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    loadFavorites();
  }, []);

  const loadFavorites = async () => {
    try {
      setLoading(true);
      const data = await getFavorites();
      setFavorites(data);
      setError(null);
    } catch (err) {
      setError('Failed to load favorites');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRemove = async (movieId: number, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await removeFavorite(movieId);
      setFavorites(favorites.filter(f => f.movie_id !== movieId));
    } catch (err) {
      console.error('Failed to remove favorite:', err);
    }
  };

  const handlePlay = (movieId: number) => {
    navigate(`/movies/${movieId}`);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[50vh]">
        <div className="text-gray-400">Loading favorites...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-[50vh]">
        <div className="text-red-500">{error}</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-white mb-6">My Favorites</h1>
      
      {favorites.length === 0 ? (
        <div className="text-center text-gray-400 py-12">
          No favorites yet. Browse movies and click the heart icon to add them here.
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {favorites.map((favorite) => (
            <div
              key={favorite.id}
              onClick={() => favorite.movie && handlePlay(favorite.movie_id)}
              className="bg-gray-800 rounded-lg overflow-hidden cursor-pointer hover:ring-2 hover:ring-blue-500 transition-all"
            >
              <div className="aspect-video bg-gray-700 flex items-center justify-center">
                <span className="text-4xl">🎬</span>
              </div>
              <div className="p-4">
                <h3 className="text-white font-medium truncate">
                  {favorite.movie?.title || 'Unknown Movie'}
                </h3>
                <p className="text-gray-400 text-sm mt-1">
                  Added {new Date(favorite.created_at).toLocaleDateString()}
                </p>
                <div className="flex justify-between items-center mt-3">
                  <button
                    onClick={(e) => handleRemove(favorite.movie_id, e)}
                    className="text-red-400 hover:text-red-300 text-sm flex items-center gap-1"
                  >
                    ❤️ Remove
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handlePlay(favorite.movie_id);
                    }}
                    className="text-blue-400 hover:text-blue-300 text-sm"
                  >
                    ▶ Play
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
