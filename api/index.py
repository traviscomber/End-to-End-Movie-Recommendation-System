import sys
import logging
from pathlib import Path

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add parent directory to path so imports work correctly
sys.path.insert(0, str(Path(__file__).parent.parent))

logger.info("[v0] API handler starting...")

try:
    logger.info("[v0] Attempting to import Flask app...")
    from app import app
    logger.info("[v0] Flask app imported successfully")
    
except Exception as e:
    logger.error(f"[v0] Failed to import Flask app: {str(e)}", exc_info=True)
    
    # Create a minimal Flask app if main app fails to load
    from flask import Flask, jsonify
    
    app = Flask(__name__)
    
    @app.route('/', methods=['GET', 'HEAD'])
    def health():
        logger.error(f"[v0] Main app failed to load: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to initialize application',
            'error': str(e)
        }), 500
    
    @app.errorhandler(Exception)
    def handle_error(err):
        logger.error(f"[v0] Unhandled exception: {str(err)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': str(err)
        }), 500

logger.info("[v0] API handler initialized successfully")

