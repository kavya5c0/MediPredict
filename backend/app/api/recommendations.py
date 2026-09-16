from fastapi import APIRouter, Depends, HTTPException, status
from app.services.recommendation_engine import HealthRecommendationEngine
from app.core.database import users_collection
from app.core.security import get_current_user
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
recommendation_engine = HealthRecommendationEngine()

@router.get("/")
async def get_recommendations(
    current_user: str = Depends(get_current_user)
):
    """Get personalized health recommendations"""
    # Get user profile
    if not users_collection:
        # Return general recommendations if database is not available
        recommendations = recommendation_engine.get_personalized_recommendations(current_user)
        return {
            "user_id": current_user,
            "recommendations": recommendations
        }
    
    try:
        user = await users_collection.find_one({"_id": ObjectId(current_user)})
        
        if not user:
            # Return general recommendations instead of error
            recommendations = recommendation_engine.get_personalized_recommendations(current_user)
            return {
                "user_id": current_user,
                "recommendations": recommendations
            }
        
        # Create/update user profile in recommendation engine
        health_profile = user.get("health_profile", {})
        health_profile["conditions"] = user.get("conditions", [])
        health_profile["medications"] = user.get("medications", [])
        health_profile["age"] = user.get("age", 0)
        
        recommendation_engine.create_user_profile(current_user, health_profile)
        
        # Get recommendations
        recommendations = recommendation_engine.get_personalized_recommendations(current_user)
        
        return {
            "user_id": current_user,
            "recommendations": recommendations
        }
    except Exception as e:
        logger.error(f"Error fetching recommendations: {e}")
        # Fallback to general recommendations
        recommendations = recommendation_engine.get_personalized_recommendations(current_user)
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
    if not users_collection:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available. Please ensure MongoDB is running."
        )
    
    # Update in database
    await users_collection.update_one(
        {"_id": ObjectId(current_user)},
        {"$set": {"health_profile": profile_data}}
    )
    
    # Update in recommendation engine
    recommendation_engine.create_user_profile(current_user, profile_data)
    
    return {
        "message": "Health profile updated successfully",
        "profile": profile_data
    }

@router.get("/similar-users")
async def get_similar_users(
    current_user: str = Depends(get_current_user)
):
    """Find users with similar health profiles"""
    similar_users = recommendation_engine.find_similar_users(current_user)
    
    return {
        "similar_users": similar_users,
        "count": len(similar_users)
    }
