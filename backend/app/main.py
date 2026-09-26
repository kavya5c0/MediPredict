from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api import auth
from app.core.database import init_db, close_db
import os
from pathlib import Path

# Check if running in Vercel
IS_VERCEL = os.environ.get('VERCEL') == '1'

app = FastAPI(
    title="AI-Powered Healthcare Assistant",
    description="Multi-disease healthcare assistant using RAG, medical report analysis, and personalized recommendations",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])

# Try to include other routers
try:
    from app.api import medical
    app.include_router(medical.router, prefix="/api/medical", tags=["Medical Reports"])
except Exception as e:
    print(f"Medical router failed: {e}")

try:
    from app.api import prediction
    app.include_router(prediction.router, prefix="/api/predict", tags=["Disease Prediction"])
except Exception as e:
    print(f"Prediction router failed: {e}")

try:
    from app.api import chat
    app.include_router(chat.router, prefix="/api/chat", tags=["Health Chat"])
except Exception as e:
    print(f"Chat router failed: {e}")

try:
    from app.api import recommendations
    app.include_router(recommendations.router, prefix="/api/recommendations", tags=["Recommendations"])
except Exception as e:
    print(f"Recommendations router failed: {e}")

# Mount static files for frontend
frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dist / "assets")), name="static")
    
    @app.get("/{path:path}")
    async def serve_frontend(path: str):
        if path.startswith("api"):
            return {"error": "API endpoint not found"}
        file_path = frontend_dist / path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(frontend_dist / "index.html")

@app.get("/")
async def root():
    # Serve frontend index.html if available
    if frontend_dist.exists():
        return FileResponse(frontend_dist / "index.html")
    return {
        "message": "AI-Powered Healthcare Assistant API",
        "version": "1.0.0",
        "environment": "vercel" if IS_VERCEL else "local",
        "status": "working",
        "endpoints": {
            "auth": "/api/auth",
            "medical": "/api/medical",
            "prediction": "/api/predict",
            "chat": "/api/chat",
            "recommendations": "/api/recommendations"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "environment": "vercel" if IS_VERCEL else "local"}

@app.on_event("startup")
async def startup_event():
    try:
        await init_db()
        
        # Create tables
        from app.core.database import get_db, release_db
        conn = await get_db()
        try:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    full_name VARCHAR(255),
                    age INTEGER,
                    gender VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    conditions TEXT[] DEFAULT '{}',
                    medications TEXT[] DEFAULT '{}',
                    health_profile JSONB DEFAULT '{}'
                )
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS medical_reports (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    filename VARCHAR(255),
                    file_path TEXT,
                    text_input TEXT,
                    analysis JSONB,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    analyzed_at TIMESTAMP
                )
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    health_data JSONB,
                    predicted_disease VARCHAR(255),
                    confidence FLOAT,
                    risk_factors TEXT[],
                    recommendations TEXT[],
                    all_probabilities JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    question TEXT,
                    answer TEXT,
                    source_documents TEXT[],
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            print("Database tables created/verified")
        finally:
            await release_db(conn)
    except Exception as e:
        print(f"Database initialization failed: {e}")
        print("Application will start without database features")
    
    # Initialize RAG system
    try:
        from app.models.rag_system import rag_system
        await rag_system.initialize()
        print("RAG system initialized successfully")
    except Exception as e:
        print(f"RAG system initialization failed: {e}")
        print("Chat will use fallback knowledge base")

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()
