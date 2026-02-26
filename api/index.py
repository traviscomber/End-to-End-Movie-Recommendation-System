import sys
from pathlib import Path

# Add parent directory to path so imports work correctly
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the Flask app from the main app.py
from app import app

# Export the app for Vercel
handler = app
