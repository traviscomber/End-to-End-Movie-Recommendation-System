# Deployment Guide

## Fixed Issues

### 1. Vectorizer Filename Mismatch
- **Issue**: Code was looking for `transform.pkl` but the actual file is `tranform.pkl`
- **Fix**: Updated `app.py` line 39 to use correct filename `tranform.pkl`

### 2. Missing Vercel Configuration
- **Issue**: No `vercel.json` file to configure Vercel deployment
- **Fix**: Created `vercel.json` with Python runtime configuration

### 3. Missing API Handler for Vercel
- **Issue**: Vercel needs a specific structure with `/api/index.py` entry point
- **Fix**: Created `/api/index.py` that exports the Flask app

### 4. Flask Path Configuration
- **Issue**: Template and static folders might not be found in serverless environment
- **Fix**: Updated `Flask(__name__)` initialization to explicitly specify template and static folder paths

### 5. Debug Mode in Production
- **Issue**: Debug mode should be disabled in production
- **Fix**: Updated `app.run()` to check `FLASK_ENV` environment variable

## Deployment Steps

### Local Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_ENV=development
export FLASK_DEBUG=True

# Run locally
python app.py
```

### Deploy to Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel
```

### Environment Variables on Vercel
Set these in Vercel project settings:
- `FLASK_ENV=production`
- `OPENAI_API_KEY` (if using AI features)
- `TMDB_API_KEY` (if using TMDB)

## Project Structure for Vercel
```
project-root/
├── api/
│   └── index.py          # Entry point for Vercel
├── app.py                # Main Flask application
├── templates/            # HTML templates
├── static/               # CSS, JS, images
├── Artifacts/            # ML models and data
│   ├── nlp_model.pkl
│   ├── tranform.pkl
│   └── main_data.csv
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel configuration
└── .env.example         # Environment variables template
```

## Troubleshooting

### 503 Bad Gateway
- Check if all dependencies in `requirements.txt` are installed
- Verify `Artifacts` folder and files exist
- Check Vercel logs: `vercel logs`

### Template Not Found
- Ensure `templates/` folder exists in project root
- Verify folder path in Flask initialization

### Module Not Found Errors
- Check that `error_handler.py` and `openai_helper.py` exist
- Verify all imports in `app.py`

### Cold Start Issues
- Vercel cold starts are normal for serverless functions
- First request after deployment may take 10-30 seconds

## Performance Optimization

1. **Artifact Loading**: Models are cached globally on first load
2. **Data Caching**: CSV data is loaded once and reused
3. **Similarity Matrix**: Computed once on startup

## Security Notes

- Never commit `.env` files with real API keys
- Use `.env.example` as a template
- Store sensitive keys in Vercel project settings
- Keep `tranform.pkl` and `nlp_model.pkl` secure (don't expose model internals)
