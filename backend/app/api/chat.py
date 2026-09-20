from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_db, release_db
from app.core.security import get_current_user
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

HEALTH_TIPS = {
    "diabetes": "Diabetes symptoms include increased thirst, frequent urination, extreme hunger, unexplained weight loss, fatigue, blurred vision, slow-healing sores, and frequent infections.",
    "heart": "Heart disease symptoms can include chest pain, shortness of breath, pain in neck/jaw/back, fatigue, swelling in legs/ankles, and irregular heartbeat.",
    "blood pressure": "To reduce blood pressure naturally: maintain a healthy diet low in sodium, exercise regularly, manage stress, limit alcohol, quit smoking, maintain healthy weight, and get adequate sleep.",
    "general": "For general health: maintain a balanced diet, exercise regularly, get 7-9 hours of sleep, manage stress, stay hydrated, and avoid smoking and excessive alcohol."
}

@router.post("/query")
async def health_chat_query(query_data: dict):
    """Process health-related query with fallback responses"""
    question = query_data.get("question", "").lower()
    
    if not question:
        raise HTTPException(status_code=400, detail="No question provided")
    
    # Simple keyword matching
    response = HEALTH_TIPS["general"]
    if "diabetes" in question:
        response = HEALTH_TIPS["diabetes"]
    elif "heart" in question or "cardio" in question:
        response = HEALTH_TIPS["heart"]
    elif "blood pressure" in question or "hypertension" in question:
        response = HEALTH_TIPS["blood pressure"]
    
    return {
        "answer": response,
        "sources": [],
        "disclaimer": "This is not medical advice. Please consult a healthcare professional."
    }

@router.get("/history")
async def get_chat_history():
    """Get chat history for user"""
    return {"history": []}

@router.delete("/history")
async def clear_chat_history():
    """Clear chat history for user"""
    return {"message": "Chat history cleared", "deleted": 0}
