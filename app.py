import json
import pickle
import requests
import bs4 as bs
import numpy as np
import pandas as pd
import urllib.request
import logging
import os
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from error_handler import (
    LoggerSetup, handle_errors, ErrorResponse, PerformanceMonitor,
    APIError, DatabaseError, ConfigurationError
)
from openai_helper import openai_helper

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = LoggerSetup.setup()

# Get the base directory
BASE_DIR = Path(__file__).resolve().parent

# Global variables for caching
data = None
similarity = None
clf = None
vectorizer = None

# Loading the dataset and trained model with proper error handling
def load_artifacts():
    global clf, vectorizer
    try:
        artifacts_dir = BASE_DIR / "Artifacts"
        model_path = artifacts_dir / "nlp_model.pkl"
        vectorizer_path = artifacts_dir / "tranform.pkl"  # Note: File is named 'tranform' not 'transform'
        
        if not model_path.exists():
            logger.warning(f"Model file not found at {model_path}")
            return False
        if not vectorizer_path.exists():
            logger.warning(f"Vectorizer file not found at {vectorizer_path}")
            return False
            
        clf = pickle.load(open(model_path, 'rb'))
        vectorizer = pickle.load(open(vectorizer_path, 'rb'))
        logger.info("Artifacts loaded successfully")
        return True
    except Exception as e:
        logger.error(f"Error loading artifacts: {str(e)}")
        return False

# Creating a similarity matrix using count vectorizer and cosine similarity
def create_similarity():
    global data, similarity
    try:
        data_path = BASE_DIR / "Artifacts" / "main_data.csv"
        if not data_path.exists():
            logger.warning(f"Data file not found at {data_path}")
            return None, None
            
        data = pd.read_csv(data_path)
        logger.info(f"Loaded data with {len(data)} movies and columns: {list(data.columns)}")
        
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(data['comb']) 
        similarity = cosine_similarity(count_matrix)
        logger.info("Similarity matrix created successfully")
        return data, similarity
    except Exception as e:
        logger.error(f"Error creating similarity matrix: {str(e)}", exc_info=True)
        return None, None

def rcmd(m):
    global data, similarity
    m = m.lower()
    try:
        if data is None or similarity is None:
            data, similarity = create_similarity()
        
        if data is None or similarity is None:
            return 'Error: Unable to load movie database. Please try again later.'
            
        if m not in data['movie_title'].unique():
            return 'Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies'
        else:
            i = data.loc[data['movie_title']==m].index[0]
            lst = list(enumerate(similarity[i]))
            lst = sorted(lst, key = lambda x:x[1] ,reverse=True)
            lst = lst[1:11] # excluding first item since it is the requested movie itself
            l = []
            for i in range(len(lst)):
                a = lst[i][0]
                l.append(data['movie_title'][a])
            return l
    except Exception as e:
        logger.error(f"Error in recommendation: {str(e)}")
        return 'Error occurred while generating recommendations. Please try again.'
    
# Converting list of string to list (eg. "["abc","def"]" to ["abc","def"])
def convert_to_list(my_list):
    try:
        my_list = my_list.split('","')
        my_list[0] = my_list[0].replace('["','')
        my_list[-1] = my_list[-1].replace('"]','')
        return my_list
    except Exception as e:
        logger.error(f"Error converting to list: {str(e)}")
        return []

def get_suggestions():
    try:
        data_path = BASE_DIR / "Artifacts" / "main_data.csv"
        if not data_path.exists():
            logger.warning(f"Data file not found at {data_path}")
            return []
        data = pd.read_csv(data_path)
        return list(data['movie_title'].str.capitalize())
    except Exception as e:
        logger.error(f"Error getting suggestions: {str(e)}")
        return []

# Create template and static folders if they don't exist
template_folder = BASE_DIR / "templates"
static_folder = BASE_DIR / "static"

try:
    template_folder.mkdir(exist_ok=True)
    static_folder.mkdir(exist_ok=True)
except Exception as e:
    logger.warning(f"Could not create folders: {e}")

app = Flask(__name__, 
            template_folder=str(template_folder),
            static_folder=str(static_folder))

