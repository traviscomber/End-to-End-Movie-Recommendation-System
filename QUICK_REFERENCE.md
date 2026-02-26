# Movie Finder - Quick Reference Card

## One-Minute Overview

**What**: AI-powered movie recommendation system with modern UI
**Why**: Find movies you love based on content similarity + trending + genres
**How**: Search → Get recommendations → Save favorites → Share with friends

## Getting Started (90 seconds)

```bash
# 1. Install
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. Run
python app.py

# 3. Open
http://localhost:5000
```

## Main URLs

| URL | Purpose |
|-----|---------|
| `/` | Search & home page |
| `/recommend` | Movie details & recommendations |
| `/categories` | Browse by genre |
| `/api/categories` | Get all genres (JSON) |
| `/api/movies-by-genre/Action` | Movies by genre (JSON) |
| `/api/trending` | Top rated movies (JSON) |

## Common Tasks

### Search for a Movie
1. Type in search box
2. Select from autocomplete (or type full name)
3. Click Search button
4. See recommendations

### Save Favorite
While viewing movie:
1. Click "♥ Add to Favorites"
2. Button changes to "★ Added"
3. Saved on device (survives refresh)

### Browse by Genre
1. Click "Browse Genres" 
2. Choose category (e.g., "Action ⚔️")
3. View all movies in category

### Share Movie
While viewing movie:
1. Click "Share" button
2. Choose platform or copy to clipboard
3. Share with friends

### View Favorites
1. Click "My Favorites" button
2. See all saved movies
3. Click to view details again

## Environment Setup

```bash
# Create .env file
cp .env.example .env

# Add API key for AI features (optional)
OPENAI_API_KEY=sk-your-key-here

# Run with env
python app.py
```

## API Quick Reference

### Get Recommendations
```bash
POST /similarity
Content-Type: application/json
{
  "movie_title": "Inception"
}
```

### Get Movie Summary (requires OpenAI)
```bash
POST /api/movie-summary
{
  "title": "Inception",
  "overview": "A skilled thief...",
  "genres": "Action, Sci-Fi"
}
```

### Get All Genres
```bash
GET /api/categories
```

### Get Movies by Genre
```bash
GET /api/movies-by-genre/Action
```

## File Locations

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application |
| `openai_helper.py` | AI integration |
| `error_handler.py` | Error handling |
| `templates/home.html` | Search page |
| `templates/recommend.html` | Movie details |
| `templates/categories.html` | Genre browsing |
| `static/style.css` | Styling |
| `static/recommend.js` | Recommendation logic |
| `static/categories.js` | Genre logic |
| `static/favorites.js` | Favorites system |
| `static/utils.js` | Utility functions |

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Enter | Search |
| Esc | Close modal |
| ↑ ↓ | Navigate autocomplete |
| Ctrl+C | Copy (after share) |

## Useful Endpoints for Development

```bash
# Get categories
curl http://localhost:5000/api/categories

# Get trending movies  
curl http://localhost:5000/api/trending

# Get Action movies
curl "http://localhost:5000/api/movies-by-genre/Action"

# Search recommendations
curl -X POST http://localhost:5000/similarity \
  -H "Content-Type: application/json" \
  -d '{"movie_title": "Inception"}'
```

## Environment Variables

```bash
FLASK_ENV              # development or production
FLASK_DEBUG            # True or False
LOG_LEVEL              # DEBUG, INFO, WARNING, ERROR
OPENAI_API_KEY         # sk-... (optional)
```

## Docker Commands

```bash
# Build image
docker build -t movie-finder .

# Run container
docker run -p 5000:5000 movie-finder

# Dev environment
docker-compose up

# Stop services
docker-compose down
```

## Documentation Quick Links

- **USER_GUIDE.md** - Features and how to use
- **SETUP_GUIDE.md** - Installation and deployment
- **ENHANCEMENT_SUMMARY.md** - What's new
- **DEVELOPMENT.md** - Architecture details
- **DOCS_INDEX.md** - All documentation

## Troubleshooting Quick Tips

| Problem | Solution |
|---------|----------|
| Movie not found | Check spelling, try autocomplete |
| Recommendations not loading | Refresh page, check connection |
| Favorites not saving | Enable cookies, try different browser |
| AI not working | Add OPENAI_API_KEY to .env |
| Port already in use | Kill process: `lsof -ti:5000` \| `xargs kill -9` |
| Import errors | Run: `pip install -r requirements.txt` |

## Performance Tips

- Use Chrome DevTools Network tab to monitor API calls
- Check logs in `logs/app.log` for issues
- Clear browser cache if UI looks wrong
- Restart app after changing .env

## Common Code Patterns

### Add to favorites (JavaScript)
```javascript
toggleFavorite('Movie Title', {
  title: 'Movie Title',
  poster: 'url',
  rating: 8.5
});
```

### Show notification
```javascript
showNotification('Message', 'success'); // or 'error', 'warning'
```

### Show loading spinner
```javascript
showLoadingSpinner('Finding movies...');
hideLoadingSpinner();
```

## Key Features Matrix

| Feature | Status | Where |
|---------|--------|-------|
| Search | ✅ | Home page |
| Recommendations | ✅ | Movie details |
| Genres | ✅ | Categories page |
| Favorites | ✅ | Everywhere |
| History | ✅ | History button |
| Share | ✅ | Movie details |
| AI Summaries | ✅ Optional | Movie details |
| Trending | ✅ | Categories page |
| Reviews | ✅ | Movie details |
| Cast Info | ✅ | Movie details |

## Design Tokens (Colors)

```css
--primary: #e50914              /* Netflix red */
--background: #0f0f0f           /* Dark bg */
--text-primary: #ffffff         /* White text */
--text-secondary: #a0a0a0       /* Gray text */
--success: #22c55e              /* Green */
--error: #ef4444                /* Red */
--warning: #f59e0b              /* Amber */
```

## Testing Checklist

- [ ] Search for movie
- [ ] View recommendations
- [ ] Add to favorites
- [ ] View favorites
- [ ] Check history
- [ ] Share movie
- [ ] Browse genres
- [ ] View cast
- [ ] Check reviews
- [ ] Mobile view

## Deployment Checklist

- [ ] Set FLASK_ENV=production
- [ ] Configure OPENAI_API_KEY (optional)
- [ ] Test locally
- [ ] Build Docker image
- [ ] Deploy to server
- [ ] Configure domain
- [ ] Set up SSL
- [ ] Monitor logs
- [ ] Test all features
- [ ] Set up backups

## Support Resources

- **Issues**: Check existing GitHub issues
- **Docs**: Read DOCS_INDEX.md for navigation
- **Setup**: Follow SETUP_GUIDE.md
- **Features**: See USER_GUIDE.md
- **Dev**: Check DEVELOPMENT.md

---

**Quick Start**: `python app.py` then visit `http://localhost:5000`

**Full Setup**: See `SETUP_GUIDE.md`

**Features**: See `USER_GUIDE.md`

**Documentation**: See `DOCS_INDEX.md`
