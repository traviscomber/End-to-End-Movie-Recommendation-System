import { useEffect } from 'react';

interface Movie {
  movie_title: string;
  imdb_score: number;
  director_name: string;
  genres: string;
  actor_1_name?: string;
  actor_2_name?: string;
  actor_3_name?: string;
}

interface MovieModalProps {
  movie: Movie;
  onClose: () => void;
}

export default function MovieModal({ movie, onClose }: MovieModalProps) {
  useEffect(() => {
    function handleEscape(e: KeyboardEvent) {
      if (e.key === 'Escape') onClose();
    }
    window.addEventListener('keydown', handleEscape);
    return () => window.removeEventListener('keydown', handleEscape);
  }, [onClose]);

  const cast = [movie.actor_1_name, movie.actor_2_name, movie.actor_3_name]
    .filter(Boolean)
    .join(', ') || 'N/A';

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div
          className="bg-dark-secondary border border-primary/30 rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header with Close */}
          <div className="sticky top-0 bg-dark-secondary border-b border-gray-700 p-6 flex justify-between items-start">
            <div>
              <h2 className="text-2xl font-bold">{movie.movie_title}</h2>
              <p className="text-gray-400 mt-1">{movie.genres}</p>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white text-2xl"
            >
              ✕
            </button>
          </div>

          {/* Content */}
          <div className="p-6 space-y-6">
            {/* Poster & Rating */}
            <div className="flex gap-6">
              <div className="w-40 aspect-video bg-gradient-to-br from-primary/20 to-primary/5 rounded-lg flex items-center justify-center text-5xl flex-shrink-0">
                🎬
              </div>

              <div className="flex-1">
                <div className="bg-primary/10 border border-primary/30 rounded-lg p-4 mb-4">
                  <p className="text-xs text-gray-400 uppercase tracking-wider">IMDb Rating</p>
                  <p className="text-4xl font-bold text-primary">★ {movie.imdb_score.toFixed(1)}/10</p>
                </div>
              </div>
            </div>

            {/* Details Grid */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-xs text-gray-400 uppercase tracking-wider mb-2">Director</p>
                <p className="font-semibold">{movie.director_name}</p>
              </div>
              <div>
                <p className="text-xs text-gray-400 uppercase tracking-wider mb-2">Genres</p>
                <p className="font-semibold">{movie.genres}</p>
              </div>
            </div>

            {/* Cast */}
            <div>
              <p className="text-xs text-gray-400 uppercase tracking-wider mb-2">Cast</p>
              <p className="font-semibold">{cast}</p>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3 pt-4">
              <button
                onClick={onClose}
                className="flex-1 px-6 py-3 bg-primary hover:bg-primary-dark rounded-lg font-semibold"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
