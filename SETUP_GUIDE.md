# Complete Setup Guide - Movie Recommendation System

## System Requirements

- Python 3.8+
- pip or poetry
- Modern web browser (Chrome, Firefox, Safari, Edge)
- 2GB+ RAM
- 500MB+ disk space for dependencies

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/traviscomber/End-to-End-Movie-Recommendation-System.git
cd End-to-End-Movie-Recommendation-System
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your configuration
nano .env  # or use your preferred editor
```

**Important Environment Variables:**

```
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# OpenAI API Key (Optional - for AI features)
# Get from https://platform.openai.com/account/api-keys
OPENAI_API_KEY=sk-your_key_here

# Logging
LOG_LEVEL=INFO
```

### 5. Running Locally

#### Development Mode

```bash
python app.py
```

The app will start at `http://localhost:5000`

#### Production Mode with Gunicorn

```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 --threads 2 --timeout 120 app:app
```

### 6. Docker Setup

#### Build Docker Image

```bash
docker build -t movie-finder:latest .
```

#### Run Container

```bash
docker run -p 5000:5000 -e OPENAI_API_KEY=your_key movie-finder:latest
```

#### Using Docker Compose

```bash
docker-compose up --build
```

The app will be available at `http://localhost:5000`

## OpenAI Integration Setup (Optional)

### Getting OpenAI API Key

1. Go to https://platform.openai.com/account/api-keys
2. Sign up or log in with your OpenAI account
3. Create a new API key
4. Copy the key and add it to your `.env` file:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxx
```

### Using OpenAI Features

With OpenAI configured, the system automatically generates:
- AI-powered movie summaries
- Intelligent recommendation explanations
- Movie comparisons
- Vibe/mood classifications

If OpenAI API key is not set, the system falls back to basic descriptions.

## Data Files

The system uses movie data from:
- **Location:** `Artifacts/main_data.csv`
- **Contains:** Movie titles, genres, cast, plot keywords, ratings, IMDb IDs
- **Size:** Pre-computed similarity matrix for fast recommendations

**Supported Columns:**
- `movie_title`: Film name
- `genres`: Comma-separated genres
- `imdb_score`: Rating (0-10)
- `cast`: Actor names
- `director`: Director name
- `comb`: Combined text features for similarity

## Project Structure

```
End-to-End-Movie-Recommendation-System/
├── app.py                      # Main Flask application
├── openai_helper.py           # OpenAI integration module
├── error_handler.py           # Error handling and logging
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose setup
├── .env.example              # Environment variables template
│
├── templates/                # HTML templates
│   ├── home.html             # Home/search page
│   ├── recommend.html        # Recommendations display
│   └── categories.html       # Genre browsing page
│
├── static/                   # Frontend assets
│   ├── style.css             # Main stylesheet
│   ├── recommend.js          # Recommendation logic
│   ├── autocomplete.js       # Search autocomplete
│   ├── favorites.js          # Favorites management
│   └── utils.js              # Utility functions
│
├── Artifacts/                # Data files
│   ├── main_data.csv         # Movie database
│   ├── nlp_model.pkl         # Sentiment analysis model
│   └── transform.pkl         # NLP vectorizer
│
└── logs/                     # Application logs
```

## Features Overview

### Search & Recommendations
- Type movie name and press Search
- Get 10 similar movies instantly
- View movie details, cast, and reviews

### Browse by Genre
- Click "Browse Genres" to see categories
- View trending/top-rated movies
- Explore movies by genre

### Favorites & History
- Add movies to favorites (saved locally)
- View search history
- One-click re-search from history

### Cast Information
- Click on cast members to see details
- Birthdates, birthplace, biography
- Profile images

### User Reviews
- Real IMDB user reviews (scraped)
- Sentiment analysis (Good/Bad)
- Multiple reviews per movie

### Social Features
- Share movies with friends
- Copy to clipboard or native share
- Shareable links

## Troubleshooting

### Issue: "Movie not in database"
- The movie might have a different title (e.g., "Avengers: Endgame" vs "Avengers Endgame")
- Try searching with different keywords
- Check spelling carefully

### Issue: No recommendations showing
- Ensure `Artifacts/main_data.csv` exists
- Check if the movie was found by TMDB API
- Look at application logs for errors

### Issue: Cast information not loading
- TMDB API might be rate-limited
- Check internet connection
- Verify TMDB API is accessible

### Issue: OpenAI features not working
- Verify API key is correct in .env file
- Check OpenAI account has credits
- Review error logs in `logs/` directory

### Issue: Port 5000 already in use
```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>

# Or use different port
python app.py --port 5001
```

## Performance Optimization

### Caching
- Movie similarity matrix is cached in memory
- Recommendations are instant after initial load
- IMDB reviews are cached during session

### Database Queries
- CSV data is loaded once on startup
- Similarity computation is pre-computed
- Recommendations are O(1) lookups

### Frontend Optimization
- Lazy loading for images
- Debounced search autocomplete
- Minified CSS and JavaScript
- Responsive image sizing

## Deployment

### Heroku Deployment

```bash
# Install Heroku CLI
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy
git push heroku main
```

### AWS EC2 Deployment

```bash
# SSH into instance
ssh -i key.pem ec2-user@your-instance

# Install Python and dependencies
sudo yum install python3 python3-pip
pip install -r requirements.txt

# Run with supervisor or systemd
```

### Docker Hub Deployment

```bash
# Build and push
docker build -t yourusername/movie-finder .
docker push yourusername/movie-finder

# Pull and run
docker pull yourusername/movie-finder
docker run -p 5000:5000 yourusername/movie-finder
```

## API Endpoints

### Public Endpoints

- **GET /** - Home page with search
- **GET /categories** - Categories browse page
- **POST /similarity** - Find similar movies
- **POST /recommend** - Get detailed recommendations

### API Routes

- **GET /api/categories** - Get list of genres (JSON)
- **GET /api/movies-by-genre/<genre>** - Get movies by genre (JSON)
- **GET /api/trending** - Get trending movies (JSON)
- **POST /api/movie-summary** - Get AI summary (requires OpenAI, JSON)

## Development Tips

### Adding New Features

1. Update `app.py` with new endpoints
2. Add route handlers with `@handle_errors` decorator
3. Add templates in `templates/` folder
4. Add styles in `static/style.css`
5. Add JavaScript in `static/` folder
6. Test locally before pushing

### Running Tests

```bash
# Enable debug mode
FLASK_ENV=development python app.py

# Check logs
tail -f logs/app.log
```

### Database Updates

To update movie data:
1. Replace `Artifacts/main_data.csv` with new data
2. Ensure columns match expected format
3. Restart Flask app
4. System will recompute similarity matrix automatically

## Support & Contribution

- Report bugs: GitHub Issues
- Suggest features: GitHub Discussions
- Contribute: Create pull request
- Documentation: Update wiki

## License

MIT License - See LICENSE file for details

## Credits

- TMDB API for movie metadata
- IMDb for user reviews
- OpenAI for AI features
- scikit-learn for ML algorithms
