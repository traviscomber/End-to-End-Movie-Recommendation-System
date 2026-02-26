# Movie Recommendation System - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

### 3. Open in Browser
```
http://localhost:5000
```

That's it! You now have the Movie Recommendation System running.

## 📖 Basic Usage

### Searching for Movies
1. Type a movie name in the search box (e.g., "Inception")
2. Select from the dropdown suggestions
3. Click "Search" or press Enter
4. Browse movie details and recommendations

### Saving Favorites
1. View a movie's details
2. Click "★ Add to Favorites"
3. Access your favorites from the "My Favorites" button on home page

### Viewing History
1. Click "History" button on home page
2. View your recent searches
3. Click any movie to search again

### Sharing Movies
1. On any movie details page
2. Click "Share" button
3. Share via native share or copy link

## 🛠 Project Structure

```
├── app.py                 # Main application
├── error_handler.py       # Error handling
├── requirements.txt       # Dependencies
├── templates/             # HTML pages
├── static/                # CSS, JavaScript
└── Artifacts/             # ML models & data
```

## 📝 Configuration

### Environment Variables (Optional)
Create `.env` file:
```env
FLASK_ENV=development
LOG_LEVEL=INFO
```

### API Keys
The application uses embedded TMDB API keys. For custom setup, update in `static/recommend.js`.

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "File not found" errors | Ensure Artifacts folder has all 3 files |
| Slow recommendations | Dataset size issue - check main_data.csv |
| Reviews not loading | IMDB may be rate-limited - this is optional |
| Favorites not saving | Using browser storage - works in same browser |

## 📱 Features

✅ Movie search with autocomplete  
✅ Content-based recommendations  
✅ Detailed movie information  
✅ User reviews with sentiment analysis  
✅ Favorites management  
✅ Search history  
✅ Share functionality  
✅ Responsive mobile design  
✅ Error handling & logging  

## 🌐 Deployment

### Using Gunicorn (Production)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker
```bash
docker build -t movie-rec .
docker run -p 5000:5000 movie-rec
```

## 📚 Full Documentation

See `DEVELOPMENT.md` for comprehensive documentation including:
- Detailed setup instructions
- API endpoint documentation
- Configuration options
- Performance optimization
- Security considerations
- Advanced deployment

## ❓ Common Questions

**Q: Can I add more movies?**
A: Update `Artifacts/main_data.csv` with additional movies.

**Q: How do recommendations work?**
A: Uses cosine similarity on combined movie features (genre, cast, keywords).

**Q: Are favorites saved permanently?**
A: Currently saved in browser localStorage. For persistence, implement backend.

**Q: Can I use my own API key?**
A: Yes, update `TMDB_API_KEY` in `.env` and `static/recommend.js`.

**Q: Is this production-ready?**
A: Yes! Includes error handling, logging, and comprehensive error recovery.

## 🔗 Quick Links

- Development Guide: `DEVELOPMENT.md`
- Requirements: `requirements.txt`
- Main App: `app.py`
- Error Handler: `error_handler.py`

## 💡 Tips

- Use browser DevTools console to see detailed logs
- Check `app.log` for server-side errors
- Clear browser cache if styles seem outdated
- Test on mobile for responsive design
- Use incognito mode to test without cached data

---

**Ready to explore movies? Start searching now!**
