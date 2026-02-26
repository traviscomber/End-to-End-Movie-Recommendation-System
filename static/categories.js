// Load all categories on page load
document.addEventListener('DOMContentLoaded', function() {
  loadCategories();
  loadTrendingMovies();
});

// Fetch and display all categories
function loadCategories() {
  console.log('[v0] Loading categories...');
  const categoriesContainer = document.getElementById('categories-container');
  
  if (!categoriesContainer) {
    console.error('[v0] Categories container not found');
    return;
  }

  categoriesContainer.innerHTML = '<div style="text-align: center; padding: 2rem;"><div class="spinner-border text-primary"></div></div>';

  fetch('/api/categories')
    .then(response => {
      console.log('[v0] API response status:', response.status);
      return response.json();
    })
    .then(data => {
      console.log('[v0] Categories loaded:', data);
      const categories = data.categories || [];
      
      if (categories && categories.length > 0) {
        console.log('[v0] Displaying', categories.length, 'categories');
        displayCategories(categories);
      } else {
        console.warn('[v0] No categories available, showing defaults');
        displayCategories(['Action', 'Drama', 'Comedy', 'Thriller', 'Sci-Fi', 'Horror', 'Romance', 'Adventure']);
      }
    })
    .catch(error => {
      console.error('[v0] Error loading categories:', error);
      console.log('[v0] Using fallback categories');
      displayCategories(['Action', 'Drama', 'Comedy', 'Thriller', 'Sci-Fi', 'Horror', 'Romance', 'Adventure']);
    });
}

// Display categories as grid
function displayCategories(categories) {
  const categoriesContainer = document.getElementById('categories-container');
  
  let html = '<div class="categories-grid">';
  
  categories.forEach(category => {
    const categoryIcon = getCategoryIcon(category);
    html += `
      <div class="category-card" onclick="loadMoviesByGenre('${category}')">
        <div class="category-icon">${categoryIcon}</div>
        <h5 class="category-name">${category}</h5>
        <p class="category-desc">Explore ${category} movies</p>
        <button class="btn btn-sm btn-primary" style="margin-top: auto;">View Movies</button>
      </div>
    `;
  });
  
  html += '</div>';
  categoriesContainer.innerHTML = html;
  console.log('[v0] Categories displayed');
}

// Get appropriate icon for category
function getCategoryIcon(category) {
  const iconMap = {
    'Action': '⚔️',
    'Adventure': '🗺️',
    'Animation': '🎨',
    'Comedy': '😄',
    'Crime': '🔍',
    'Documentary': '📹',
    'Drama': '🎭',
    'Family': '👨‍👩‍👧‍👦',
    'Fantasy': '✨',
    'History': '📚',
    'Horror': '👻',
    'Music': '🎵',
    'Mystery': '🕵️',
    'Romance': '💕',
    'Science Fiction': '🚀',
    'Sci-Fi': '🚀',
    'Sci Fi': '🚀',
    'Thriller': '⚡',
    'War': '🎖️',
    'Western': '🤠',
    'Tubi': '🎞️',
    'B-Movies': '🎞️',
    'Indie': '🌟',
    'Gems': '💎',
    'Cult': '👁️'
  };
  
  for (const key in iconMap) {
    if (category.toLowerCase().includes(key.toLowerCase())) {
      return iconMap[key];
    }
  }
  return '🎬';
}

