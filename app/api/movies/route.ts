import { NextRequest, NextResponse } from 'next/server';
import { loadMovies, searchMovies, getMoviesByGenre, getAllGenres } from '@/lib/movies';

export async function GET(req: NextRequest) {
  try {
    // Load movies on first request
    const movies = await loadMovies();
    
    if (!movies.length) {
      return NextResponse.json({ error: 'No movies found' }, { status: 500 });
    }

    const searchParams = req.nextUrl.searchParams;
    const q = searchParams.get('q')?.trim();
    const genre = searchParams.get('genre')?.trim();

    if (q) {
      const results = searchMovies(q);
      return NextResponse.json({ movies: results, query: q });
    }

    if (genre) {
      const results = getMoviesByGenre(genre);
      return NextResponse.json({ movies: results, genre });
    }

    const genres = getAllGenres();
    return NextResponse.json({ genres, total: movies.length });
  } catch (error) {
    console.error('[v0] API Error:', error);
    return NextResponse.json({ error: 'Failed to fetch movies' }, { status: 500 });
  }
}
