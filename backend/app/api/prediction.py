from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.disease_model import DiseasePredictor
from app.core.database import predictions_collection
from app.core.security import get_current_user
from bson import ObjectId
from datetime import datetime

router = APIRouter()
predictor = DiseasePredictor()

@router.post("/disease")
async def predict_disease(
    health_data: dict,
    current_user: str = Depends(get_current_user)
):
    """Predict disease risk based on health parameters"""
    # Extract features from health data
    features = [
        health_data.get("age", 0),
        health_data.get("bmi", 0),
        health_data.get("blood_pressure_systolic", 0),
        health_data.get("blood_pressure_diastolic", 0),
        health_data.get("heart_rate", 0),
        health_data.get("glucose_level", 0),
        health_data.get("cholesterol", 0),
        1 if health_data.get("smoking", False) else 0,
        1 if health_data.get("alcohol", False) else 0,
        1 if health_data.get("family_history_diabetes", False) else 0,
        1 if health_data.get("family_history_heart", False) else 0,
        1 if health_data.get("family_history_hypertension", False) else 0,
        health_data.get("physical_activity", 0),
        health_data.get("sleep_hours", 0),
        health_data.get("stress_level", 0),
        1 if health_data.get("diabetes", False) else 0,
        1 if health_data.get("heart_disease", False) else 0,
        1 if health_data.get("hypertension", False) else 0,
        1 if health_data.get("asthma", False) else 0,
        1 if health_data.get("arthritis", False) else 0
    ]
    
    try:
        # For demo, create a simple prediction without trained model
        # In production, load trained model
        result = {
            "predicted_disease": "General Health Assessment",
            "confidence": 0.85,
            "all_probabilities": {
                "Diabetes": 0.15,
                "Heart Disease": 0.20,
                "Hypertension": 0.25,
                "Asthma": 0.10,
                "COPD": 0.05,
                "Arthritis": 0.15,
                "Depression": 0.08,
                "Anxiety": 0.12,
                "Obesity": 0.30,
                "Cancer": 0.05
            },
            "risk_factors": _analyze_risk_factors(health_data),
            "recommendations": _generate_prediction_recommendations(health_data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
    
    # Save prediction to database
    prediction_data = {
        "user_id": current_user,
        "health_data": health_data,
        "prediction": result,
        "created_at": datetime.utcnow()
    }
    
    await predictions_collection.insert_one(prediction_data)
    
    return result

def _analyze_risk_factors(health_data: dict) -> List[str]:
    """Analyze risk factors from health data"""
    risk_factors = []
    
    if health_data.get("bmi", 0) > 30:
        risk_factors.append("High BMI (Obesity)")
    
    if health_data.get("blood_pressure_systolic", 0) > 140:
        risk_factors.append("High systolic blood pressure")
    
    if health_data.get("glucose_level", 0) > 126:
        risk_factors.append("Elevated glucose levels")
    
    if health_data.get("cholesterol", 0) > 240:
        risk_factors.append("High cholesterol")
    
    if health_data.get("smoking", False):
        risk_factors.append("Smoking")
    
    if health_data.get("physical_activity", 0) < 150:
        risk_factors.append("Low physical activity")
    
    if health_data.get("sleep_hours", 0) < 6:
        risk_factors.append("Insufficient sleep")
    
    return risk_factors

def _generate_prediction_recommendations(health_data: dict) -> List[str]:
    """Generate recommendations based on prediction"""
    recommendations = []
    
    if health_data.get("bmi", 0) > 25:
        recommendations.append("Consider weight management through diet and exercise")
    
    if health_data.get("blood_pressure_systolic", 0) > 120:
        recommendations.append("Monitor blood pressure regularly")
    
    if health_data.get("smoking", False):
        recommendations.append("Smoking cessation is strongly recommended")
    
    if health_data.get("physical_activity", 0) < 150:
        recommendations.append("Increase physical activity to at least 150 minutes per week")
    
    if health_data.get("stress_level", 0) > 7:
        recommendations.append("Consider stress management techniques")
    
    return recommendations

@router.get("/history")
async def get_prediction_history(
    current_user: str = Depends(get_current_user)
):
    """Get prediction history for user"""
    predictions = await predictions_collection.find(
        {"user_id": current_user}
    ).sort("created_at", -1).to_list(length=50)
    
    for prediction in predictions:
        prediction["_id"] = str(prediction["_id"])
    
    return {"predictions": predictions}
