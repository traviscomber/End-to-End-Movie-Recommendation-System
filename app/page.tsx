'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface Movie {
  movie_title: string;
  imdb_score: number;
  director_name: string;
  genres: string;
}

export default function Home() {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [genres, setGenres] = useState<string[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedMovie, setSelectedMovie] = useState<Movie | null>(null);
  const router = useRouter();

  useEffect(() => {
    loadGenres();
  }, []);

  async function loadGenres() {
    try {
      const res = await fetch('/api/movies');
      const data = await res.json();
      if (data.genres) setGenres(data.genres);
    } catch (error) {
      console.error('[v0] Error loading genres:', error);
    }
  }

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    if (searchQuery.trim()) {
      router.push(`/search?q=${encodeURIComponent(searchQuery)}`);
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-dark to-dark-secondary">
      {/* Header */}
      <header className="border-b border-gray-700">
        <div className="container py-6">
          <h1 className="text-4xl font-bold text-primary">🎬 Movie Finder</h1>
          <p className="text-gray-400 mt-2">Discover your next favorite film</p>
        </div>
      </header>

      {/* Search Section */}
      <section className="container py-12">
        <form onSubmit={handleSearch} className="max-w-2xl mx-auto">
          <div className="flex gap-3">
            <input
              type="text"
              placeholder="Search movies, directors, actors..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="flex-1 px-6 py-3 bg-dark-secondary border border-gray-600 rounded-lg focus:border-primary focus:outline-none"
            />
            <button
              type="submit"
              className="px-8 py-3 bg-primary hover:bg-primary-dark rounded-lg font-semibold"
            >
              Search
            </button>
          </div>
        </form>
      </section>

      {/* Genres */}
      <section className="container py-12">
        <h2 className="text-2xl font-bold mb-8">Browse by Genre</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
          {genres.map((genre) => (
            <button
              key={genre}
              onClick={() => router.push(`/browse?genre=${encodeURIComponent(genre)}`)}
              className="p-4 bg-dark-secondary hover:bg-primary/20 border border-gray-700 hover:border-primary rounded-lg font-semibold transition"
            >
              {genre}
            </button>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-700 mt-20">
        <div className="container py-8 text-center text-gray-500">
          <p>Movie Recommendation System • All Rights Reserved</p>
        </div>
      </footer>
    </div>
  );
}
