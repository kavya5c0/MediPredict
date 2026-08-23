from fastapi import APIRouter, Depends, HTTPException
from app.models.rag_system import MedicalRAGSystem
from app.core.database import chat_history_collection
from app.core.security import get_current_user
from bson import ObjectId
from datetime import datetime

router = APIRouter()
rag_system = MedicalRAGSystem()

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
        # Initialize RAG system if needed
        rag_system.initialize_vectorstore()
        rag_system.setup_qa_chain()
        
        # Get response from RAG system
        response = rag_system.query(question)
        
        # Save to chat history
        chat_entry = {
            "user_id": current_user,
            "question": question,
            "answer": response["answer"],
            "source_documents": response["source_documents"],
            "timestamp": datetime.utcnow()
        }
        
        await chat_history_collection.insert_one(chat_entry)
        
        return {
            "answer": response["answer"],
            "sources": response["source_documents"],
            "disclaimer": "This is not medical advice. Please consult a healthcare professional."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")

@router.get("/history")
async def get_chat_history(
    current_user: str = Depends(get_current_user),
    limit: int = 20
):
    """Get chat history for user"""
    history = await chat_history_collection.find(
        {"user_id": current_user}
    ).sort("timestamp", -1).to_list(length=limit)
    
    for entry in history:
        entry["_id"] = str(entry["_id"])
    
    return {"history": history}

@router.delete("/history")
async def clear_chat_history(
    current_user: str = Depends(get_current_user)
):
    """Clear chat history for user"""
    result = await chat_history_collection.delete_many(
        {"user_id": current_user}
    )
    
    return {
        "message": f"Deleted {result.deleted_count} chat entries"
    }
