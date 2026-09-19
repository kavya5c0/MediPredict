from fastapi import APIRouter, Depends, HTTPException
from app.models.rag_system import MedicalRAGSystem
from app.core.database import chat_history_collection
from app.core.security import get_current_user
from bson import ObjectId
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Lazy initialization of RAG system
_rag_system = None

def get_rag_system():
    """Lazy initialization of RAG system to avoid startup failures"""
    global _rag_system
    if _rag_system is None:
        _rag_system = MedicalRAGSystem()
    return _rag_system

@router.post("/query")
async def health_chat_query(
    query_data: dict,
    current_user: str = Depends(get_current_user)
):
    """Process health-related query using RAG system"""
    question = query_data.get("question", "")
    
    if not question:
        raise HTTPException(status_code=400, detail="No question provided")
    
    try:
        # Get RAG system instance (lazy initialization)
        rag_system = get_rag_system()
        
        # Initialize RAG system if needed (with graceful fallback)
        try:
            rag_system.initialize_vectorstore()
            rag_system.setup_qa_chain()
        except Exception as e:
            logger.warning(f"RAG system initialization failed: {e}, using fallback mode")
        
        # Get response from RAG system (has internal fallback handling)
        response = rag_system.query(question)
        
        # Save to chat history
        if chat_history_collection:
            chat_entry = {
                "user_id": current_user,
                "question": question,
                "answer": response["answer"],
                "source_documents": response["source_documents"],
                "timestamp": datetime.utcnow()
            }
            
            try:
                await chat_history_collection.insert_one(chat_entry)
            except Exception as e:
                logger.warning(f"Failed to save chat history: {e}")
        
        return {
            "answer": response["answer"],
            "sources": response["source_documents"],
            "disclaimer": "This is not medical advice. Please consult a healthcare professional."
        }
        
    except Exception as e:
        logger.error(f"Query processing failed: {e}")
        # Return a helpful error response instead of crashing
        return {
            "answer": "I apologize, but I'm unable to process your question at the moment. Please try again later or consult a healthcare professional for medical advice.",
            "sources": [],
            "disclaimer": "This is not medical advice. Please consult a healthcare professional."
        }

@router.get("/history")
async def get_chat_history(
    current_user: str = Depends(get_current_user),
    limit: int = 20
):
    """Get chat history for user"""
    if chat_history_collection is None:
        return {"history": []}
    
    try:
        history = await chat_history_collection.find(
            {"user_id": current_user}
        ).sort("timestamp", -1).to_list(length=limit)
        
        for entry in history:
            entry["_id"] = str(entry["_id"])
            # Convert datetime to string
            if "timestamp" in entry and hasattr(entry["timestamp"], "isoformat"):
                entry["timestamp"] = entry["timestamp"].isoformat()
        
        return {"history": history}
    except Exception as e:
        logger.error(f"Error fetching chat history: {e}")
        return {"history": []}

@router.post("/history")
async def add_to_chat_history(
    chat_data: dict,
    current_user: str = Depends(get_current_user)
):
    """Add entry to chat history"""
    if chat_history_collection is None:
        return {"message": "Database not available", "history": []}
    
    try:
        chat_entry = {
            "user_id": current_user,
            "question": chat_data.get("question", ""),
            "answer": chat_data.get("answer", ""),
            "source_documents": chat_data.get("source_documents", []),
            "timestamp": datetime.utcnow()
        }
        
        await chat_history_collection.insert_one(chat_entry)
        
        return {"message": "Chat history saved"}
    except Exception as e:
        logger.error(f"Error saving chat history: {e}")
        return {"message": "Failed to save chat history"}

@router.delete("/history")
async def clear_chat_history(
    current_user: str = Depends(get_current_user)
):
    """Clear chat history for user"""
    if chat_history_collection is None:
        return {"message": "Database not available", "deleted": 0}
    
    try:
        result = await chat_history_collection.delete_many(
            {"user_id": current_user}
        )
        
        return {
            "message": f"Deleted {result.deleted_count} chat entries",
            "deleted": result.deleted_count
        }
    except Exception as e:
        logger.error(f"Error clearing chat history: {e}")
        return {"message": "Failed to clear history", "deleted": 0}
