from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth
import os

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

# Include other routers
try:
    from app.api import medical
    app.include_router(medical.router, prefix="/api/medical", tags=["Medical Reports"])
except ImportError:
    pass

try:
    from app.api import prediction
    app.include_router(prediction.router, prefix="/api/predict", tags=["Disease Prediction"])
except ImportError:
    pass

try:
    from app.api import chat
    app.include_router(chat.router, prefix="/api/chat", tags=["Health Chat"])
except ImportError:
    pass

try:
    from app.api import recommendations
    app.include_router(recommendations.router, prefix="/api/recommendations", tags=["Recommendations"])
except ImportError:
    pass

@app.get("/")
async def root():
    return {
        "message": "AI-Powered Healthcare Assistant API",
        "version": "1.0.0",
        "environment": "vercel" if IS_VERCEL else "local",
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
