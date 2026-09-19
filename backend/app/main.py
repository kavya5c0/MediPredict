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

@app.get("/")
async def root():
    return {
        "message": "AI-Powered Healthcare Assistant API",
        "version": "1.0.0",
        "environment": "vercel" if IS_VERCEL else "local",
        "status": "minimal"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "environment": "vercel" if IS_VERCEL else "local"}
