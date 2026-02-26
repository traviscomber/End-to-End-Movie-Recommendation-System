import sys
from pathlib import Path

# Add parent directory to path so imports work correctly
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    # Import the Flask app from the main app.py
    from app import app
    
    # Export the app for Vercel
    handler = app
    
except Exception as e:
    import logging
    logging.error(f"Failed to import Flask app: {str(e)}", exc_info=True)
    
    # Create a minimal Flask app if main app fails to load
    from flask import Flask, jsonify
    
    app = Flask(__name__)
    
    @app.route('/', methods=['GET', 'HEAD'])
    def health():
        return jsonify({
            'status': 'error',
            'message': f'Failed to initialize application: {str(e)}'
        }), 500
    
    handler = app

