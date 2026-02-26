#!/usr/bin/env python3
"""
Deployment Health Check Script
Verifies all required files and configurations are in place for Vercel deployment
"""

import os
import sys
from pathlib import Path

def check_files():
    """Check if all required files exist"""
    base_dir = Path(__file__).parent
    required_files = [
        "app.py",
        "requirements.txt",
        "vercel.json",
        "api/index.py",
        "error_handler.py",
        "openai_helper.py",
        "templates/home.html",
        "templates/categories.html",
        "static/style.css",
        "Artifacts/nlp_model.pkl",
        "Artifacts/tranform.pkl",
        "Artifacts/main_data.csv",
    ]
    
    print("Checking required files...")
    missing = []
    for file in required_files:
        path = base_dir / file
        if path.exists():
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - MISSING")
            missing.append(file)
    
    return len(missing) == 0

def check_imports():
    """Check if all required Python modules can be imported"""
    print("\nChecking Python imports...")
    required_modules = [
        "flask",
        "pandas",
        "numpy",
        "sklearn",
        "bs4",
        "nltk",
        "requests",
    ]
    
    all_ok = True
    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError as e:
            print(f"✗ {module} - {e}")
            all_ok = False
    
    return all_ok

def check_flask_config():
    """Check Flask configuration"""
    print("\nChecking Flask configuration...")
    try:
        from app import app, BASE_DIR
        
        # Check template folder
        template_folder = BASE_DIR / "templates"
        if template_folder.exists():
            print(f"✓ Template folder exists: {template_folder}")
        else:
            print(f"✗ Template folder missing: {template_folder}")
            return False
        
        # Check static folder
        static_folder = BASE_DIR / "static"
        if static_folder.exists():
            print(f"✓ Static folder exists: {static_folder}")
        else:
            print(f"✗ Static folder missing: {static_folder}")
            return False
        
        # Check app configuration
        print(f"✓ Flask app initialized")
        return True
    except Exception as e:
        print(f"✗ Error initializing Flask: {e}")
        return False

def main():
    print("=" * 60)
    print("Deployment Health Check")
    print("=" * 60)
    
    checks = [
        ("File Check", check_files),
        ("Import Check", check_imports),
        ("Flask Configuration", check_flask_config),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Error in {name}: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("Health Check Summary")
    print("=" * 60)
    
    all_passed = all(result for _, result in results)
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ All checks passed! Ready for deployment.")
        return 0
    else:
        print("\n✗ Some checks failed. Fix the issues above before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
