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
    .then(response => response.json())
    .then(data => {
      console.log('[v0] Categories loaded:', data.categories.length);
      if (data.categories && data.categories.length > 0) {
        displayCategories(data.categories);
      } else {
        categoriesContainer.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">No categories available</p>';
      }
    })
    .catch(error => {
      console.error('[v0] Error loading categories:', error);
      categoriesContainer.innerHTML = '<p style="text-align: center; color: var(--error);">Error loading categories. Please try again.</p>';
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
    'Thriller': '⚡',
    'War': '🎖️',
    'Western': '🤠',
    'Romance': '💕'
  };
  
  for (const key in iconMap) {
    if (category.toLowerCase().includes(key.toLowerCase())) {
      return iconMap[key];
    }
  }
  return '🎬';
}

// Load movies by selected genre
function loadMoviesByGenre(genre) {
  console.log('[v0] Loading movies for genre:', genre);
  const moviesContainer = document.getElementById('genre-movies-container');
  const genreTitle = document.getElementById('genre-title');
  
  // Show loading state
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
    .then(response => response.json())
    .then(data => {
      console.log('[v0] Trending movies loaded:', data.trending.length);
      if (data.trending && data.trending.length > 0) {
        displayTrendingMovies(data.trending);
      }
    })
    .catch(error => console.error('[v0] Error loading trending:', error));
}

// Display trending movies carousel
function displayTrendingMovies(movies) {
  const trendingContainer = document.getElementById('trending-container');
  
  let html = '<div class="trending-carousel">';
  movies.slice(0, 8).forEach((movie, index) => {
    html += `
      <div class="trending-card">
        <div style="background: linear-gradient(135deg, var(--primary), rgba(229, 9, 20, 0.5)); padding: 2rem; border-radius: 1rem; text-align: center; height: 100%;">
          <div style="font-size: 2rem; margin-bottom: 1rem;">🏆</div>
          <h6 style="color: var(--text-primary); margin-bottom: 0.5rem; font-weight: 700;">#${index + 1}</h6>
          <h5 style="color: white; margin-bottom: 0.5rem;">${movie.movie_title}</h5>
          <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Rating: ${movie.imdb_score}/10</p>
        </div>
      </div>
    `;
  });
  html += '</div>';
  
  trendingContainer.innerHTML = html;
  console.log('[v0] Trending movies displayed');
}

// Navigate to movie search
function searchMovieFromGenre(movieTitle) {
  window.location.href = '/?search=' + encodeURIComponent(movieTitle);
}
