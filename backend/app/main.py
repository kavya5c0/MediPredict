from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_redis, close_redis
from app.api import auth
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        await init_redis()
    except Exception as e:
        print(f"Redis initialization failed: {e}")
    yield
    # Shutdown
    try:
        await close_redis()
    except Exception as e:
        print(f"Redis shutdown failed: {e}")

app = FastAPI(
    title="AI-Powered Healthcare Assistant",
    description="Multi-disease healthcare assistant using RAG, medical report analysis, and personalized recommendations",
    version="1.0.0",
    lifespan=lifespan
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

# Try to include optional routers (may fail if dependencies are missing)
try:
    from app.api import medical
    app.include_router(medical.router, prefix="/api/medical", tags=["Medical Reports"])
    print("Medical reports router enabled")
except ImportError as e:
    print(f"Medical reports router disabled: {e}")

try:
    from app.api import prediction
    app.include_router(prediction.router, prefix="/api/predict", tags=["Disease Prediction"])
    print("Disease prediction router enabled")
except ImportError as e:
    print(f"Disease prediction router disabled: {e}")

try:
    from app.api import chat
    app.include_router(chat.router, prefix="/api/chat", tags=["Health Chat"])
    print("Health chat router enabled")
except ImportError as e:
    print(f"Health chat router disabled: {e}")

try:
    from app.api import recommendations
    app.include_router(recommendations.router, prefix="/api/recommendations", tags=["Recommendations"])
    print("Recommendations router enabled")
except ImportError as e:
    print(f"Recommendations router disabled: {e}")

@app.get("/")
async def root():
    return {
        "message": "AI-Powered Healthcare Assistant API",
        "version": "1.0.0",
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
    return {"status": "healthy"}
