#!/usr/bin/env python3
"""
Railway deployment verification script
Run this to test if your app is ready for Railway deployment
"""

import os
import sys
from pathlib import Path

def check_requirements():
    """Check if requirements.txt exists"""
    if Path("requirements.txt").exists():
        print("✅ requirements.txt found")
        return True
    print("❌ requirements.txt not found")
    return False

def check_dockerfile():
    """Check if Dockerfile exists"""
    if Path("Dockerfile").exists():
        print("✅ Dockerfile found")
        return True
    print("❌ Dockerfile not found")
    return False

def check_app():
    """Check if app.py exists"""
    if Path("src/backend/app.py").exists():
        print("✅ src/backend/app.py found")
        return True
    print("❌ src/backend/app.py not found")
    return False

def check_frontend():
    """Check if Frontend directory exists"""
    if Path("src/Frontend").exists():
        print("✅ src/Frontend directory found")
        return True
    print("❌ src/Frontend directory not found")
    return False

def check_env():
    """Check environment variables"""
    required_vars = ['FLASK_ENV', 'SECRET_KEY']
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print(f"⚠️  Missing environment variables: {', '.join(missing)}")
        print("   These will be set by Railway")
        return True
    print("✅ Environment variables configured")
    return True

def main():
    print("🚀 Railway Deployment Checklist\n")
    
    checks = [
        ("Requirements", check_requirements),
        ("Dockerfile", check_dockerfile),
        ("Application", check_app),
        ("Frontend", check_frontend),
        ("Environment", check_env),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Error checking {name}: {e}")
            results.append(False)
    
    print("\n" + "="*50)
    if all(results):
        print("✅ All checks passed! Ready for Railway deployment")
        return 0
    else:
        print("❌ Some checks failed. Please fix them before deploying")
        return 1

if __name__ == "__main__":
    sys.exit(main())
