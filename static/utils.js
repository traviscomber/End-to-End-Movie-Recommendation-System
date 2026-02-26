// Notification system
function showNotification(message, type = 'info', duration = 3000) {
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.innerHTML = `
    <div style="display: flex; align-items: center; gap: 1rem; padding: 1rem 1.5rem; background: rgba(0, 0, 0, 0.9); border-left: 4px solid ${getColorForType(type)}; border-radius: 0.5rem; backdrop-filter: blur(10px); color: white; font-weight: 500;">
      ${getIconForType(type)}
      <span>${message}</span>
    </div>
  `;
  
  const container = document.body;
  container.appendChild(notification);
  
  notification.style.position = 'fixed';
  notification.style.bottom = '2rem';
  notification.style.right = '2rem';
  notification.style.zIndex = '9999';
  notification.style.animation = 'fadeIn 0.3s ease-in-out';
  
  setTimeout(() => {
    notification.style.animation = 'fadeOut 0.3s ease-in-out';
    setTimeout(() => notification.remove(), 300);
  }, duration);
}

function getColorForType(type) {
  const colors = {
    'success': '#31a24c',
    'error': '#ef4444',
    'warning': '#f59e0b',
    'info': '#e50914'
  };
  return colors[type] || colors.info;
}

function getIconForType(type) {
  const icons = {
    'success': '<i class="fas fa-check-circle" style="color: #31a24c; font-size: 1.25rem;"></i>',
    'error': '<i class="fas fa-exclamation-circle" style="color: #ef4444; font-size: 1.25rem;"></i>',
    'warning': '<i class="fas fa-exclamation-triangle" style="color: #f59e0b; font-size: 1.25rem;"></i>',
    'info': '<i class="fas fa-info-circle" style="color: #e50914; font-size: 1.25rem;"></i>'
  };
  return icons[type] || icons.info;
}

// Loading spinner
function showLoadingSpinner(text = 'Loading...') {
  const spinner = document.createElement('div');
  spinner.id = 'global-spinner';
  spinner.innerHTML = `
    <div style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0, 0, 0, 0.8); backdrop-filter: blur(5px); display: flex; align-items: center; justify-content: center; z-index: 10000;">
      <div style="text-align: center;">
        <div style="width: 50px; height: 50px; border: 4px solid rgba(229, 9, 20, 0.3); border-top-color: #e50914; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 1rem;"></div>
        <p style="color: #b3b3b3; font-size: 1rem;">${text}</p>
      </div>
    </div>
  `;
  
  // Add spin animation if not already present
  if (!document.querySelector('#spinner-styles')) {
    const style = document.createElement('style');
    style.id = 'spinner-styles';
    style.textContent = `
      @keyframes spin {
        to { transform: rotate(360deg); }
      }
    `;
    document.head.appendChild(style);
  }
  
  document.body.appendChild(spinner);
}

function hideLoadingSpinner() {
  const spinner = document.getElementById('global-spinner');
  if (spinner) {
    spinner.style.animation = 'fadeOut 0.3s ease-in-out';
    setTimeout(() => spinner.remove(), 300);
  }
}

// Debounce function for input events
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Throttle function
function throttle(func, limit) {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// Lazy load images
function lazyLoadImages() {
  if ('IntersectionObserver' in window) {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
          observer.unobserve(img);
        }
      });
    });
    images.forEach(img => imageObserver.observe(img));
  }
}

// Copy to clipboard with feedback
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    showNotification('Copied to clipboard!', 'success', 2000);
  }).catch(err => {
    showNotification('Failed to copy', 'error', 2000);
    console.error('Failed to copy:', err);
  });
}

// Format rating scale
function formatRating(rating) {
  return (Math.round(rating * 10) / 10).toFixed(1);
}

// Get dominant color from image (for accent colors)
function getDominantColor(imageUrl, callback) {
  const img = new Image();
  img.crossOrigin = 'Anonymous';
  img.onload = function() {
    const canvas = document.createElement('canvas');
    canvas.width = img.width;
    canvas.height = img.height;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0);
    
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;
    
    let r = 0, g = 0, b = 0;
    for (let i = 0; i < data.length; i += 4) {
      r += data[i];
      g += data[i + 1];
      b += data[i + 2];
    }
    
    r = Math.floor(r / (data.length / 4));
    g = Math.floor(g / (data.length / 4));
    b = Math.floor(b / (data.length / 4));
    
    callback(`rgb(${r}, ${g}, ${b})`);
  };
  img.src = imageUrl;
}

// Initialize tooltips
function initializeTooltips() {
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-toggle="tooltip"]'));
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
}

// Smooth scroll to element
function smoothScrollTo(elementId) {
  const element = document.getElementById(elementId);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

// Check if device is mobile
function isMobileDevice() {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

// Get query parameter
function getQueryParam(param) {
  const params = new URLSearchParams(window.location.search);
  return params.get(param);
}

// Format date
function formatDate(dateString) {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString('en-US', options);
}

// Animate on scroll
function animateOnScroll() {
  const elements = document.querySelectorAll('[data-animate]');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.animation = `fadeIn 0.6s ease-in-out forwards`;
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });
  
  elements.forEach(el => observer.observe(el));
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  initializeTooltips();
  animateOnScroll();
  lazyLoadImages();
});
