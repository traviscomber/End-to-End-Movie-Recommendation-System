// Favorites Management System
class FavoritesManager {
  constructor() {
    this.storageKey = 'movieRecommendations_favorites';
    this.favorites = this.loadFavorites();
  }

  loadFavorites() {
    try {
      const data = localStorage.getItem(this.storageKey);
      return data ? JSON.parse(data) : [];
    } catch (e) {
      console.error('Error loading favorites:', e);
      return [];
    }
  }

  saveFavorites() {
    try {
      localStorage.setItem(this.storageKey, JSON.stringify(this.favorites));
    } catch (e) {
      console.error('Error saving favorites:', e);
    }
  }

  addFavorite(movie) {
    if (!this.isFavorite(movie.title)) {
      this.favorites.push({
        title: movie.title,
        poster: movie.poster,
        rating: movie.rating,
        timestamp: new Date().toISOString()
      });
      this.saveFavorites();
      return true;
    }
    return false;
  }

  removeFavorite(title) {
    this.favorites = this.favorites.filter(fav => fav.title !== title);
    this.saveFavorites();
    return true;
  }

  isFavorite(title) {
    return this.favorites.some(fav => fav.title === title);
  }

  getFavorites() {
    return this.favorites;
  }

  clearAllFavorites() {
    this.favorites = [];
    this.saveFavorites();
  }
}

// Initialize favorites manager
const favoritesManager = new FavoritesManager();

// Add favorite button handler
function toggleFavorite(movieTitle, movieData) {
  const button = document.getElementById('favorite-btn');
  if (!button) return;

  if (favoritesManager.isFavorite(movieTitle)) {
    favoritesManager.removeFavorite(movieTitle);
    button.classList.remove('active');
    button.innerHTML = '☆ Add to Favorites';
    showNotification('Removed from favorites');
  } else {
    favoritesManager.addFavorite(movieData);
    button.classList.add('active');
    button.innerHTML = '★ Added to Favorites';
    showNotification('Added to favorites');
  }
}

// Display favorites
function displayFavorites() {
  const favorites = favoritesManager.getFavorites();
  const container = document.getElementById('favorites-container');
  
  if (!container) return;

  if (favorites.length === 0) {
    container.innerHTML = '<p class="text-center" style="color: var(--text-secondary); padding: var(--spacing-xl);">No favorites yet</p>';
    return;
  }

  let html = '<div class="movie-content">';
  favorites.forEach(movie => {
    html += `
      <div class="card" style="width: 15rem;">
        <div class="imghvr">
          <img class="card-img-top" height="360" width="240" alt="${movie.title} - poster" src="${movie.poster}">
          <figcaption class="fig">
            <button class="card-btn btn btn-danger" onclick="removeFavoriteCard('${movie.title}')"> Remove </button>
          </figcaption>
        </div>
        <div class="card-body">
          <h5 class="card-title">${movie.title}</h5>
          <h6>Rating: ${movie.rating}/10</h6>
        </div>
      </div>
    `;
  });
  html += '</div>';
  container.innerHTML = html;
}

function removeFavoriteCard(title) {
  favoritesManager.removeFavorite(title);
  displayFavorites();
  showNotification('Removed from favorites');
}

// Notification system
function showNotification(message) {
  const notification = document.createElement('div');
  notification.className = 'notification';
  notification.textContent = message;
  notification.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: var(--primary);
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 0.5rem;
    z-index: 1000;
    animation: slideIn 0.3s ease-in-out;
  `;
  
  document.body.appendChild(notification);
  setTimeout(() => {
    notification.style.animation = 'slideOut 0.3s ease-in-out';
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}

// Watch history
class WatchHistory {
  constructor() {
    this.storageKey = 'movieRecommendations_history';
    this.history = this.loadHistory();
  }

  loadHistory() {
    try {
      const data = localStorage.getItem(this.storageKey);
      return data ? JSON.parse(data) : [];
    } catch (e) {
      console.error('Error loading history:', e);
      return [];
    }
  }

  saveHistory() {
    try {
      localStorage.setItem(this.storageKey, JSON.stringify(this.history.slice(0, 20)));
    } catch (e) {
      console.error('Error saving history:', e);
    }
  }

  addToHistory(movieTitle) {
    // Remove if already exists
    this.history = this.history.filter(h => h !== movieTitle);
    // Add to beginning
    this.history.unshift(movieTitle);
    // Keep only last 20
    this.history = this.history.slice(0, 20);
    this.saveHistory();
  }

  getHistory() {
    return this.history;
  }

  clearHistory() {
    this.history = [];
    this.saveHistory();
  }
}

const watchHistory = new WatchHistory();

// CSS animations
const style = document.createElement('style');
style.textContent = `
  @keyframes slideIn {
    from {
      transform: translateX(400px);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }
  
  @keyframes slideOut {
    from {
      transform: translateX(0);
      opacity: 1;
    }
    to {
      transform: translateX(400px);
      opacity: 0;
    }
  }
`;
document.head.appendChild(style);
