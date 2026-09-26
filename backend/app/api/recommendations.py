from fastapi import APIRouter, Depends, HTTPException
from app.data.medical_knowledge import MEDICAL_KNOWLEDGE_BASE, HEALTH_SCREENING_RECOMMENDATIONS
from app.core.database import get_db, release_db
from app.core.security import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

def get_age_based_recommendations(age: int) -> list:
    """Get age-appropriate health screening recommendations"""
    if age < 40:
        return HEALTH_SCREENING_RECOMMENDATIONS["age_18_39"]
    elif age < 50:
        return HEALTH_SCREENING_RECOMMENDATIONS["age_40_49"]
    elif age < 65:
        return HEALTH_SCREENING_RECOMMENDATIONS["age_50_64"]
    else:
        return HEALTH_SCREENING_RECOMMENDATIONS["age_65_plus"]

def get_lifestyle_recommendations(health_profile: dict) -> list:
    """Get personalized lifestyle recommendations based on health profile"""
    recommendations = []
    
    # BMI-based recommendations
    bmi = health_profile.get("bmi", 0)
    if bmi > 30:
        recommendations.append({
            "category": "Weight Management",
            "title": "Achieve Healthy Weight",
            "description": "Work with a healthcare provider to create a personalized weight loss plan. Aim for gradual, sustainable weight loss of 1-2 pounds per week.",
            "priority": "high",
            "actionable": True
        })
        recommendations.append({
            "category": "Nutrition",
            "title": "Calorie Awareness",
            "description": "Create a modest calorie deficit (500-750 calories/day) through diet and exercise combination.",
            "priority": "high",
            "actionable": True
        })
    elif bmi < 18.5:
        recommendations.append({
            "category": "Weight Management",
            "title": "Healthy Weight Gain",
            "description": "Consult a registered dietitian for a safe weight gain plan. Focus on nutrient-dense foods.",
            "priority": "high",
            "actionable": True
        })
    
    # Physical activity recommendations
    activity_level = health_profile.get("physical_activity", 0)
    if activity_level < 150:
        recommendations.append({
            "category": "Exercise",
            "title": "Increase Physical Activity",
            description": "Aim for 150 minutes of moderate-intensity aerobic activity per week. Start with 30 minutes of brisk walking 5 days a week.",
            "priority": "high",
            "actionable": True
        })
        recommendations.append({
            "category": "Exercise",
            "title": "Add Strength Training",
            description": "Include muscle-strengthening activities at least 2 days per week. Work major muscle groups (legs, hips, back, abdomen, chest, shoulders, arms).",
            "priority": "medium",
            "actionable": True
        })
    
    # Sleep recommendations
    sleep_hours = health_profile.get("sleep_hours", 0)
    if sleep_hours < 7:
        recommendations.append({
            "category": "Sleep",
            "title": "Improve Sleep Duration",
            description": "Aim for 7-9 hours of quality sleep per night. Establish a consistent sleep schedule and create a relaxing bedtime routine.",
            "priority": "high",
            "actionable": True
        })
    
    # Diet recommendations
    recommendations.append({
        "category": "Nutrition",
        "title": "Follow Mediterranean Diet Pattern",
        "description": "Emphasize plant-based foods, healthy fats (olive oil, nuts, avocados), lean proteins, and whole grains. Limit red meat to once or twice a week.",
        "priority": "high",
        "actionable": True
    })
    recommendations.append({
        "category": "Nutrition",
        "title": "Increase Fruit and Vegetable Intake",
        "description": "Aim for 5-9 servings of fruits and vegetables daily. Choose a variety of colors to ensure a wide range of nutrients.",
        "priority": "medium",
        "actionable": True
    })
    
    # Stress management
    recommendations.append({
        "category": "Mental Health",
        "title": "Practice Stress Management",
        "description": "Engage in stress-reducing activities such as meditation, deep breathing exercises, yoga, or progressive muscle relaxation.",
        "priority": "medium",
        "actionable": True
    })
    
    # Hydration
    recommendations.append({
        "category": "Hydration",
        "title": "Stay Adequately Hydrated",
        "description": "Drink at least 8 glasses (64 oz) of water daily. Increase intake during hot weather or physical activity.",
        "priority": "medium",
        "actionable": True
    })
    
    return recommendations

@router.get("/")
async def get_recommendations(
    current_user: str = Depends(get_current_user)
):
    """Get personalized health recommendations"""
    try:
        conn = await get_db()
    except Exception:
        # Fallback without database - return general recommendations
        return {
            "user_id": current_user,
            "recommendations": get_lifestyle_recommendations({}),
            "screening": ["Regular health check-ups", "Annual physical exam", "Blood pressure monitoring"]
        }
    
    try:
        user = await conn.fetchrow(
            "SELECT * FROM users WHERE id = $1",
            int(current_user)
        )
        
        if not user:
            return {
                "user_id": current_user,
                "recommendations": get_lifestyle_recommendations({}),
                "screening": ["Regular health check-ups", "Annual physical exam", "Blood pressure monitoring"]
            }
        
        # Get health profile
        health_profile = user.get("health_profile", {})
        age = user.get("age", 0)
        
        # Get personalized recommendations
        lifestyle_recs = get_lifestyle_recommendations(health_profile)
        screening_recs = get_age_based_recommendations(age)
        
        return {
            "user_id": current_user,
            "recommendations": lifestyle_recs,
            "screening": screening_recs
        }
    except Exception as e:
        logger.error(f"Error fetching recommendations: {e}")
        return {
            "user_id": current_user,
            "recommendations": get_lifestyle_recommendations({}),
            "screening": ["Regular health check-ups", "Annual physical exam", "Blood pressure monitoring"]
        }
    finally:
        await release_db(conn)

@router.post("/profile")
async def update_health_profile(
    profile_data: dict,
    current_user: str = Depends(get_current_user)
):
    """Update user health profile for recommendations"""
    try:
        conn = await get_db()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available. Please ensure PostgreSQL is running."
        )
    
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
