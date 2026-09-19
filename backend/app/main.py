from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Try to include routers
try:
    from app.api import auth
    app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
except Exception as e:
    print(f"Auth router failed: {e}")

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

@app.get("/")
async def root():
    return {
        "message": "AI-Powered Healthcare Assistant API",
        "version": "1.0.0",
        "environment": "vercel" if IS_VERCEL else "local",
        "status": "working"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "environment": "vercel" if IS_VERCEL else "local"}