# Load artifacts on startup - don't crash if they're missing
try:
    logger.info("Attempting to load artifacts...")
    if load_artifacts():
        logger.info("Artifacts loaded successfully on startup")
    else:
        logger.warning("Artifacts not fully loaded, app will continue without them")
except Exception as e:
    logger.warning(f"Non-critical error loading artifacts: {str(e)}")

# Global error handlers
@app.errorhandler(404)
def not_found(e):
    logger.warning(f"404 Not Found: {request.path}")
    return jsonify({'error': 'Not found', 'path': request.path}), 404

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"500 Internal Server Error: {str(e)}", exc_info=True)
    return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
    return jsonify({'error': 'Server error', 'message': str(e)}), 500

@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint for deployment monitoring."""
    status = {
        'status': 'healthy',
        'environment': os.getenv('FLASK_ENV', 'development'),
        'data_loaded': data is not None,
        'model_loaded': clf is not None,
        'vectorizer_loaded': vectorizer is not None,
    }
    return jsonify(status), 200

@app.route("/api/search", methods=["GET", "POST"])
def api_search():
    """Search for movies - fast endpoint without NLP processing."""
    try:
        query = request.args.get('q', '') or request.form.get('query', '')
        query = query.strip().lower()
        
        if not query:
            return jsonify({'error': 'Please provide a search query', 'movies': [], 'similar': []}), 400
        
        logger.info(f"[v0] Searching for: {query}")
        
        if data is None:
            return jsonify({'error': 'Database not loaded', 'movies': [], 'similar': []}), 500
        
        # Search for movies by title (fuzzy matching) - FAST
        found_movies = []
        for idx, row in data.iterrows():
            title = str(row.get('movie_title', '')).lower()
            # Direct match or partial match
            if query in title or title in query:
                # Build complete movie object
                rating = float(row.get('imdb_score', 6.0))
                director = str(row.get('director_name', 'Unknown Director')).strip() or 'Unknown Director'
                genres = str(row.get('genres', 'N/A')).strip() or 'N/A'
                
                # Collect cast
                cast = []
                for i in range(1, 4):
                    actor = row.get(f'actor_{i}_name')
                    if pd.notna(actor) and str(actor).strip() and str(actor).strip() != 'nan':
                        cast.append(str(actor).strip())
                
                movie_obj = {
                    'movie_title': str(row.get('movie_title', 'Unknown')).strip(),
                    'imdb_score': round(rating, 1),
                    'director_name': director,
                    'genres': genres,
                    'cast': ', '.join(cast) if cast else 'Unknown Cast',
                    'source': 'Database',
                }
                found_movies.append(movie_obj)
        
        logger.info(f"[v0] Found {len(found_movies)} movies matching '{query}'")
        
        result = {
            'query': query,
            'movies': found_movies,
            'similar': [],
            'total_found': len(found_movies),
            'total_similar': 0
        }
        
        logger.info(f"[v0] Search response: {len(found_movies)} movies")
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"[v0] Search error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e), 'movies': [], 'similar': []}), 500

@app.route("/api/recommendations/<movie_title>", methods=["GET"])
def api_recommendations(movie_title):
    """Get NLP-based recommendations for a specific movie."""
    try:
        movie_title = movie_title.strip()
        logger.info(f"[v0] Getting recommendations for: {movie_title}")
        
        if data is None or similarity is None:
            return jsonify({'error': 'Database not loaded', 'recommendations': []}), 500
        
        # Find the movie in database
        matching_movies = data[data['movie_title'].str.lower() == movie_title.lower()]
        if matching_movies.empty:
            logger.warning(f"[v0] Movie not found: {movie_title}")
            return jsonify({'error': f'Movie "{movie_title}" not found', 'recommendations': []}), 404
        
        # Get NLP recommendations
        rec_list = rcmd(matching_movies.iloc[0]['movie_title'])
        
        recommendations = []
        if isinstance(rec_list, list):
            for rec_title in rec_list[:10]:  # Top 10 recommendations
                rec_movie = data[data['movie_title'] == rec_title]
                if not rec_movie.empty:
                    rec_row = rec_movie.iloc[0]
                    rating = float(rec_row.get('imdb_score', 6.0))
                    director = str(rec_row.get('director_name', 'Unknown Director')).strip() or 'Unknown Director'
                    genres = str(rec_row.get('genres', 'N/A')).strip() or 'N/A'
                    
                    # Collect cast
                    cast = []
                    for i in range(1, 4):
                        actor = rec_row.get(f'actor_{i}_name')
                        if pd.notna(actor) and str(actor).strip() and str(actor).strip() != 'nan':
                            cast.append(str(actor).strip())
                    
                    rec_obj = {
                        'movie_title': rec_title,
                        'imdb_score': round(rating, 1),
                        'director_name': director,
                        'genres': genres,
                        'cast': ', '.join(cast) if cast else 'Unknown Cast',
                        'source': 'Database',
                    }
                    recommendations.append(rec_obj)
        
        result = {
            'movie_title': movie_title,
            'recommendations': recommendations,
            'total': len(recommendations)
        }
        
        logger.info(f"[v0] Recommendations response: {len(recommendations)} similar movies")
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"[v0] Recommendations error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e), 'recommendations': []}), 500

@app.route("/")
@app.route("/home")
@handle_errors
def home():
    with PerformanceMonitor("Load Home Page"):
        suggestions = get_suggestions()
        logger.info(f"Loaded {len(suggestions)} movie suggestions")
        return render_template('home.html', suggestions=suggestions)

@app.route("/similarity", methods=["POST"])
@handle_errors
def similarity():
    with PerformanceMonitor("Find Similar Movies"):
        try:
            movie = request.form.get('name', '').strip()
            if not movie:
                logger.warning("Empty movie name provided to similarity endpoint")
                return 'Please enter a movie name'
            
            logger.info(f"Finding recommendations for: {movie}")
            rc = rcmd(movie)
            if type(rc) == str:
                logger.warning(f"Recommendation failed for {movie}: {rc}")
                return rc
            else:
                logger.info(f"Found {len(rc)} recommendations for {movie}")
                m_str = "---".join(rc)
                return m_str
        except Exception as e:
            logger.error(f"Error in similarity endpoint: {str(e)}", exc_info=True)
            return 'Error processing request. Please try again.'

@app.route("/recommend", methods=["POST"])
@handle_errors
def recommend():
    with PerformanceMonitor("Generate Recommendations Page"):
        try:
            # getting data from AJAX request
            title = request.form.get('title', '')
            cast_ids = request.form.get('cast_ids', '[]')
            cast_names = request.form.get('cast_names', '[]')
            cast_chars = request.form.get('cast_chars', '[]')
            cast_bdays = request.form.get('cast_bdays', '[]')
            cast_bios = request.form.get('cast_bios', '[]')
            cast_places = request.form.get('cast_places', '[]')
            cast_profiles = request.form.get('cast_profiles', '[]')
            imdb_id = request.form.get('imdb_id', '')
            poster = request.form.get('poster', '')
            genres = request.form.get('genres', '')
            overview = request.form.get('overview', '')
            vote_average = request.form.get('rating', '0')
            vote_count = request.form.get('vote_count', '0')
            release_date = request.form.get('release_date', '')
            runtime = request.form.get('runtime', '')
            status = request.form.get('status', '')
            rec_movies = request.form.get('rec_movies', '[]')
            rec_posters = request.form.get('rec_posters', '[]')

            logger.info(f"Generating recommendation page for: {title}")

            # get movie suggestions for auto complete
            suggestions = get_suggestions()

            # call the convert_to_list function for every string that needs to be converted to list
            rec_movies = convert_to_list(rec_movies)
            rec_posters = convert_to_list(rec_posters)
            cast_names = convert_to_list(cast_names)
            cast_chars = convert_to_list(cast_chars)
            cast_profiles = convert_to_list(cast_profiles)
            cast_bdays = convert_to_list(cast_bdays)
            cast_bios = convert_to_list(cast_bios)
            cast_places = convert_to_list(cast_places)
            
            # convert string to list (eg. "[1,2,3]" to [1,2,3])
            cast_ids = cast_ids.split(',')
            cast_ids[0] = cast_ids[0].replace("[","")
            cast_ids[-1] = cast_ids[-1].replace("]","")
            
            # rendering the string to python string
            for i in range(len(cast_bios)):
                cast_bios[i] = cast_bios[i].replace(r'\n', '\n').replace(r'\"','\"')
            
            # combining multiple lists as a dictionary which can be passed to the html file so that it can be processed easily and the order of information will be preserved
            movie_cards = {rec_posters[i]: rec_movies[i] for i in range(len(rec_posters))}
            
            casts = {cast_names[i]:[cast_ids[i], cast_chars[i], cast_profiles[i]] for i in range(len(cast_profiles))}

            cast_details = {cast_names[i]:[cast_ids[i], cast_profiles[i], cast_bdays[i], cast_places[i], cast_bios[i]] for i in range(len(cast_places))}

            # web scraping to get user reviews from IMDB site
            reviews_list = []  # list of reviews
            reviews_status = []  # list of comments (good or bad)
            
            try:
                logger.debug(f"Fetching IMDB reviews for ID: {imdb_id}")
                sauce = urllib.request.urlopen(f'https://www.imdb.com/title/{imdb_id}/reviews?ref_=tt_ov_rt', timeout=10).read()
                soup = bs.BeautifulSoup(sauce, 'lxml')
                soup_result = soup.find_all("div", {"class": "text show-more__control"})

                for reviews in soup_result:
                    if reviews.string and clf is not None and vectorizer is not None:
                        reviews_list.append(reviews.string)
                        # passing the review to our model
                        movie_review_list = np.array([reviews.string])
                        movie_vector = vectorizer.transform(movie_review_list)
                        pred = clf.predict(movie_vector)
                        reviews_status.append('Good' if pred else 'Bad')
                
                logger.info(f"Fetched {len(reviews_list)} reviews from IMDB")
            except Exception as e:
                logger.warning(f"Could not fetch IMDB reviews: {str(e)}")

            # combining reviews and comments into a dictionary
            movie_reviews = {reviews_list[i]: reviews_status[i] for i in range(len(reviews_list))}     

            logger.info(f"Successfully generated recommendation page for: {title}")
            # passing all the data to the html file
            return render_template('recommend.html', title=title, poster=poster, overview=overview, vote_average=vote_average,
                vote_count=vote_count, release_date=release_date, runtime=runtime, status=status, genres=genres,
                movie_cards=movie_cards, reviews=movie_reviews, casts=casts, cast_details=cast_details)
        except Exception as e:
            logger.error(f"Error in recommend endpoint: {str(e)}", exc_info=True)
            return render_template('recommend.html', title='Error', poster='', overview='An error occurred while processing your request.',
                                 vote_average='0', vote_count='0', release_date='', runtime='', status='',
                                 genres='', movie_cards={}, reviews={}, casts={}, cast_details={})

@app.route("/categories")
@handle_errors
def categories():
    """Display categories/genres page."""
    with PerformanceMonitor("Load Categories Page"):
        logger.info("Loading categories page")
        return render_template('categories.html')

@app.route("/api/categories-and-trending", methods=["GET"])
@handle_errors
def get_categories_and_trending():
    """Get both categories and trending movies in a single optimized call."""
    try:
        global data, similarity
        if data is None or similarity is None:
            data, similarity = create_similarity()
        
        logger.info("[v0] Fetching categories and trending in single call")
        
        # Default values
        default_categories = ['Action', 'Drama', 'Comedy', 'Thriller', 'Sci-Fi', 'Horror', 'Romance', 'Adventure', 'B-Movies (Tubi)', 'Indie Gems']
        categories = set(default_categories)
        trending_movies = []
        
        # Extract categories from data
        if data is not None and 'genres' in data.columns:
            for movie_genres in data['genres']:
                if isinstance(movie_genres, str):
                    genres_list = [g.strip() for g in movie_genres.split() if g.strip()]
                    categories.update(genres_list)
        
        # Calculate trending movies
        if data is not None:
            for idx, row in data.iterrows():
                if len(trending_movies) >= 10:
                    break
                    
                movie_title = row.get('movie_title', 'Unknown')
                actors = sum(1 for i in range(1, 4) if pd.notna(row.get(f'actor_{i}_name')) and row.get(f'actor_{i}_name') != '')
                has_director = 1 if pd.notna(row.get('director_name')) and row.get('director_name') != '' else 0
                has_genres = 1 if pd.notna(row.get('genres')) and row.get('genres') != '' else 0
                
                score = (actors * 2 + (has_director * 2) + (has_genres * 2)) / 8
                score = min(9.5, max(6.0, score))
                
                trending_movies.append({
                    'movie_title': movie_title,
                    'imdb_score': round(score, 1),
                    'genres': str(row.get('genres', 'Unknown')),
                    'director': str(row.get('director_name', 'Unknown'))
                })
        
        sorted_categories = sorted(list(categories))
        
        result = {
            'categories': sorted_categories if sorted_categories else default_categories,
            'trending': trending_movies,
            'cached': False,
            'timestamp': str(pd.Timestamp.now())
        }
        
        logger.info(f"[v0] Combined response: {len(result['categories'])} categories, {len(result['trending'])} trending movies")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"[v0] Error in combined endpoint: {str(e)}", exc_info=True)
        return jsonify({
            'categories': ['Action', 'Drama', 'Comedy', 'Thriller', 'Sci-Fi', 'Horror', 'Romance', 'Adventure', 'B-Movies (Tubi)', 'Indie Gems'],
            'trending': [],
            'error': str(e)
        }), 200

@app.route("/api/categories", methods=["GET"])
@handle_errors
def get_categories():
    """Get list of all movie categories/genres including indie sections."""
    try:
        global data, similarity
        if data is None or similarity is None:
            data, similarity = create_similarity()
        
        if data is None:
            return jsonify({'categories': ['Action', 'Drama', 'Comedy', 'Thriller', 'Sci-Fi', 'Horror', 'Romance', 'Adventure', 'B-Movies (Tubi)', 'Indie Gems']}), 200
        
        # Extract genres from the data
        categories = set()
        if 'genres' in data.columns:
            for movie_genres in data['genres']:
                if isinstance(movie_genres, str):
                    genres_list = [g.strip() for g in movie_genres.split() if g.strip()]
                    categories.update(genres_list)
        
        # Add indie/alternative sources
        categories.add('B-Movies (Tubi)')
        categories.add('Indie Gems')
        categories.add('Cult Classics')
        categories.add('Hidden Gems')
        
        sorted_categories = sorted(list(categories))
        logger.info(f"Retrieved {len(sorted_categories)} categories")
        return jsonify({'categories': sorted_categories if sorted_categories else ['Action', 'Drama', 'Comedy', 'Thriller', 'Sci-Fi', 'Horror', 'Romance', 'Adventure', 'B-Movies (Tubi)', 'Indie Gems']})
    except Exception as e:
        logger.error(f"Error getting categories: {str(e)}", exc_info=True)
        return jsonify({'categories': ['Action', 'Drama', 'Comedy', 'Thriller', 'Sci-Fi', 'Horror', 'Romance', 'Adventure', 'B-Movies (Tubi)', 'Indie Gems']}), 200

@app.route("/api/movies-by-genre/<genre>", methods=["GET"])
@handle_errors
def get_movies_by_genre(genre):
    """Get movies by genre, including indie/alternative sources."""
    try:
        global data, similarity
        if data is None or similarity is None:
            data, similarity = create_similarity()
        
        genre_lower = genre.lower()
        movies = []
        logger.info(f"[v0] Fetching movies for genre: {genre}")
        
        # Handle special indie/alternative categories
        if 'tubi' in genre_lower or 'b-movies' in genre_lower or 'b-movie' in genre_lower:
            # Return curated B-movie/indie collection
            indie_movies = [
                {'movie_title': 'The Room', 'imdb_score': 7.3, 'source': 'Tubi', 'director_name': 'Tommy Wiseau', 'genres': 'Drama', 'actor_1_name': 'Tommy Wiseau', 'actor_2_name': 'Greg Sestero', 'actor_3_name': 'Carolyn Minnott'},
                {'movie_title': 'Rubber', 'imdb_score': 5.9, 'source': 'Tubi', 'director_name': 'Quentin Dupieux', 'genres': 'Comedy', 'actor_1_name': 'Stephen Spinella', 'actor_2_name': 'Roxane Mesquida', 'actor_3_name': 'Wings Hauser'},
                {'movie_title': 'ThanksKilling', 'imdb_score': 5.8, 'source': 'Tubi', 'director_name': 'Jordan Downey', 'genres': 'Horror', 'actor_1_name': 'Wes Keltner', 'actor_2_name': 'Natalie Rodriguez', 'actor_3_name': ''},
                {'movie_title': 'Birdemic: Shock and Terror', 'imdb_score': 1.9, 'source': 'Tubi', 'director_name': 'James Nguyen', 'genres': 'Sci-Fi', 'actor_1_name': 'Alan Bagh', 'actor_2_name': 'Whitney Moore', 'actor_3_name': 'Janae Cohn'},
                {'movie_title': 'Troll 2', 'imdb_score': 4.0, 'source': 'Tubi', 'director_name': 'Claudio Fragasso', 'genres': 'Horror', 'actor_1_name': 'Michael Stephenson', 'actor_2_name': 'Connie McFarland', 'actor_3_name': 'Jonathan Day'},
                {'movie_title': 'Blood Lake', 'imdb_score': 4.5, 'source': 'Tubi', 'director_name': 'Donald Farmer', 'genres': 'Horror', 'actor_1_name': 'Matt Shell', 'actor_2_name': 'Bridget Marquardt', 'actor_3_name': ''},
                {'movie_title': 'Werewolf', 'imdb_score': 3.2, 'source': 'Tubi', 'director_name': 'Tony Zarindast', 'genres': 'Horror', 'actor_1_name': 'John Roll', 'actor_2_name': 'Adrianna Miles', 'actor_3_name': 'Rib Hilton'},
                {'movie_title': 'Miami Connection', 'imdb_score': 5.4, 'source': 'Tubi', 'director_name': 'Richard Martiez', 'genres': 'Action', 'actor_1_name': 'YK Kim', 'actor_2_name': 'Angelo Di Prospero', 'actor_3_name': 'Craig Sechler'},
                {'movie_title': 'The Giant Gila Monster', 'imdb_score': 4.2, 'source': 'Tubi', 'director_name': 'Ray Kellogg', 'genres': 'Sci-Fi', 'actor_1_name': 'Don Sullivan', 'actor_2_name': 'Lisa Simone', 'actor_3_name': 'Fred Graham'},
                {'movie_title': 'Plan 9 from Outer Space', 'imdb_score': 5.6, 'source': 'Tubi', 'director_name': 'Ed Wood', 'genres': 'Sci-Fi', 'actor_1_name': 'Gregory Walcott', 'actor_2_name': 'Mona McKinnon', 'actor_3_name': 'Duke Moore'},
            ]
            logger.info(f"[v0] Returning {len(indie_movies)} B-movies from Tubi")
            result = {'genre': genre, 'movies': indie_movies[:20], 'source': 'Tubi'}
            logger.info(f"[v0] Response: {result}")
            return jsonify(result)
        
        elif 'indie' in genre_lower or 'gems' in genre_lower or 'hidden' in genre_lower or 'cult' in genre_lower:
            # Return indie/hidden gems
            indie_movies = [
                {'movie_title': 'Everything Everywhere All at Once', 'imdb_score': 8.1, 'source': 'Indie', 'director_name': 'Daniel Kwan, Daniel Scheinert', 'genres': 'Drama', 'actor_1_name': 'Michelle Yeoh', 'actor_2_name': 'Stephanie Hsu', 'actor_3_name': 'Ke Huy Quan'},
                {'movie_title': 'Mulholland Drive', 'imdb_score': 8.0, 'source': 'Indie', 'director_name': 'David Lynch', 'genres': 'Drama', 'actor_1_name': 'Naomi Watts', 'actor_2_name': 'Laura Harring', 'actor_3_name': 'Justin Theroux'},
                {'movie_title': 'Eternal Sunshine of the Spotless Mind', 'imdb_score': 8.3, 'source': 'Indie', 'director_name': 'Michel Gondry', 'genres': 'Romance', 'actor_1_name': 'Jim Carrey', 'actor_2_name': 'Kate Winslet', 'actor_3_name': 'Thomas Jay Ryan'},
                {'movie_title': 'Donnie Darko', 'imdb_score': 8.0, 'source': 'Indie', 'director_name': 'Richard Kelly', 'genres': 'Drama', 'actor_1_name': 'Jake Gyllenhaal', 'actor_2_name': 'Jena Malone', 'actor_3_name': 'Mary McDonnell'},
                {'movie_title': 'A Ghost Story', 'imdb_score': 7.5, 'source': 'Indie', 'director_name': 'David Lowery', 'genres': 'Drama', 'actor_1_name': 'Casey Affleck', 'actor_2_name': 'Rooney Mara', 'actor_3_name': 'Will Old'},
                {'movie_title': 'The Florida Project', 'imdb_score': 7.9, 'source': 'Indie', 'director_name': 'Sean Baker', 'genres': 'Drama', 'actor_1_name': 'Willem Dafoe', 'actor_2_name': 'Bria Vinaite', 'actor_3_name': 'Brooklynn Prince'},
                {'movie_title': 'Hunt for the Wilderpeople', 'imdb_score': 7.9, 'source': 'Indie', 'director_name': 'Taika Waititi', 'genres': 'Comedy', 'actor_1_name': 'Sam Neill', 'actor_2_name': 'Julian Dennison', 'actor_3_name': 'Rima Te Wiata'},
                {'movie_title': 'Moonrise Kingdom', 'imdb_score': 7.8, 'source': 'Indie', 'director_name': 'Wes Anderson', 'genres': 'Adventure', 'actor_1_name': 'Jared Gilman', 'actor_2_name': 'Kara Hayward', 'actor_3_name': 'Bruce Willis'},
                {'movie_title': 'The Lighthouse', 'imdb_score': 7.5, 'source': 'Indie', 'director_name': 'Robert Eggers', 'genres': 'Drama', 'actor_1_name': 'Robert Pattinson', 'actor_2_name': 'Willem Dafoe', 'actor_3_name': 'Valeriia Karaman'},
                {'movie_title': 'Parasite', 'imdb_score': 8.6, 'source': 'Indie', 'director_name': 'Bong Joon-ho', 'genres': 'Thriller', 'actor_1_name': 'Song Kang-ho', 'actor_2_name': 'Lee Sun-kyun', 'actor_3_name': 'Cho Yeo-jeong'},
            ]
            logger.info(f"[v0] Returning {len(indie_movies)} indie gems")
            result = {'genre': genre, 'movies': indie_movies[:20], 'source': 'Indie'}
            logger.info(f"[v0] Response: {result}")
            return jsonify(result)
        
        # Standard genre filtering from main database
        if data is not None and 'genres' in data.columns:
            logger.info(f"[v0] Searching database for genre: {genre_lower}")
            for idx, row in data.iterrows():
                genres_str = str(row.get('genres', '')).lower()
                if genre_lower in genres_str or genre_lower.replace('-', '') in genres_str.replace('-', ''):
                    # Calculate quality score
                    actors_count = sum(1 for i in range(1, 4) if pd.notna(row.get(f'actor_{i}_name')) and row.get(f'actor_{i}_name') != '')
                    has_director = 1 if pd.notna(row.get('director_name')) and row.get('director_name') != '' else 0
                    score = 6.0 + ((actors_count * 0.5 + has_director * 2) / 10.0)
                    score = min(9.5, max(6.0, score))
                    
                    # Build complete movie object with all available data
                    director_name = str(row.get('director_name', 'Unknown Director')).strip()
                    if director_name == '' or director_name == 'nan':
                        director_name = 'Unknown Director'
                    
                    genres = str(row.get('genres', 'N/A')).strip()
                    if genres == '' or genres == 'nan':
                        genres = 'N/A'
                    
                    # Collect cast members
                    cast = []
                    for i in range(1, 4):
                        actor = row.get(f'actor_{i}_name')
                        if pd.notna(actor) and str(actor).strip() and str(actor).strip() != 'nan':
                            cast.append(str(actor).strip())
                    cast_str = ', '.join(cast) if cast else 'Unknown Cast'
                    
                    movie_dict = {
                        'movie_title': str(row.get('movie_title', 'Unknown')).strip(),
                        'title': str(row.get('movie_title', 'Unknown')).strip(),  # Alias for compatibility
                        'imdb_score': round(score, 1),
                        'rating': round(score, 1),  # Alias for compatibility
                        'source': 'Database',
                        'director_name': director_name,
                        'genres': genres,
                        'cast': cast_str,
                        'actor_1_name': str(row.get('actor_1_name', '')).strip() if pd.notna(row.get('actor_1_name')) else '',
                        'actor_2_name': str(row.get('actor_2_name', '')).strip() if pd.notna(row.get('actor_2_name')) else '',
                        'actor_3_name': str(row.get('actor_3_name', '')).strip() if pd.notna(row.get('actor_3_name')) else '',
                    }
                    movies.append(movie_dict)
        else:
            logger.warning(f"[v0] Data not loaded or no genres column")
        
        # Sort by rating descending
        movies_sorted = sorted(movies, key=lambda x: x['rating'], reverse=True)[:20]
        logger.info(f"[v0] Retrieved {len(movies_sorted)} movies for genre: {genre}")
        logger.info(f"[v0] First movie: {movies_sorted[0] if movies_sorted else 'None'}")
        result = {'genre': genre, 'movies': movies_sorted, 'source': 'Database'}
        logger.info(f"[v0] Response movies count: {len(result['movies'])}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"[v0] Error getting movies by genre: {str(e)}", exc_info=True)
        return jsonify({'movies': [], 'genre': genre}), 200

@app.route("/api/movie-summary", methods=["POST"])
@handle_errors
def get_movie_summary():
    """Get AI-powered movie summary and recommendation explanation."""
    try:
        title = request.json.get('title', '')
        overview = request.json.get('overview', '')
        genres = request.json.get('genres', '')
        
        if not title:
            return jsonify({'error': 'Movie title required'}), 400
        
        summary = openai_helper.generate_movie_summary(title, overview, genres)
        logger.info(f"Generated AI summary for: {title}")
        return jsonify(summary)
    except Exception as e:
        logger.error(f"Error generating movie summary: {str(e)}")
        # Return fallback response
        return jsonify({
            'summary': 'A great movie worth watching!',
            'why_recommended': 'Based on content similarity with your search.',
            'perfect_for': 'Movie enthusiasts',
            'vibe': 'Engaging'
        })

@app.route("/api/trending", methods=["GET"])
@handle_errors
def get_trending():
    """Get trending/top-rated movies with calculated quality scores."""
    try:
        global data, similarity
        if data is None or similarity is None:
            data, similarity = create_similarity()
        
        if data is None:
            return jsonify({'trending': []}), 200
        
        # Create trending movies with quality scores based on data completeness
        trending_movies = []
        for idx, row in data.iterrows():
            movie_title = row.get('movie_title', 'Unknown')
            
            # Calculate quality score based on data richness
            actors_count = sum(1 for i in range(1, 4) if pd.notna(row.get(f'actor_{i}_name')) and row.get(f'actor_{i}_name') != '')
            has_director = 1 if pd.notna(row.get('director_name')) and row.get('director_name') != '' else 0
            has_genres = 1 if pd.notna(row.get('genres')) and row.get('genres') != '' else 0
            
            # Calculate score: 6.0-9.5 range
            score_components = (actors_count * 0.5) + (has_director * 2) + (has_genres * 1.5)
            quality_score = 6.0 + (score_components / 10.0)
            quality_score = min(9.5, max(6.0, quality_score))
            
            trending_movies.append({
                'movie_title': movie_title,
                'imdb_score': round(quality_score, 1),
                'genres': str(row.get('genres', 'Unknown')),
                'director': str(row.get('director_name', 'Unknown'))
            })
        
        # Sort by score descending and get top 10
        trending_sorted = sorted(trending_movies, key=lambda x: x['imdb_score'], reverse=True)[:10]
        
        logger.info(f"Retrieved {len(trending_sorted)} trending movies with scores")
        return jsonify({'trending': trending_sorted})
    except Exception as e:
        logger.error(f"Error getting trending movies: {str(e)}", exc_info=True)
        return jsonify({'trending': []}), 200

if __name__ == '__main__':
    # Only run debug server locally, not on Vercel
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host="0.0.0.0", port=5000)

