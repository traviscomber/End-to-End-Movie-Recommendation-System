# Movie Recommendation System - Enhanced Edition

A modern, AI-powered movie recommendation system with a stunning UI, comprehensive features, and intelligent recommendations.

![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Version](https://img.shields.io/badge/Version-2.0-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## About This Project

Movie recommendation systems are designed to provide personalized movie suggestions to users, enhancing their entertainment experience by helping them discover movies tailored to their preferences. This project showcases a modern, production-ready Movie Recommendation System combining machine learning with beautiful UI design.

**What's New in This Version:**
- Modern glassmorphic UI with smooth animations
- Proper recommendations display with movie cards
- Genre/category browsing system
- Optional OpenAI integration for AI-powered summaries
- User favorites and search history
- Social sharing features
- Comprehensive error handling and logging
- Production-ready deployment setup

## Key Features

### Search & Recommendations
- Intelligent movie search with autocomplete
- Content-based recommendations using cosine similarity
- Beautiful cards showing 10 recommended movies
- Movie details including cast, reviews, and ratings

### Genre Browsing
- Browse movies by category (Action, Drama, Comedy, Sci-Fi, etc.)
- Trending movies carousel
- Genre-specific movie collections
- Emoji-based category icons for easy navigation

### User Features
- **Favorites**: Save movies to personal watchlist (persists locally)
- **Search History**: Track last 20 searches with quick recall
- **Sharing**: Share movies via native share API or clipboard
- **AI Summaries**: Get AI-powered movie summaries (when OpenAI configured)

### Technical Excellence
- Comprehensive error handling with custom exceptions
- Detailed logging for debugging and monitoring
- Performance monitoring for API calls
- Graceful degradation if services unavailable
- Production-ready with Docker support

## Built With

**Backend**
- Flask 2.3+
- Python 3.10+
- Scikit-learn (ML recommendations)
- Pandas (data processing)
- BeautifulSoup4 (web scraping)
- OpenAI API (optional AI features)

**Frontend**
- HTML5 & CSS3 (modern design)
- JavaScript ES6+ (interactive features)
- Bootstrap 4 (responsive layout)
- Font Awesome 6 (icons)

**DevOps**
- Docker & Docker Compose
- Gunicorn (production server)
- Environment configuration

See `requirements.txt` for complete dependency list.

## Quick Start (5 Minutes)

### Prerequisites
- Python 3.8+
- pip or conda
- Git

### Installation

```bash
# 1. Clone repository
git clone https://github.com/traviscomber/End-to-End-Movie-Recommendation-System.git
cd End-to-End-Movie-Recommendation-System

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
python app.py
```

The application will be available at `http://localhost:5000`

### Optional: Configure OpenAI

For AI-powered movie summaries and recommendations:

```bash
# 1. Get API key from: https://platform.openai.com/account/api-keys

# 2. Create .env file
cp .env.example .env

# 3. Add your key to .env
OPENAI_API_KEY=sk-your-key-here

# 4. Restart application
python app.py
```

## Usage

### Search for Movies
1. Visit home page
2. Type a movie name (e.g., "Inception")
3. Click Search
4. Browse recommendations

### Browse by Genre
1. Click "Browse Genres" button
2. Select a genre
3. View all movies in that category

### Manage Favorites
1. While viewing movie, click "♥ Add to Favorites"
2. Click "My Favorites" to view saved movies
3. Use "Clear All" to remove favorites

### View Search History
1. Click "History" button
2. See your last 20 searches
3. Click movie to search again
4. Use "Clear History" to reset

### Share Movies
1. While viewing movie, click "Share" button
2. Choose sharing method (social media or clipboard)
3. Share with friends

## Project Structure

```
.
├── app.py                      # Main Flask application
├── openai_helper.py            # AI integration module
├── error_handler.py            # Error handling utilities
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Production container
├── docker-compose.yml          # Development environment
├── .env.example                # Environment template
├── README.md                   # This file
├── DOCS_INDEX.md               # Documentation guide
├── ENHANCEMENT_SUMMARY.md      # What's new
├── USER_GUIDE.md               # User manual
├── SETUP_GUIDE.md              # Detailed setup
├── templates/
│   ├── home.html              # Search interface
│   ├── recommend.html         # Movie details
│   └── categories.html        # Genre browsing
├── static/
│   ├── style.css              # Modern styling
│   ├── recommend.js           # Recommendations logic
│   ├── categories.js          # Genre browsing
│   ├── favorites.js           # Favorites system
│   ├── utils.js               # Utilities
│   └── autocomplete.js        # Search suggestions
└── Artifacts/
    ├── main_data.csv          # Movie database
    ├── nlp_model.pkl          # ML model
    └── transform.pkl          # Vectorizer
```

## API Endpoints

### Public Routes
- `GET /` - Home page with search
- `GET /categories` - Genre browsing page
- `GET /recommend` - Movie details page

### API Endpoints
- `POST /similarity` - Get recommendations
- `GET /api/categories` - List all genres
- `GET /api/movies-by-genre/<genre>` - Movies by genre
- `POST /api/movie-summary` - AI summary (requires OpenAI)
- `GET /api/trending` - Trending movies

See `ENHANCEMENT_SUMMARY.md` for detailed API documentation.

## Configuration

### Environment Variables

```bash
# Flask Configuration
FLASK_ENV=production              # development or production
FLASK_DEBUG=False                 # Set to True for debugging
LOG_LEVEL=INFO                    # DEBUG, INFO, WARNING, ERROR

# OpenAI (Optional for AI features)
OPENAI_API_KEY=sk-...             # Get from platform.openai.com
```

### Design Customization

Edit `static/style.css` to customize:
- Primary color (--primary): #e50914
- Background (--background): #0f0f0f
- Text color (--text-primary): #ffffff
- And more design tokens

## Deployment

### Docker (Recommended)

```bash
# Development
docker-compose up

# Production
docker build -t movie-finder .
docker run -p 5000:5000 \
  -e OPENAI_API_KEY=sk-... \
  movie-finder
```

### Heroku

```bash
git push heroku main
heroku config:set OPENAI_API_KEY=sk-...
```

### Traditional Server

```bash
gunicorn --bind 0.0.0.0:5000 \
  --workers 4 \
  --threads 2 \
  --timeout 120 \
  app:app
```

See `SETUP_GUIDE.md` for detailed deployment instructions.

## Documentation

- **DOCS_INDEX.md** - Complete documentation guide
- **USER_GUIDE.md** - Feature walkthrough and tips
- **SETUP_GUIDE.md** - Detailed setup and deployment
- **ENHANCEMENT_SUMMARY.md** - What's new and detailed features
- **DEVELOPMENT.md** - Architecture and development guide
- **FEATURES.md** - Complete feature list

Choose one based on your role:
- Users: Start with USER_GUIDE.md
- Developers: Start with SETUP_GUIDE.md
- Everyone: DOCS_INDEX.md for navigation

## Performance Features

- Recommendation caching for fast results
- Lazy loading of images and data
- Optimized CSS with minification
- API call batching where possible
- Graceful error handling
- Detailed performance logging

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Acknowledgments

- Original project: KalyanMurapaka45
- TMDB API for movie data
- OpenAI for AI features
- Bootstrap and Font Awesome for UI components
- scikit-learn for ML algorithms

## Contact & Support

For issues, questions, or suggestions:
1. Check DOCS_INDEX.md for documentation
2. Review troubleshooting sections
3. Check existing GitHub issues
4. Create a new issue with details

## Roadmap

Planned enhancements:
- User accounts and cloud sync
- Collaborative filtering
- More ML models
- Advanced filtering options
- API rate limiting
- User ratings and reviews
- Mobile app version

## Version History

### v2.0 (Current)
- Modern UI redesign with glassmorphism
- Genre browsing system
- OpenAI integration
- Improved error handling
- User favorites and history
- Comprehensive documentation

### v1.0
- Original recommendation system
- Basic UI
- TMDB integration
- Review scraping

---

**Made with ❤️ - Ready for production!**

For comprehensive documentation, start with `DOCS_INDEX.md`

3. **Activate the Virtual Environment** (Optional)
   - Activate the virtual environment based on your operating system:
       ```
       conda activate <Environment_Name>/
       ```

4. **Install Dependencies**
   - Navigate to the project directory:
     ```
     cd [project_directory]
     ```
   - Run the following command to install project dependencies:
     ```
     pip install -r requirements.txt
     ```

5. **Run the Project**
   - Start the project by running the appropriate command.
     ```
     python app.py
     ```

6. **Access the Project**
   - Open a web browser or the appropriate client to access the project.
  
<br><br>
### Option 2: Installation from DockerHub

If you prefer to use Docker, you can install and run the project using a Docker container from DockerHub:

1. **Pull the Docker Image**
   - Open your terminal or command prompt.
   - Run the following command to pull the Docker image from DockerHub:
     ```
     docker pull kalyan45/movierecommend-app
     ```

2. **Run the Docker Container**
   - Start the Docker container by running the following command, and mapping any necessary ports:
     ```
     docker run -p 5000:5000 kalyan45/movierecommend-app
     ```

3. **Access the Project**
   - Open a web browser or the appropriate client to access the project.



   
# Contributing

Contributions make the open-source community such an amazing place to learn, inspire, and create. I would greatly appreciate any contributions you make.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch 
3. Commit your Changes 
4. Push to the Branch 
5. Open a Pull Request

<!-- LICENSE -->
# License

Distributed under the GNU General Public License v3.0. See `LICENSE.txt` for more information.

# Acknowledgements

This project was inspired by the Kaggle dataset on Spam Email Detection and the corresponding competition. We also acknowledge the open-source Python libraries used in this project and their contributors.

