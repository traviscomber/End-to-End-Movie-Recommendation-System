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
        vectorizer_path = artifacts_dir / "transform.pkl"
        
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
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(data['comb']) 
        similarity = cosine_similarity(count_matrix)
        logger.info("Similarity matrix created successfully")
        return data, similarity
    except Exception as e:
        logger.error(f"Error creating similarity matrix: {str(e)}")
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


app = Flask(__name__)

# Load artifacts on startup
load_artifacts()

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

@app.route("/api/categories", methods=["GET"])
@handle_errors
def get_categories():
    """Get list of all movie categories/genres."""
    try:
        if data is None:
            create_similarity()
        
        if data is None:
            return jsonify({'error': 'Unable to load movie database'}), 500
        
        # Extract genres from the data
        categories = set()
        for movie_genres in data.get('genres', []):
            if isinstance(movie_genres, str):
                genres_list = [g.strip() for g in movie_genres.split(',')]
                categories.update(genres_list)
        
        sorted_categories = sorted(list(categories))
        logger.info(f"Retrieved {len(sorted_categories)} categories")
        return jsonify({'categories': sorted_categories})
    except Exception as e:
        logger.error(f"Error getting categories: {str(e)}")
        return jsonify({'error': 'Failed to retrieve categories'}), 500

@app.route("/api/movies-by-genre/<genre>", methods=["GET"])
@handle_errors
def get_movies_by_genre(genre):
    """Get movies by genre."""
    try:
        if data is None:
            create_similarity()
        
        if data is None:
            return jsonify({'error': 'Unable to load movie database'}), 500
        
        # Filter movies by genre
        movies = []
        for idx, row in data.iterrows():
            genres_str = str(row.get('genres', ''))
            if genre.lower() in genres_str.lower():
                movies.append({
                    'title': row.get('movie_title', ''),
                    'rating': row.get('imdb_score', 0)
                })
        
        logger.info(f"Retrieved {len(movies)} movies for genre: {genre}")
        return jsonify({'genre': genre, 'movies': movies[:20]})  # Limit to 20
    except Exception as e:
        logger.error(f"Error getting movies by genre: {str(e)}")
        return jsonify({'error': 'Failed to retrieve movies'}), 500

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
    """Get trending/top-rated movies."""
    try:
        if data is None:
            create_similarity()
        
        if data is None:
            return jsonify({'error': 'Unable to load movie database'}), 500
        
        # Sort by rating and return top 10
        trending = data.nlargest(10, 'imdb_score')[['movie_title', 'imdb_score', 'genres']].to_dict('records')
        logger.info(f"Retrieved {len(trending)} trending movies")
        return jsonify({'trending': trending})
    except Exception as e:
        logger.error(f"Error getting trending movies: {str(e)}")
        return jsonify({'error': 'Failed to retrieve trending movies'}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

