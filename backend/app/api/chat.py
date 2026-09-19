from fastapi import APIRouter, Depends, HTTPException
from app.core.database import chat_history_collection
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Simple fallback chat responses
HEALTH_TIPS = {
    "diabetes": "Diabetes symptoms include increased thirst, frequent urination, extreme hunger, unexplained weight loss, fatigue, blurred vision, slow-healing sores, and frequent infections. If you experience these symptoms, please consult a healthcare provider for proper diagnosis and treatment.",
    "heart": "Heart disease symptoms can include chest pain, shortness of breath, pain in neck/jaw/back, fatigue, swelling in legs/ankles, and irregular heartbeat. Seek immediate medical attention if you experience chest pain or shortness of breath.",
    "hypertension": "High blood pressure often has no symptoms, but may include headaches, shortness of breath, or nosebleeds. Regular blood pressure monitoring is important for early detection.",
    "blood pressure": "To reduce blood pressure naturally: maintain a healthy diet low in sodium, exercise regularly (30 minutes most days), manage stress through meditation or yoga, limit alcohol consumption, quit smoking, maintain a healthy weight, and get adequate sleep (7-9 hours). Consider the DASH diet which emphasizes fruits, vegetables, whole grains, and low-fat dairy.",
    "general": "For general health: maintain a balanced diet rich in fruits and vegetables, exercise regularly (150 minutes per week), get 7-9 hours of sleep, manage stress, stay hydrated, and avoid smoking and excessive alcohol. Regular check-ups with healthcare providers are essential."
}

@router.post("/query")
async def health_chat_query(query_data: dict):
    """Process health-related query with fallback responses (no auth required for demo)"""
    question = query_data.get("question", "").lower()
    
    if not question:
        raise HTTPException(status_code=400, detail="No question provided")
    
    # Simple keyword matching for demo purposes
    response = "I apologize, but I'm unable to process specific health questions at the moment. The AI chat service requires additional dependencies that aren't currently installed. For accurate medical advice, please consult a healthcare professional."
    
    if "diabetes" in question:
        response = HEALTH_TIPS["diabetes"]
    elif "heart" in question or "cardio" in question:
        response = HEALTH_TIPS["heart"]
    elif "blood pressure" in question or "hypertension" in question:
        response = HEALTH_TIPS["blood pressure"]
    else:
        response = HEALTH_TIPS["general"]
    
    # Save to chat history if available
    if chat_history_collection is not None:
        try:
            chat_entry = {
                "user_id": "demo-user",
                "question": query_data.get("question", ""),
                "answer": response,
                "source_documents": [],
                "timestamp": datetime.utcnow()
            }
            await chat_history_collection.insert_one(chat_entry)
        except Exception as e:
            logger.warning(f"Failed to save chat history: {e}")
    
    return {
        "answer": response,
        "sources": [],
        "disclaimer": "This is not medical advice. Please consult a healthcare professional."
    }

@router.get("/history")
async def get_chat_history():
    """Get chat history for user (no auth required for demo)"""
    if chat_history_collection is None:
        return {"history": []}
    
    try:
        history = await chat_history_collection.find(
            {"user_id": "demo-user"}
        ).sort("timestamp", -1).to_list(length=20)
        
        for entry in history:
            entry["_id"] = str(entry["_id"])
            if "timestamp" in entry and hasattr(entry["timestamp"], "isoformat"):
                entry["timestamp"] = entry["timestamp"].isoformat()
        
        return {"history": history}
    except Exception as e:
        logger.error(f"Error fetching chat history: {e}")
        return {"history": []}

@router.delete("/history")
async def clear_chat_history():
    """Clear chat history for user (no auth required for demo)"""
    if chat_history_collection is None:
        return {"message": "Database not available", "deleted": 0}
    
    try:
        result = await chat_history_collection.delete_many(
            {"user_id": "demo-user"}
        )
        
        return {
            "message": f"Deleted {result.deleted_count} chat entries",
            "deleted": result.deleted_count
        }
    except Exception as e:
        logger.error(f"Error clearing chat history: {e}")
        return {"message": "Failed to clear history", "deleted": 0}
