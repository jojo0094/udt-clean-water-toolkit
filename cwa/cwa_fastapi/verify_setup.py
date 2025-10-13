#!/usr/bin/env python3
"""
Verification script to check if all imports work correctly
"""
import sys

def verify_imports():
    """Check if all required modules can be imported"""
    errors = []
    
    try:
        import fastapi
        print("✓ FastAPI imported successfully")
    except ImportError as e:
        errors.append(f"✗ FastAPI import failed: {e}")
    
    try:
        import uvicorn
        print("✓ Uvicorn imported successfully")
    except ImportError as e:
        errors.append(f"✗ Uvicorn import failed: {e}")
    
    try:
        import sqlalchemy
        print("✓ SQLAlchemy imported successfully")
    except ImportError as e:
        errors.append(f"✗ SQLAlchemy import failed: {e}")
    
    try:
        import geoalchemy2
        print("✓ GeoAlchemy2 imported successfully")
    except ImportError as e:
        errors.append(f"✗ GeoAlchemy2 import failed: {e}")
    
    try:
        import psycopg2
        print("✓ Psycopg2 imported successfully")
    except ImportError as e:
        errors.append(f"✗ Psycopg2 import failed: {e}")
    
    try:
        import shapely
        print("✓ Shapely imported successfully")
    except ImportError as e:
        errors.append(f"✗ Shapely import failed: {e}")
    
    try:
        import pydantic
        print("✓ Pydantic imported successfully")
    except ImportError as e:
        errors.append(f"✗ Pydantic import failed: {e}")
    
    if errors:
        print("\n" + "="*50)
        print("ERRORS FOUND:")
        for error in errors:
            print(error)
        return False
    
    print("\n" + "="*50)
    print("All imports successful!")
    return True

def verify_app_structure():
    """Check if the app structure is correct"""
    import os
    
    required_files = [
        "__init__.py",
        "main.py",
        "routes.py",
        "models.py",
        "schemas.py",
        "database.py",
        "requirements.txt"
    ]
    
    print("\nChecking file structure:")
    all_found = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} found")
        else:
            print(f"✗ {file} missing")
            all_found = False
    
    return all_found

if __name__ == "__main__":
    print("FastAPI Application Verification")
    print("="*50)
    
    imports_ok = verify_imports()
    structure_ok = verify_app_structure()
    
    if imports_ok and structure_ok:
        print("\n" + "="*50)
        print("✓ Verification successful! Ready to run.")
        sys.exit(0)
    else:
        print("\n" + "="*50)
        print("✗ Verification failed. Please check the errors above.")
        sys.exit(1)
