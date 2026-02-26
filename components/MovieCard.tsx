interface Movie {
  movie_title: string;
  imdb_score: number;
  director_name: string;
  genres: string;
}

interface MovieCardProps {
  movie: Movie;
  onClick: () => void;
}

export default function MovieCard({ movie, onClick }: MovieCardProps) {
  return (
    <button
      onClick={onClick}
      className="group flex flex-col h-full bg-dark-secondary rounded-lg overflow-hidden hover:border-primary border border-gray-700 transition"
    >
      {/* Poster Placeholder */}
      <div className="w-full aspect-video bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center text-4xl group-hover:from-primary/30 group-hover:to-primary/10 transition">
        🎬
      </div>

      {/* Details */}
      <div className="flex-1 p-4 flex flex-col">
        <h3 className="font-semibold text-sm line-clamp-2 group-hover:text-primary transition">
          {movie.movie_title}
        </h3>
        
        <p className="text-xs text-gray-400 mt-2 line-clamp-1">
          {movie.director_name}
        </p>

        <div className="mt-auto pt-3 border-t border-gray-600 flex items-center justify-between">
          <span className="text-xs text-gray-400">{movie.genres.split(',')[0]}</span>
          <span className="font-bold text-primary">★ {movie.imdb_score.toFixed(1)}</span>
        </div>
      </div>
    </button>
  );
}
