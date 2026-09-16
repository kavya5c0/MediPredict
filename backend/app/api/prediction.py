from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.disease_model import DiseasePredictor
from app.core.database import predictions_collection
from app.core.security import get_current_user
from bson import ObjectId
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

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
        # Calculate rule-based disease probabilities based on actual health data
        probabilities = _calculate_disease_probabilities(health_data)
        
        # Find the disease with highest probability
        max_disease = max(probabilities.items(), key=lambda x: x[1])
        
        result = {
            "predicted_disease": max_disease[0],
            "confidence": max_disease[1],
            "all_probabilities": probabilities,
            "risk_factors": _analyze_risk_factors(health_data),
            "recommendations": _generate_prediction_recommendations(health_data)
        }
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
    
    # Save prediction to database
    if predictions_collection:
        prediction_data = {
            "user_id": current_user,
            "health_data": health_data,
            "prediction": result,
            "created_at": datetime.utcnow()
        }
        
        try:
            await predictions_collection.insert_one(prediction_data)
        except Exception as e:
            logger.warning(f"Failed to save prediction to database: {e}")
    
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

def _calculate_disease_probabilities(health_data: dict) -> dict:
    """Calculate disease probabilities based on actual health data values"""
    probabilities = {}
    
    # Diabetes risk calculation
    diabetes_risk = 0.05  # baseline
    if health_data.get("glucose_level", 0) > 126:
        diabetes_risk += 0.40
    elif health_data.get("glucose_level", 0) > 100:
        diabetes_risk += 0.20
    if health_data.get("bmi", 0) > 30:
        diabetes_risk += 0.15
    if health_data.get("family_history_diabetes", False):
        diabetes_risk += 0.15
    if health_data.get("age", 0) > 45:
        diabetes_risk += 0.10
    probabilities["Diabetes"] = min(diabetes_risk, 0.95)
    
    # Heart Disease risk calculation
    heart_risk = 0.05  # baseline
    if health_data.get("cholesterol", 0) > 240:
        heart_risk += 0.30
    elif health_data.get("cholesterol", 0) > 200:
        heart_risk += 0.15
    if health_data.get("blood_pressure_systolic", 0) > 140:
        heart_risk += 0.20
    if health_data.get("smoking", False):
        heart_risk += 0.20
    if health_data.get("family_history_heart", False):
        heart_risk += 0.15
    if health_data.get("age", 0) > 55:
        heart_risk += 0.10
    probabilities["Heart Disease"] = min(heart_risk, 0.95)
    
    # Hypertension risk calculation
    hypertension_risk = 0.05  # baseline
    if health_data.get("blood_pressure_systolic", 0) > 140:
        hypertension_risk += 0.50
    elif health_data.get("blood_pressure_systolic", 0) > 130:
        hypertension_risk += 0.30
    elif health_data.get("blood_pressure_systolic", 0) > 120:
        hypertension_risk += 0.15
    if health_data.get("bmi", 0) > 30:
        hypertension_risk += 0.15
    if health_data.get("family_history_hypertension", False):
        hypertension_risk += 0.15
    if health_data.get("stress_level", 0) > 7:
        hypertension_risk += 0.10
    probabilities["Hypertension"] = min(hypertension_risk, 0.95)
    
    # Obesity calculation
    obesity_risk = 0.05  # baseline
    bmi = health_data.get("bmi", 0)
    if bmi > 30:
        obesity_risk = 0.90
    elif bmi > 25:
        obesity_risk = 0.60
    elif bmi > 23:
        obesity_risk = 0.30
    if health_data.get("physical_activity", 0) < 150:
        obesity_risk += 0.10
    probabilities["Obesity"] = min(obesity_risk, 0.95)
    
    # Asthma risk calculation
    asthma_risk = 0.05  # baseline
    if health_data.get("asthma", False):
        asthma_risk = 0.85
    if health_data.get("smoking", False):
        asthma_risk += 0.15
    probabilities["Asthma"] = min(asthma_risk, 0.95)
    
    # COPD risk calculation
    copd_risk = 0.03  # baseline
    if health_data.get("smoking", False):
        copd_risk += 0.30
    if health_data.get("age", 0) > 60:
        copd_risk += 0.15
    probabilities["COPD"] = min(copd_risk, 0.95)
    
    # Arthritis risk calculation
    arthritis_risk = 0.05  # baseline
    if health_data.get("arthritis", False):
        arthritis_risk = 0.85
    if health_data.get("age", 0) > 50:
        arthritis_risk += 0.20
    if health_data.get("bmi", 0) > 30:
        arthritis_risk += 0.15
    probabilities["Arthritis"] = min(arthritis_risk, 0.95)
    
    # Depression risk calculation
    depression_risk = 0.05  # baseline
    if health_data.get("stress_level", 0) > 7:
        depression_risk += 0.30
    if health_data.get("sleep_hours", 0) < 6:
        depression_risk += 0.20
    if health_data.get("physical_activity", 0) < 150:
        depression_risk += 0.10
    probabilities["Depression"] = min(depression_risk, 0.95)
    
    # Anxiety risk calculation
    anxiety_risk = 0.05  # baseline
    if health_data.get("stress_level", 0) > 7:
        anxiety_risk += 0.35
    if health_data.get("sleep_hours", 0) < 6:
        anxiety_risk += 0.15
    probabilities["Anxiety"] = min(anxiety_risk, 0.95)
    
    # Cancer risk calculation (general, low baseline)
    cancer_risk = 0.03  # baseline
    if health_data.get("smoking", False):
        cancer_risk += 0.15
    if health_data.get("age", 0) > 60:
        cancer_risk += 0.10
    if health_data.get("alcohol", False):
        cancer_risk += 0.05
    probabilities["Cancer"] = min(cancer_risk, 0.50)  # Keep conservative
    
    return probabilities

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
    if not predictions_collection:
        return {"predictions": []}
    
    try:
        predictions = await predictions_collection.find(
            {"user_id": current_user}
        ).sort("created_at", -1).to_list(length=50)
        
        for prediction in predictions:
            prediction["_id"] = str(prediction["_id"])
            # Convert datetime objects to strings
            if "created_at" in prediction and hasattr(prediction["created_at"], "isoformat"):
                prediction["created_at"] = prediction["created_at"].isoformat()
        
        return {"predictions": predictions}
    except Exception as e:
        logger.error(f"Error fetching prediction history: {e}")
        return {"predictions": []}
