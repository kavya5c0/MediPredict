from fastapi import APIRouter, Depends, HTTPException
from app.models.rag_system import rag_system
from app.core.database import get_db, release_db
from app.core.security import get_current_user
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/query")
async def health_chat_query(query_data: dict):
    """Process health-related query using real RAG system"""
    question = query_data.get("question", "")
    
    if not question:
        raise HTTPException(status_code=400, detail="No question provided")
    
    # Use real RAG system
    result = await rag_system.query(question)
    
    # Save to database if available
    try:
        conn = await get_db()
        try:
            await conn.execute("""
                INSERT INTO chat_history (user_id, question, answer, source_documents, timestamp)
                VALUES ($1, $2, $3, $4, $5)
            """, 1, question, result["answer"], str(result["sources"]), datetime.utcnow())
        finally:
            await release_db(conn)
    except Exception as e:
        logger.error(f"Failed to save chat history: {e}")
    
    return result

@router.get("/history")
async def get_chat_history():
    """Get chat history for user"""
    try:
        conn = await get_db()
    except Exception:
        return {"history": []}
    
    try:
        history = await conn.fetch("""
            SELECT * FROM chat_history ORDER BY timestamp DESC LIMIT 20
        """)
        
        return {"history": [dict(h) for h in history]}
    finally:
        await release_db(conn)

@router.delete("/history")
async def clear_chat_history():
    """Clear chat history for user"""
    try:
        conn = await get_db()
    except Exception:
        return {"message": "Chat history cleared", "deleted": 0}
    
    try:
        deleted = await conn.execute("DELETE FROM chat_history")
        return {"message": "Chat history cleared", "deleted": deleted}
    finally:
        await release_db(conn)
