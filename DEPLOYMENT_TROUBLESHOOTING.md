# Deployment Troubleshooting Guide

## Fixed: Serverless Function Crash (FUNCTION_INVOCATION_FAILED)

### What Was Wrong
The Vercel serverless function was crashing during initialization with error code `FUNCTION_INVOCATION_FAILED`. This happened because:

1. **No error handling in api/index.py** - Import failures weren't caught, causing the function to crash silently
2. **No error handlers in Flask app** - Unhandled exceptions would crash the serverless function
3. **Artifact loading could fail silently** - Missing files would crash on app startup
4. **No health check endpoint** - No way to diagnose deployment issues

### Fixes Applied

#### 1. Added Error Handling to Serverless Entry Point (`api/index.py`)
```python
try:
    from app import app
    handler = app
except Exception as e:
    # Creates minimal Flask app with error response
    # This prevents complete function failure
```

#### 2. Added Global Error Handlers (`app.py`)
```python
@app.errorhandler(404)
@app.errorhandler(500)
@app.errorhandler(Exception)
# Catch all exceptions and return JSON responses
```

#### 3. Wrapped Artifact Loading in Try-Catch
```python
try:
    load_artifacts()
except Exception as e:
    logger.error(f"Failed to load artifacts: {str(e)}")
    # App continues to run even if artifacts fail to load
```

#### 4. Added Health Check Endpoint
```
GET /api/health
```
Returns JSON with:
- status: "healthy" or "error"
- data_loaded: true/false
- model_loaded: true/false
- vectorizer_loaded: true/false

### How to Debug Deployment Issues

#### 1. Check Health Endpoint
```bash
curl https://your-vercel-app.vercel.app/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "environment": "production",
  "data_loaded": true,
  "model_loaded": true,
  "vectorizer_loaded": true
}
```

#### 2. Check Vercel Logs
```bash
vercel logs --follow
```

Look for:
- Import errors
- File not found errors
- Permission issues
- Memory/timeout issues

#### 3. Common Issues and Solutions

**Issue: "Vectorizer file not found"**
- Check that `Artifacts/tranform.pkl` exists (note: typo in filename is intentional)
- Ensure file is committed to Git repository

**Issue: "ModuleNotFoundError"**
- Check requirements.txt has all dependencies
- Verify Python version is 3.9+

**Issue: "TemplateNotFound"**
- Ensure `templates/` directory exists
- Check template names match exactly (case-sensitive)

**Issue: "Timeout after 30s"**
- Initial data loading may take too long
- Consider lazy loading on first request instead of app startup

### Testing Before Deployment

1. **Test locally first**
   ```bash
   FLASK_ENV=production python app.py
   ```

2. **Run health check locally**
   ```bash
   curl http://localhost:5000/api/health
   ```

3. **Check all files are committed**
   ```bash
   git status
   ```

4. **Verify Artifacts directory**
   ```bash
   ls -la Artifacts/
   # Should show:
   # main_data.csv
   # nlp_model.pkl
   # tranform.pkl (note the typo)
   ```

### Deployment Checklist

- [ ] All files committed to Git
- [ ] `vercel.json` exists and is correct
- [ ] `api/index.py` exists with error handling
- [ ] `Artifacts/` directory has all required files
- [ ] `requirements.txt` includes all dependencies
- [ ] `FLASK_ENV=production` set in Vercel environment
- [ ] Health check passes locally
- [ ] No merge conflicts in repository

### Quick Redeploy

```bash
git add -A
git commit -m "Fixes for deployment"
git push origin main
vercel --prod
```

### Check Deployment Status

```bash
# View live logs
vercel logs

# Test endpoint
curl https://your-app.vercel.app/api/health

# Test home page
curl https://your-app.vercel.app/
```

## Still Having Issues?

1. Check `vercel logs` output for specific errors
2. Verify all files are in the repository with `git status`
3. Ensure `Artifacts/` directory is committed (not in .gitignore)
4. Check Python version requirement in `vercel.json`
5. Try running `vercel --prod --force` to force a rebuild
