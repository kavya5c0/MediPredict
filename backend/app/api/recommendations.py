from fastapi import APIRouter, Depends, HTTPException
from app.services.recommendation_engine import HealthRecommendationEngine
from app.core.database import users_collection
from app.core.security import get_current_user
from bson import ObjectId

router = APIRouter()
recommendation_engine = HealthRecommendationEngine()

@router.get("/")
async def get_recommendations(
    current_user: str = Depends(get_current_user)
):
    """Get personalized health recommendations"""
    # Get user profile
    user = await users_collection.find_one({"_id": ObjectId(current_user)})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create/update user profile in recommendation engine
    health_profile = user.get("health_profile", {})
    health_profile["conditions"] = user.get("conditions", [])
    health_profile["medications"] = user.get("medications", [])
    
    recommendation_engine.create_user_profile(current_user, health_profile)
    
    # Get recommendations
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
