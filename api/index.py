import sys
import os

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Simple test to see if imports work
try:
    from app.main import app
    asgi_app = app
except Exception as e:
    print(f"Import error: {e}")
    # Create a minimal fallback app
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.get("/")
    async def root():
        return {"error": "Import failed", "message": str(e)}
    
    asgi_app = app