// Display all categories with grouping for indie sources
function displayCategories(categories) {
  const categoriesContainer = document.getElementById('categories-container');
  
  if (!categoriesContainer) return;

  // Separate regular genres from indie/alternative sources
  const regularGenres = [];
  const alternativeSources = [];
  
  categories.forEach(cat => {
    const catLower = cat.toLowerCase();
    if (catLower.includes('tubi') || catLower.includes('indie') || 
        catLower.includes('gem') || catLower.includes('cult') || catLower.includes('b-movie')) {
      alternativeSources.push(cat);
    } else {
      regularGenres.push(cat);
    }
  });

  let html = '<div class="categories-wrapper">';
  
  // Regular genres section
  html += '<div class="category-section">';
  html += '<h4 style="color: var(--primary); margin-bottom: 1.5rem; font-weight: 700; margin-top: 0;">Popular Genres</h4>';
  html += '<div class="categories-grid">';
  
  regularGenres.forEach((genre) => {
    const icon = getCategoryIcon(genre);
    html += `
      <div class="category-card" onclick="loadMoviesByGenre('${genre}')">
        <div class="category-icon">${icon}</div>
        <h5 class="category-name">${genre}</h5>
        <p class="category-desc">Explore ${genre} movies</p>
        <button class="btn btn-sm btn-primary" style="margin-top: auto;">View Movies</button>
      </div>
    `;
  });
  
  html += '</div></div>';
  
  // Alternative sources section
  if (alternativeSources.length > 0) {
    html += '<div class="category-section" style="margin-top: 3rem;">';
    html += '<h4 style="color: #ff6b6b; margin-bottom: 1rem; font-weight: 700;">Crazy Feeds - Indie & B-Movies</h4>';
    html += '<p style="color: var(--text-secondary); margin-bottom: 1.5rem; font-size: 0.9rem;">Discover cult classics, hidden gems, and wild B-movies from Tubi and indie sources</p>';
    html += '<div class="categories-grid">';
    
    alternativeSources.forEach((source) => {
      const icon = getCategoryIcon(source);
      html += `
        <div class="category-card indie-card" onclick="loadMoviesByGenre('${source}')" style="border: 2px solid #ff6b6b;">
          <div class="category-icon" style="font-size: 2rem;">${icon}</div>
          <h5 class="category-name">${source}</h5>
          <p class="category-desc">Experimental & Unique</p>
          <div style="display: flex; gap: 0.5rem; margin-top: auto;">
            <span style="background: #ff6b6b; color: white; padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-size: 0.7rem; font-weight: 600;">NEW</span>
          </div>
        </div>
      `;
    });
    
    html += '</div></div>';
  }
  
  html += '</div>';
  categoriesContainer.innerHTML = html;
  console.log('[v0] Categories displayed with indie sources:', categories.length);
}

// Load movies by selected genre
function loadMoviesByGenre(genre) {
  console.log('[v0] Loading movies for genre:', genre);
  const moviesContainer = document.getElementById('genre-movies-container');
  const genreTitle = document.getElementById('genre-title');
  
  // Show loading state
  if (moviesContainer && genreTitle) {
    moviesContainer.innerHTML = '<div style="text-align: center; padding: 2rem;"><div class="spinner-border text-primary"></div></div>';
    genreTitle.textContent = `Loading ${genre} movies...`;
  }

  fetch(`/api/movies-by-genre/${encodeURIComponent(genre)}`)
    .then(response => response.json())
    .then(data => {
      console.log('[v0] Movies loaded for genre:', genre, data.movies.length);
      if (data.movies && data.movies.length > 0) {
        displayGenreMovies(data.movies, genre, data.source);
        if (genreTitle) genreTitle.textContent = `${genre} Movies`;
      } else {
        if (moviesContainer) {
          moviesContainer.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">No movies found for this genre.</p>';
        }
        if (genreTitle) genreTitle.textContent = `${genre} - No movies found`;
      }
    })
    .catch(error => {
      console.error('[v0] Error loading movies:', error);
      if (moviesContainer) {
        moviesContainer.innerHTML = '<p style="text-align: center; color: var(--error);">Error loading movies. Please try again.</p>';
      }
    });
}

// Display movies for a genre
function displayGenreMovies(movies, genre, source = 'Database') {
  const moviesContainer = document.getElementById('genre-movies-container');
  if (!moviesContainer) return;

  let html = '<div class="genre-movies-grid">';
  
  movies.forEach((movie, index) => {
    const movieTitle = movie.title || 'Unknown Movie';
    const rating = movie.rating || 0;
    const movieSource = movie.source || source || 'Database';
    
    // Generate emoji based on genre
    let emoji = '🎬';
    const genreLower = genre.toLowerCase();
    if (genreLower.includes('action')) emoji = '⚔️';
    else if (genreLower.includes('comedy')) emoji = '😄';
    else if (genreLower.includes('horror')) emoji = '👻';
    else if (genreLower.includes('romance')) emoji = '💕';
    else if (genreLower.includes('sci-fi')) emoji = '🚀';
    else if (genreLower.includes('drama')) emoji = '🎭';
    else if (genreLower.includes('tubi') || genreLower.includes('b-movie')) emoji = '🎞️';
    else if (genreLower.includes('indie') || genreLower.includes('gems')) emoji = '🌟';
    
    html += `
      <div class="genre-movie-card" onclick="searchMovie('${movieTitle}')">
        <div class="genre-movie-poster">${emoji}</div>
        <div class="genre-movie-info">
          <div class="genre-movie-title">${movieTitle}</div>
          <div class="genre-movie-rating">★ ${rating}/10</div>
          <div class="genre-movie-source">${movieSource}</div>
        </div>
      </div>
    `;
  });
  
  html += '</div>';
  moviesContainer.innerHTML = html;
  console.log('[v0] Genre movies displayed:', movies.length);
}

