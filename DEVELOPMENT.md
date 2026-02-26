# Movie Recommendation System - Development Guide

## Overview

This is a modern, production-ready Movie Recommendation System built with Flask, machine learning, and interactive web technologies. The system provides intelligent movie recommendations based on content similarity, displays detailed movie information, and manages user preferences.

## Project Structure

```
.
├── app.py                          # Main Flask application
├── error_handler.py                # Error handling and logging utilities
├── template.py                     # File structure template
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
│
├── Artifacts/                      # ML models and data
│   ├── main_data.csv              # Movie dataset
│   ├── nlp_model.pkl              # Sentiment analysis model
│   └── transform.pkl              # Feature vectorizer
│
├── templates/                      # HTML templates
│   ├── home.html                  # Home/search page
│   ├── recommend.html             # Movie details page
│   └── index.html                 # (Legacy)
│
└── static/                         # Frontend assets
    ├── style.css                  # Main stylesheet with design tokens
    ├── recommend.js               # Movie recommendation logic
    ├── autocomplete.js            # Search autocomplete
    └── favorites.js               # User favorites management
```

## Features

### Core Features
- **Movie Search**: Auto-complete search with suggestions
- **Content-Based Recommendations**: Uses cosine similarity on movie attributes
- **Movie Details**: Comprehensive information including cast, reviews, and ratings
- **User Reviews**: Sentiment analysis of IMDB reviews
- **Responsive Design**: Mobile-first, fully responsive interface

### User Features
- **Favorites Management**: Save favorite movies locally (browser storage)
- **Search History**: Track previous searches
- **Share Functionality**: Share movies via native share or clipboard
- **Notification System**: User-friendly in-app notifications

### Technical Features
- **Error Handling**: Comprehensive error handling with custom exceptions
- **Performance Monitoring**: Track operation durations
- **Logging System**: File and console logging for debugging
- **Configuration**: Environment-based configuration support

## Setup & Installation

### Prerequisites
- Python 3.7+
- pip or conda
- Git (for version control)

### Installation Steps

1. **Clone or download the repository**
   ```bash
   cd End-to-End-Movie-Recommendation-System
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings (optional - API key for TMDB)
   ```

5. **Verify data files**
   - Ensure `Artifacts/main_data.csv` exists
   - Ensure `Artifacts/nlp_model.pkl` exists
   - Ensure `Artifacts/transform.pkl` exists

## Running the Application

### Development Mode
```bash
python app.py
```

The application will start on `http://localhost:5000`

### Production Mode
For production deployment, use a production WSGI server:

```bash
# Using Gunicorn (recommended)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Using uWSGI
pip install uwsgi
uwsgi --http :5000 --wsgi-file app.py --callable app --processes 4 --threads 2
```

## API Endpoints

### GET `/` and `/home`
Display the home page with movie search interface.

**Response**: HTML page with search form

### POST `/similarity`
Get recommended movies similar to the searched movie.

**Parameters**:
- `name` (string): Movie name to find recommendations for

**Response**:
```
movie1---movie2---movie3---...
```
Or error message if movie not found

### POST `/recommend`
Display detailed movie information with recommendations.

**Parameters**:
- `title` (string): Movie title
- `poster` (string): Movie poster URL
- `genres` (string): Comma-separated genres
- `rating` (float): TMDB rating
- `overview` (string): Movie description
- `release_date` (string): Release date
- `runtime` (string): Duration
- `status` (string): Release status
- `imdb_id` (string): IMDB ID for reviews
- `rec_movies` (JSON): Recommended movie titles
- `rec_posters` (JSON): Recommended movie posters
- `cast_names` (JSON): Cast member names
- `cast_ids` (JSON): Cast member IDs
- And other cast-related fields

**Response**: HTML page with full movie details

## Configuration

### Environment Variables

Create a `.env` file with:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# TMDB API Key (for movie data - already embedded in JavaScript)
# TMDB_API_KEY=your_api_key_here

