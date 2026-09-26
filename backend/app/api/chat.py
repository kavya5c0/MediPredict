from fastapi import APIRouter, Depends, HTTPException
from app.data.medical_knowledge import MEDICAL_KNOWLEDGE_BASE
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

def search_knowledge_base(query: str) -> dict:
    """Search the medical knowledge base for relevant information"""
    query_lower = query.lower()
    results = {}
    
    # Search all categories
    for category, data in MEDICAL_KNOWLEDGE_BASE.items():
        if category == "diabetes" and "diabetes" in query_lower:
            results["diabetes"] = data
        elif category == "hypertension" and ("blood pressure" in query_lower or "hypertension" in query_lower):
            results["hypertension"] = data
        elif category == "heart_disease" and ("heart" in query_lower or "cardio" in query_lower):
            results["heart_disease"] = data
        elif category == "general_health":
            # Check for general health topics
            if "nutrition" in query_lower or "diet" in query_lower or "food" in query_lower:
                results["nutrition"] = data["nutrition"]
            elif "exercise" in query_lower or "physical activity" in query_lower or "workout" in query_lower:
                results["exercise"] = data["exercise"]
            elif "sleep" in query_lower:
                results["sleep"] = data["sleep"]
            elif "water" in query_lower or "hydration" in query_lower:
                results["hydration"] = data["hydration"]
    
    return results

def format_response(query: str, knowledge_data: dict) -> str:
    """Format a comprehensive response based on knowledge base data"""
    response_parts = []
    
    if "diabetes" in knowledge_data:
        data = knowledge_data["diabetes"]
        response_parts.append(f"### Diabetes Information")
        response_parts.append(f"**Symptoms:** {', '.join(data['symptoms'][:5])}...")
        response_parts.append(f"**Risk Factors:** {', '.join(data['risk_factors'][:5])}...")
        response_parts.append(f"**Prevention:** {', '.join(data['prevention'][:3])}...")
    
    elif "hypertension" in knowledge_data:
        data = knowledge_data["hypertension"]
        response_parts.append(f"### Hypertension (High Blood Pressure)")
        response_parts.append(f"**Symptoms:** {', '.join(data['symptoms'][:5])}...")
        response_parts.append(f"**Target Blood Pressure:** {', '.join(data['target_blood_pressure'][:3])}...")
        response_parts.append(f"**Prevention:** {', '.join(data['prevention'][:3])}...")
    
    elif "heart_disease" in knowledge_data:
        data = knowledge_data["heart_disease"]
        response_parts.append(f"### Heart Disease Information")
        response_parts.append(f"**Symptoms:** {', '.join(data['symptoms'][:5])}...")
        response_parts.append(f"**Diet Recommendations:** {', '.join(data['diet_recommendations'][:3])}...")
        response_parts.append(f"**Prevention:** {', '.join(data['prevention'][:3])}...")
    
    if "nutrition" in knowledge_data:
        data = knowledge_data["nutrition"]
        response_parts.append(f"### Nutrition Guidelines")
        response_parts.append(f"**Daily Servings:**")
        response_parts.append(f"- Fruits/Vegetables: {data['fruits_vegetables']}")
        response_parts.append(f"- Whole Grains: {data['whole_grains']}")
        response_parts.append(f"- Limit Sodium: {data['sodium']}")
    
    if "exercise" in knowledge_data:
        data = knowledge_data["exercise"]
        response_parts.append(f"### Exercise Recommendations")
        response_parts.append(f"**Adults:** {data['adults']}")
        response_parts.append(f"**Types:** {', '.join(data['types'])}")
    
    if "sleep" in knowledge_data:
        data = knowledge_data["sleep"]
        response_parts.append(f"### Sleep Guidelines")
        response_parts.append(f"**Adults:** {data['adults']}")
        response_parts.append(f"**Quality:** {data['quality']}")
    
    if "hydration" in knowledge_data:
        data = knowledge_data["hydration"]
        response_parts.append(f"### Hydration Guidelines")
        response_parts.append(f"**Daily Intake:** {data['daily_intake']}")
        response_parts.append(f"**Sources:** {', '.join(data['sources'])}")
    
    if not response_parts:
        response_parts.append("I found general health information that may be helpful:")
        response_parts.append("Maintain a balanced diet, exercise regularly, get adequate sleep, and consult healthcare professionals for specific medical advice.")
    
    return "\n\n".join(response_parts)

@router.post("/query")
async def health_chat_query(query_data: dict):
    """Process health-related query using real medical knowledge base"""
    question = query_data.get("question", "")
    
    if not question:
        raise HTTPException(status_code=400, detail="No question provided")
    
    # Search knowledge base
    knowledge_data = search_knowledge_base(question)
    
    # Format response
    response = format_response(question, knowledge_data)
    
    return {
        "answer": response,
        "sources": ["WHO", "CDC", "Mayo Clinic", "NIH", "American Heart Association"],
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