// Navigate to search a movie
function searchMovie(movieTitle) {
  console.log('[v0] Searching for movie:', movieTitle);
  window.location.href = '/?search=' + encodeURIComponent(movieTitle);
}
  moviesContainer.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 2rem;"><div class="spinner-border text-primary"></div></div>';
  genreTitle.textContent = `${genre} Movies`;
  
  // Scroll to results
  moviesContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });

  fetch(`/api/movies-by-genre/${encodeURIComponent(genre)}`)
    .then(response => response.json())
    .then(data => {
      console.log('[v0] Movies loaded for genre:', data.movies.length);
      if (data.movies && data.movies.length > 0) {
        displayMoviesByGenre(data.movies, genre);
      } else {
        moviesContainer.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: var(--text-secondary);">No movies found in this category</p>';
      }
    })
    .catch(error => {
      console.error('[v0] Error loading movies:', error);
      moviesContainer.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: var(--error);">Error loading movies. Please try again.</p>';
    });
}

// Display movies for a genre
function displayMoviesByGenre(movies, genre) {
  const moviesContainer = document.getElementById('genre-movies-container');
  
  let html = '';
  movies.forEach(movie => {
    const stars = Math.round(movie.rating / 2);
    const starHTML = '<i class="fas fa-star"></i>'.repeat(Math.min(5, stars)) + 
                     '<i class="far fa-star"></i>'.repeat(Math.max(0, 5 - stars));
    
    html += `
      <div class="movie-grid-card">
        <div class="movie-card-placeholder">
          <div style="font-size: 3rem; margin-bottom: 1rem;">${getCategoryIcon(genre)}</div>
          <h5 style="color: var(--text-primary); margin-bottom: 0.5rem;">${movie.title}</h5>
          <div style="color: var(--primary); font-size: 0.9rem;">${starHTML}</div>
          <p style="color: var(--text-secondary); font-size: 0.85rem; margin-top: 0.5rem;">${movie.rating}/10</p>
        </div>
      </div>
    `;
  });
  
  moviesContainer.innerHTML = html;
  console.log('[v0] Movies displayed for genre:', genre);
}

// Load trending movies
function loadTrendingMovies() {
  const trendingContainer = document.getElementById('trending-container');
  
  if (!trendingContainer) {
    return;
  }

  fetch('/api/trending')
    .then(response => {
      console.log('[v0] Trending API response:', response.status);
      return response.json();
    })
    .then(data => {
      console.log('[v0] Trending movies loaded:', data.trending ? data.trending.length : 0);
      if (data.trending && data.trending.length > 0) {
        displayTrendingMovies(data.trending);
      } else {
        console.log('[v0] No trending movies, hiding section');
        trendingContainer.parentElement.style.display = 'none';
      }
    })
    .catch(error => {
      console.error('[v0] Error loading trending:', error);
      trendingContainer.parentElement.style.display = 'none';
    });
}

// Display trending movies carousel
function displayTrendingMovies(movies) {
  const trendingContainer = document.getElementById('trending-container');
  
  let html = '<div class="trending-carousel">';
  movies.slice(0, 8).forEach((movie, index) => {
    const rating = movie.imdb_score || 0;
    const movieTitle = movie.movie_title || 'Unknown Movie';
    
    html += `
      <div class="trending-card">
        <div style="background: linear-gradient(135deg, var(--primary), rgba(229, 9, 20, 0.5)); padding: 2rem; border-radius: 1rem; text-align: center; height: 100%;">
          <div style="font-size: 2rem; margin-bottom: 1rem;">🏆</div>
          <h6 style="color: var(--text-primary); margin-bottom: 0.5rem; font-weight: 700;">#${index + 1}</h6>
          <h5 style="color: white; margin-bottom: 0.5rem;">${movieTitle}</h5>
          <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Rating: ${rating.toFixed(1)}/10</p>
        </div>
      </div>
    `;
  });
  html += '</div>';
  
  trendingContainer.innerHTML = html;
  console.log('[v0] Trending movies displayed:', movies.length);
}

// Navigate to movie search
function searchMovieFromGenre(movieTitle) {
  window.location.href = '/?search=' + encodeURIComponent(movieTitle);
}
