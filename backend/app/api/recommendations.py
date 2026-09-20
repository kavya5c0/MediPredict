from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_db, release_db
from app.core.security import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
async def get_recommendations(
    current_user: str = Depends(get_current_user)
):
    """Get personalized health recommendations"""
    # Simple rule-based recommendations
    recommendations = [
        {
            "category": "Diet",
            "title": "Balanced Nutrition",
            "description": "Maintain a diet rich in fruits, vegetables, whole grains, and lean proteins.",
            "priority": "high"
        },
        {
            "category": "Exercise",
            "title": "Regular Physical Activity",
            "description": "Aim for at least 150 minutes of moderate exercise per week.",
            "priority": "high"
        },
        {
            "category": "Sleep",
            "title": "Quality Sleep",
            "description": "Get 7-9 hours of quality sleep each night for optimal health.",
            "priority": "medium"
        },
        {
            "category": "Hydration",
            "title": "Stay Hydrated",
            "description": "Drink at least 8 glasses of water daily to maintain proper hydration.",
            "priority": "medium"
        }
    ]
    
    return {
        "user_id": current_user,
        "recommendations": recommendations
    }

@router.post("/profile")
async def update_health_profile(
    profile_data: dict,
    current_user: str = Depends(get_current_user)
):
    """Update user health profile for recommendations"""
    conn = await get_db()
    try:
        await conn.execute(
            "UPDATE users SET health_profile = $1 WHERE id = $2",
            profile_data, int(current_user)
        )
        
        return {
            "message": "Health profile updated successfully",
            "profile": profile_data
        }
    finally:
        await release_db(conn)
