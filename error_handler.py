"""
Error Handler and Logging Module
Centralized error handling and logging for the Movie Recommendation System
"""

import logging
import sys
from functools import wraps
from flask import jsonify
from datetime import datetime

class MovieRecommendationError(Exception):
    """Base exception for Movie Recommendation System"""
    pass

class DatabaseError(MovieRecommendationError):
    """Exception for database-related errors"""
    pass

class APIError(MovieRecommendationError):
    """Exception for API-related errors"""
    pass

class ConfigurationError(MovieRecommendationError):
    """Exception for configuration-related errors"""
    pass

class LoggerSetup:
    """Configure logging for the application"""
    
    @staticmethod
    def setup(app=None, log_file='app.log'):
        """Setup application logging"""
        logger = logging.getLogger('movie_recommendation')
        logger.setLevel(logging.DEBUG)
        
        # File handler
        try:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.INFO)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            print(f"Error setting up file handler: {e}")
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        return logger

logger = LoggerSetup.setup()

def handle_errors(f):
    """Decorator to handle errors in route handlers"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except APIError as e:
            logger.error(f"API Error in {f.__name__}: {str(e)}")
            return jsonify({'error': 'API Error', 'message': str(e)}), 400
        except DatabaseError as e:
            logger.error(f"Database Error in {f.__name__}: {str(e)}")
            return jsonify({'error': 'Database Error', 'message': 'Unable to access database'}), 500
        except ConfigurationError as e:
            logger.error(f"Configuration Error in {f.__name__}: {str(e)}")
            return jsonify({'error': 'Configuration Error', 'message': str(e)}), 500
        except MovieRecommendationError as e:
            logger.error(f"Movie Recommendation Error in {f.__name__}: {str(e)}")
            return jsonify({'error': 'Error', 'message': str(e)}), 400
        except Exception as e:
            logger.exception(f"Unexpected error in {f.__name__}: {str(e)}")
            return jsonify({'error': 'Unexpected Error', 'message': 'An unexpected error occurred'}), 500
    return decorated_function

class ErrorResponse:
    """Create standardized error responses"""
    
    @staticmethod
    def movie_not_found(movie_name):
        logger.warning(f"Movie not found: {movie_name}")
        return {
            'error': True,
            'message': f'Sorry! The movie "{movie_name}" is not in our database.',
            'suggestion': 'Please check the spelling or try with another movie.'
        }
    
    @staticmethod
    def api_error(endpoint, error_msg):
        logger.error(f"API Error at {endpoint}: {error_msg}")
        return {
            'error': True,
            'message': 'Error connecting to movie database.',
            'details': error_msg
        }
    
    @staticmethod
    def invalid_request(field, reason):
        logger.warning(f"Invalid request for field {field}: {reason}")
        return {
            'error': True,
            'message': f'Invalid {field}: {reason}',
        }

class PerformanceMonitor:
    """Monitor performance of operations"""
    
    def __init__(self, operation_name):
        self.operation_name = operation_name
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        logger.debug(f"Starting operation: {self.operation_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (datetime.now() - self.start_time).total_seconds()
        if exc_type:
            logger.error(f"Operation {self.operation_name} failed after {duration}s: {exc_val}")
        else:
            logger.info(f"Operation {self.operation_name} completed in {duration:.3f}s")
        return False
