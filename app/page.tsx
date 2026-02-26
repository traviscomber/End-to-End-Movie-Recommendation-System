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
  const [genres, setGenres] = useState<string[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
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
    <div className="min-h-screen bg-dark">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-dark via-dark to-purple-900/20 pt-20 pb-32">
        <div className="container mx-auto px-4">
          {/* Hero Content */}
          <div className="text-center mb-12">
            <h1 className="text-5xl md:text-6xl font-bold mb-4">
              Movie <span className="text-primary">Finder</span>
            </h1>
            <p className="text-xl text-gray-400 mb-8">
              Discover great films and watch them on Tubi
            </p>

            {/* Search Bar */}
            <form onSubmit={handleSearch} className="max-w-2xl mx-auto mb-8">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search by movie title, director, or actor..."
                  className="flex-1 px-6 py-4 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-primary focus:outline-none"
                />
                <button
                  type="submit"
                  className="px-8 py-4 bg-primary hover:bg-red-600 rounded-lg font-semibold transition"
                >
                  Search
                </button>
              </div>
            </form>

            {/* Action Button */}
            <button
              onClick={() => router.push('/browse')}
              className="px-8 py-3 bg-purple-600 hover:bg-purple-700 rounded-lg font-semibold transition inline-block"
            >
              Browse by Genre
            </button>
          </div>

          {/* Featured Badge */}
          <div className="max-w-4xl mx-auto bg-purple-900/40 border border-purple-500/50 rounded-xl p-6 text-center">
            <p className="text-purple-300">
              <span className="font-semibold">Powered by Tubi</span> - Stream hundreds of free movies with ads
            </p>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-dark-secondary/50">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">How it works</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            {/* Feature 1 */}
            <div className="text-center">
              <div className="text-4xl mb-4">🔍</div>
              <h3 className="text-xl font-bold mb-2">Search & Browse</h3>
              <p className="text-gray-400">
                Find movies by title, genre, director, or actor with ease
              </p>
            </div>

            {/* Feature 2 */}
            <div className="text-center">
              <div className="text-4xl mb-4">⭐</div>
              <h3 className="text-xl font-bold mb-2">Ratings & Details</h3>
              <p className="text-gray-400">
                See IMDb ratings, cast, genres, and detailed information
              </p>
            </div>

            {/* Feature 3 */}
            <div className="text-center">
              <div className="text-4xl mb-4">🎬</div>
              <h3 className="text-xl font-bold mb-2">Watch on Tubi</h3>
              <p className="text-gray-400">
                Stream directly to Tubi with one click - free with ads
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Genres Section */}
      <section className="container py-16">
        <h2 className="text-3xl font-bold mb-8">Browse by Genre</h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          {genres.slice(0, 20).map((genre) => (
            <button
              key={genre}
              onClick={() => router.push(`/browse?genre=${encodeURIComponent(genre)}`)}
              className="p-4 bg-dark-secondary hover:bg-primary/20 border border-gray-700 hover:border-primary rounded-lg font-semibold transition text-sm"
            >
              {genre}
            </button>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-700 mt-20">
        <div className="container py-8 text-center text-gray-500">
          <p>Movie Recommendation System • Powered by Tubi • All Rights Reserved</p>
        </div>
      </footer>
    </div>
  );
}
