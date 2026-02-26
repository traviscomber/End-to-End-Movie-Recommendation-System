#!/bin/bash
# Movie Recommendation System startup script

echo "Starting Movie Recommendation System..."
echo "======================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

# Run the app
echo ""
echo "Starting Flask application..."
echo "======================================="
echo "The application will be available at:"
echo "http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "======================================="
echo ""

python app.py