# Application Settings
LOG_LEVEL=INFO
```

### Application Settings

Key settings in `app.py`:
- `debug=True`: Enable Flask debug mode (set to False in production)
- `host="0.0.0.0"`: Server host
- `port=5000`: Server port

## Database & Data

### Data Sources

1. **main_data.csv**: Movie dataset with features for similarity calculation
   - Columns: `movie_title`, `comb` (combined features), and others
   
2. **TMDB API**: Movie metadata (poster, cast, reviews, ratings)
   - No API key required in client (embedded key used)
   - Rate limits apply - monitor usage

3. **IMDB**: User reviews for sentiment analysis
   - Web scraping with Beautiful Soup
   - May be rate-limited or blocked

### ML Models

- **nlp_model.pkl**: Sentiment classification model (Good/Bad)
- **transform.pkl**: Feature vectorizer for text transformation

## Error Handling

The system includes comprehensive error handling:

### Custom Exceptions
- `MovieRecommendationError`: Base exception
- `DatabaseError`: Data access issues
- `APIError`: External API failures
- `ConfigurationError`: Configuration problems

### Error Logging
All errors are logged to:
- **Console**: Real-time feedback
- **File**: `app.log` for persistence

### User-Facing Errors
Users see friendly error messages with suggestions for resolution.

## Logging

### Log Levels
- `DEBUG`: Detailed operation traces
- `INFO`: General operational information
- `WARNING`: Warning messages (recoverable)
- `ERROR`: Error messages with stack traces

### Log Locations
- **Console**: Visible during development
- **File**: `app.log` in project root

### Example Log Lines
```
2024-01-15 10:30:45 - INFO - Loaded 5000 movie suggestions
2024-01-15 10:30:48 - INFO - Finding recommendations for: Inception
2024-01-15 10:30:50 - INFO - Found 10 recommendations for Inception
```

## Performance Tips

1. **Optimize Dataset**: Keep `main_data.csv` reasonably sized
2. **Cache Results**: The app caches similarities on first load
3. **Limit Reviews**: IMDB scraping can be slow - consider limiting
4. **Use CDN**: Serve images from CDN in production
5. **Database**: Consider migrating to a real database for scale

## Troubleshooting

### Common Issues

**Issue**: "Error in loading Artifacts"
- **Solution**: Verify pickle files exist and are valid
- Check file paths are correct
- Ensure Python version compatibility

**Issue**: "Movie not found in database"
- **Solution**: Check dataset size and content
- Verify movie name spelling
- Database may need updates

**Issue**: IMDB reviews not loading
- **Solution**: IMDB may have rate limits or changed HTML structure
- Update BeautifulSoup selectors if needed
- Reviews are optional - app works without them

**Issue**: Slow recommendations
- **Solution**: Check dataset size
- Monitor server resources
- Consider pagination for large datasets

**Issue**: Favorites not persisting
- **Solution**: This uses localStorage (browser storage)
- Works only within same browser/domain
- For persistence, implement backend storage

## Deployment Options

### Heroku
```bash
# Install Heroku CLI
heroku login
heroku create your-app-name
git push heroku main
```

### Docker
```bash
docker build -t movie-rec .
docker run -p 5000:5000 movie-rec
```

### AWS / Google Cloud / DigitalOcean
Use standard Python Flask deployment procedures with the provided `requirements.txt`.

## Development Guidelines

### Code Style
- Use 4-space indentation
- Follow PEP 8 for Python
- Use meaningful variable names
- Add docstrings to functions

### Testing
Manually test:
1. Search functionality
2. Recommendation accuracy
3. Page load times
4. Error scenarios
5. Mobile responsiveness

### Adding Features
1. Create feature branch
2. Implement with logging
3. Add error handling
4. Test thoroughly
5. Update documentation
6. Submit PR

## Security Considerations

1. **API Keys**: Don't commit real keys; use environment variables
2. **Input Validation**: Validate all user inputs
3. **CORS**: Configure appropriately for production
4. **Rate Limiting**: Implement for public deployments
5. **HTTPS**: Always use in production
6. **Dependencies**: Keep packages updated

## Browser Compatibility

- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support
- IE: Not supported (use Edge)

Tested viewport sizes:
- Mobile: 320px - 480px
- Tablet: 481px - 768px
- Desktop: 769px+

## Browser Storage

- **Favorites**: Stored in `localStorage` under `movieRecommendations_favorites`
- **History**: Stored in `localStorage` under `movieRecommendations_history`
- **Persistence**: Limited to same browser/domain
- **Capacity**: ~5-10MB per domain

## Future Enhancements

- User accounts with cloud sync
- Advanced filtering (genre, year, ratings)
- Collaborative filtering recommendations
- Movie watchlist/ratings
- Integration with streaming services
- Real-time notifications
- Backend database (PostgreSQL/MongoDB)
- API authentication
- Advanced analytics

## Support & Contributing

For issues or contributions:
1. Check existing issues
2. Document the problem clearly
3. Provide steps to reproduce
4. Include logs/screenshots
5. Submit with detailed PR description

## License

This project is part of the Movie Recommendation System series.

## Contact

For questions or feedback, please refer to the project documentation.

---

**Last Updated**: 2024-01-15
**Version**: 2.0
**Status**: Production Ready
