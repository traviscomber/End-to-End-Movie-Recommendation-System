'use client';

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import MovieCard from '@/components/MovieCard';
import MovieModal from '@/components/MovieModal';

interface Movie {
  movie_title: string;
  imdb_score: number;
  director_name: string;
  genres: string;
  actor_1_name?: string;
}

export default function BrowsePage() {
  const searchParams = useSearchParams();
  const genre = searchParams.get('genre');
  const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedMovie, setSelectedMovie] = useState<Movie | null>(null);

  useEffect(() => {
    if (!genre) return;
    
    async function loadMovies() {
      try {
        setLoading(true);
        const res = await fetch(`/api/movies?genre=${encodeURIComponent(genre)}`);
        const data = await res.json();
        setMovies(data.movies || []);
      } catch (error) {
        console.error('[v0] Error loading movies:', error);
      } finally {
        setLoading(false);
      }
    }

    loadMovies();
  }, [genre]);

  return (
    <div className="min-h-screen bg-dark">
      {/* Header */}
      <header className="border-b border-gray-700 sticky top-0 z-40 bg-dark/95 backdrop-blur">
        <div className="container py-6">
          <a href="/" className="text-primary font-semibold hover:underline mb-4 inline-block">
            ← Back to Home
          </a>
          <h1 className="text-3xl font-bold">{genre}</h1>
          <p className="text-gray-400 mt-2">{movies.length} movies found</p>
        </div>
      </header>

      {/* Content */}
      <main className="container py-12">
        {loading ? (
          <div className="text-center py-20">
            <p className="text-gray-400">Loading movies...</p>
          </div>
        ) : movies.length === 0 ? (
          <div className="text-center py-20">
            <p className="text-gray-400">No movies found in this genre.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
            {movies.map((movie) => (
              <MovieCard
                key={movie.movie_title}
                movie={movie}
                onClick={() => setSelectedMovie(movie)}
              />
            ))}
          </div>
        )}
      </main>

      {/* Movie Modal */}
      {selectedMovie && (
        <MovieModal
          movie={selectedMovie}
          onClose={() => setSelectedMovie(null)}
        />
      )}
    </div>
  );
}
