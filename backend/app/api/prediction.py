from fastapi import APIRouter, Depends, HTTPException
from app.data.medical_knowledge import DISEASE_RISK_CALCULATORS, MEDICAL_KNOWLEDGE_BASE
from app.models.ml_models import ml_models
from app.core.database import get_db, release_db
from app.core.security import get_current_user
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

def calculate_diabetes_risk(health_data: dict) -> dict:
    """Calculate diabetes risk based on real medical criteria"""
    risk_score = 0
    risk_factors = []
    
    bmi = health_data.get("bmi", 0)
    age = health_data.get("age", 0)
    glucose = health_data.get("glucose_level", 0)
    
    # BMI risk
    if bmi >= 30:
        risk_score += 30
        risk_factors.append("BMI ≥ 30 (obesity)")
    elif bmi >= 25:
        risk_score += 15
        risk_factors.append("BMI 25-29.9 (overweight)")
    
    # Age risk
    if age >= 65:
        risk_score += 25
        risk_factors.append("Age ≥ 65")
    elif age >= 45:
        risk_score += 15
        risk_factors.append("Age 45-64")
    
    # Glucose risk
    if glucose >= 126:
        risk_score += 35
        risk_factors.append("Fasting glucose ≥ 126 mg/dL")
    elif glucose >= 100:
        risk_score += 20
        risk_factors.append("Fasting glucose 100-125 mg/dL (prediabetes)")
    
    # Additional factors
    if health_data.get("physical_activity", 0) < 150:
        risk_score += 20
        risk_factors.append("Physical activity < 150 min/week")
    
    if health_data.get("family_history_diabetes", False):
        risk_score += 15
        risk_factors.append("Family history of diabetes")
    
    # Determine risk level
    if risk_score >= 70:
        predicted_disease = "High Risk - Type 2 Diabetes"
        confidence = 0.85
    elif risk_score >= 40:
        predicted_disease = "Moderate Risk - Prediabetes"
        confidence = 0.75
    else:
        predicted_disease = "Low Risk"
        confidence = 0.65
    
    return {
        "predicted_disease": predicted_disease,
        "confidence": confidence,
        "risk_score": risk_score,
        "risk_factors": risk_factors
    }

def calculate_cardiovascular_risk(health_data: dict) -> dict:
    """Calculate cardiovascular risk based on real medical criteria"""
    risk_score = 0
    risk_factors = []
    
    bmi = health_data.get("bmi", 0)
    systolic_bp = health_data.get("blood_pressure_systolic", 0)
    diastolic_bp = health_data.get("blood_pressure_diastolic", 0)
    cholesterol = health_data.get("cholesterol", 0)
    
    # BMI risk
    if bmi >= 30:
        risk_score += 25
        risk_factors.append("BMI ≥ 30 (obesity)")
    elif bmi >= 25:
        risk_score += 15
        risk_factors.append("BMI 25-29.9 (overweight)")
    
    # Blood pressure risk
    if systolic_bp >= 140 or diastolic_bp >= 90:
        risk_score += 30
        risk_factors.append("Stage 2 Hypertension (≥140/90)")
    elif systolic_bp >= 130 or diastolic_bp >= 80:
        risk_score += 20
        risk_factors.append("Stage 1 Hypertension (130-139/80-89)")
    elif systolic_bp >= 120:
        risk_score += 10
        risk_factors.append("Elevated Blood Pressure (120-129/<80)")
    
    # Cholesterol risk
    if cholesterol >= 240:
        risk_score += 25
        risk_factors.append("Total cholesterol ≥ 240 mg/dL")
    elif cholesterol >= 200:
        risk_score += 15
        risk_factors.append("Borderline high cholesterol (200-239 mg/dL)")
    
    # Age risk
    age = health_data.get("age", 0)
    if age >= 65:
        risk_score += 20
        risk_factors.append("Age ≥ 65")
    elif age >= 45:
        risk_score += 10
        risk_factors.append("Age 45-64")
    
    # Smoking
    if health_data.get("smoking", False):
        risk_score += 30
        risk_factors.append("Smoking")
    
    # Physical inactivity
    if health_data.get("physical_activity", 0) < 150:
        risk_score += 20
        risk_factors.append("Physical inactivity")
    
    # Determine risk level
    if risk_score >= 70:
        predicted_disease = "High Risk - Cardiovascular Disease"
        confidence = 0.85
    elif risk_score >= 40:
        predicted_disease = "Moderate Risk - Cardiovascular Disease"
        confidence = 0.75
    else:
        predicted_disease = "Low Risk"
        confidence = 0.65
    
    return {
        "predicted_disease": predicted_disease,
        "confidence": confidence,
        "risk_score": risk_score,
        "risk_factors": risk_factors
    }

def generate_recommendations(risk_result: dict, health_data: dict) -> list:
    """Generate personalized recommendations based on risk assessment"""
    recommendations = []
    risk_factors = risk_result.get("risk_factors", [])
    
    # BMI-related recommendations
    if any("BMI" in factor for factor in risk_factors):
        recommendations.append({
            "category": "Weight Management",
            "priority": "high",
            "action": "Achieve and maintain a healthy BMI (18.5-24.9)",
            "details": "Consult a healthcare provider for a personalized weight loss plan"
        })
    
    # Blood pressure recommendations
    if any("Blood Pressure" in factor or "Hypertension" in factor for factor in risk_factors):
        recommendations.append({
            "category": "Blood Pressure",
            "priority": "high",
            "action": "Follow DASH diet (Dietary Approaches to Stop Hypertension)",
            "details": "Limit sodium to <2,300 mg/day, increase potassium intake"
        })
        recommendations.append({
            "category": "Blood Pressure",
            "priority": "high",
            "action": "Monitor blood pressure regularly",
            "details": "Keep a log and share with your healthcare provider"
        })
    
    # Physical activity recommendations
    if "Physical inactivity" in risk_factors:
        recommendations.append({
            "category": "Exercise",
            "priority": "high",
            "action": "Increase physical activity to 150 minutes/week",
            "details": "Start with 30 minutes of moderate activity 5 days a week"
        })
    
    # Smoking recommendations
    if "Smoking" in risk_factors:
        recommendations.append({
            "category": "Smoking Cessation",
            "priority": "high",
            "action": "Quit smoking immediately",
            "details": "Consult healthcare provider for smoking cessation programs"
        })
    
    # Glucose/diabetes recommendations
    if any("glucose" in factor.lower() for factor in risk_factors):
        recommendations.append({
            "category": "Blood Sugar Management",
            "priority": "high",
            "action": "Monitor blood glucose regularly",
            "details": "Follow a balanced diet with controlled carbohydrate intake"
        })
        recommendations.append({
            "category": "Nutrition",
            "priority": "medium",
            "action": "Follow a diabetic-friendly diet",
            "details": "Choose complex carbs, limit sugary foods, eat regular meals"
        })
    
    # General health recommendations
    recommendations.append({
        "category": "Regular Screening",
        "priority": "medium",
        "action": "Schedule regular health check-ups",
        "details": "Follow age-appropriate screening guidelines"
    })
    
    recommendations.append({
        "category": "Stress Management",
        "priority": "medium",
        "action": "Practice stress reduction techniques",
        "details": "Meditation, yoga, deep breathing, or regular exercise"
    })
    
    return recommendations

@router.post("/disease")
async def predict_disease(health_data: dict):
    """Predict disease using ML models trained on real medical data"""
    try:
        conn = await get_db()
    except Exception:
        # Fallback without database
        pass
    
    # Use ML models for prediction
    diabetes_result = ml_models.predict_diabetes(health_data)
    heart_result = ml_models.predict_heart_disease(health_data)
    hypertension_result = ml_models.predict_hypertension(health_data)
    stroke_result = ml_models.predict_stroke(health_data)
    kidney_result = ml_models.predict_kidney_disease(health_data)
    liver_result = ml_models.predict_liver_disease(health_data)
    respiratory_result = ml_models.predict_respiratory_disease(health_data)
    
    # Collect results
    predictions = []
    all_probabilities = {}
    
    if diabetes_result:
        predictions.append({
            "disease": "Type 2 Diabetes",
            "prediction": diabetes_result["prediction"],
            "probability": diabetes_result["probability"],
            "risk_level": diabetes_result["risk_level"],
            "method": "ML (Random Forest)"
        })
        all_probabilities["Type 2 Diabetes"] = diabetes_result["probability"]
    
    if heart_result:
        predictions.append({
            "disease": "Heart Disease",
            "prediction": heart_result["prediction"],
            "probability": heart_result["probability"],
            "risk_level": heart_result["risk_level"],
            "method": "ML (Random Forest)"
        })
        all_probabilities["Heart Disease"] = heart_result["probability"]
    
    if hypertension_result:
        predictions.append({
            "disease": "Hypertension",
            "prediction": hypertension_result["prediction"],
            "probability": hypertension_result["probability"],
            "risk_level": hypertension_result["risk_level"],
            "method": "ML (Logistic Regression)"
        })
        all_probabilities["Hypertension"] = hypertension_result["probability"]
    
    if stroke_result:
        predictions.append({
            "disease": "Stroke",
            "prediction": stroke_result["prediction"],
            "probability": stroke_result["probability"],
            "risk_level": stroke_result["risk_level"],
            "method": "ML (Random Forest)"
        })
        all_probabilities["Stroke"] = stroke_result["probability"]
    
    if kidney_result:
        predictions.append({
            "disease": "Kidney Disease",
            "prediction": kidney_result["prediction"],
            "probability": kidney_result["probability"],
            "risk_level": kidney_result["risk_level"],
            "method": "ML (Random Forest)"
        })
        all_probabilities["Kidney Disease"] = kidney_result["probability"]
    
    if liver_result:
        predictions.append({
            "disease": "Liver Disease",
            "prediction": liver_result["prediction"],
            "probability": liver_result["probability"],
            "risk_level": liver_result["risk_level"],
            "method": "ML (Random Forest)"
        })
        all_probabilities["Liver Disease"] = liver_result["probability"]
    
    if respiratory_result:
        predictions.append({
            "disease": "Respiratory Disease",
            "prediction": respiratory_result["prediction"],
            "probability": respiratory_result["probability"],
            "risk_level": respiratory_result["risk_level"],
            "method": "ML (Random Forest)"
        })
        all_probabilities["Respiratory Disease"] = respiratory_result["probability"]
    
    # Find highest risk
    if predictions:
        predictions.sort(key=lambda x: x["probability"], reverse=True)
        highest_risk = predictions[0]
    else:
        # Fallback to rule-based if ML models not available
        diabetes_risk = calculate_diabetes_risk(health_data)
        cardio_risk = calculate_cardiovascular_risk(health_data)
        
        risks = [
            (diabetes_risk["risk_score"], diabetes_risk),
            (cardio_risk["risk_score"], cardio_risk)
        ]
        risks.sort(key=lambda x: x[0], reverse=True)
        highest_risk = risks[0][1]
        
        all_probabilities = {
            "Type 2 Diabetes": 0.5,
            "Cardiovascular Disease": 0.5,
            "Hypertension": 0.3
        }
    
    # Generate recommendations based on ML predictions
    recommendations = generate_ml_recommendations(predictions, health_data)
    
    result = {
        "predicted_disease": highest_risk.get("disease", "Unknown") if predictions else highest_risk["predicted_disease"],
        "confidence": highest_risk.get("probability", 0.7) if predictions else highest_risk["confidence"],
        "risk_level": highest_risk.get("risk_level", "Medium") if predictions else "Medium",
        "method": "Machine Learning" if predictions else "Rule-Based",
        "risk_factors": extract_risk_factors(health_data),
        "recommendations": [rec["action"] for rec in recommendations],
        "all_probabilities": all_probabilities,
        "model_details": predictions
    }
    
    # Save to database if available
    try:
        result_id = await conn.fetchrow("""
            INSERT INTO predictions (user_id, health_data, predicted_disease, confidence, risk_factors, recommendations, all_probabilities)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING id
        """, 1, health_data, result["predicted_disease"], result["confidence"], 
            result["risk_factors"], result["recommendations"], result["all_probabilities"])
        result["prediction_id"] = str(result_id["id"])
    except:
        pass
    finally:
        try:
            await release_db(conn)
        except:
            pass
    
    return result

def extract_risk_factors(health_data: dict) -> list:
    """Extract risk factors from health data for ML model context"""
    risk_factors = []
    
    bmi = health_data.get("bmi", 0)
    if bmi >= 30:
        risk_factors.append("Obesity (BMI ≥ 30)")
    elif bmi >= 25:
        risk_factors.append("Overweight (BMI 25-29.9)")
    
    if health_data.get("smoking", False):
        risk_factors.append("Smoking")
    
    if health_data.get("physical_activity", 0) < 150:
        risk_factors.append("Physical inactivity")
    
    if health_data.get("family_history_diabetes", False):
        risk_factors.append("Family history of diabetes")
    
    return risk_factors

def generate_ml_recommendations(predictions: list, health_data: dict) -> list:
    """Generate recommendations based on ML model predictions"""
    recommendations = []
    
    for pred in predictions:
        if pred["risk_level"] == "High":
            recommendations.append({
                "category": pred["disease"],
                "priority": "high",
                "action": f"High risk for {pred['disease']} detected",
                "details": f"ML model predicts {pred['probability']:.1%} probability"
            })
        elif pred["risk_level"] == "Medium":
            recommendations.append({
                "category": pred["disease"],
                "priority": "medium",
                "action": f"Moderate risk for {pred['disease']}",
                "details": f"ML model predicts {pred['probability']:.1%} probability"
            })
    
    # Add general health recommendations
    recommendations.append({
        "category": "General Health",
        "priority": "medium",
        "action": "Maintain regular health check-ups",
        "details": "Monitor your health metrics regularly"
    })
    
    return recommendations

@router.get("/history")
async def get_prediction_history(
    current_user: str = Depends(get_current_user)
):
    """Get prediction history for user"""
    try:
        conn = await get_db()
    except Exception:
        return {"predictions": []}
    
    try:
        predictions = await conn.fetch("""
            SELECT * FROM predictions WHERE user_id = $1 ORDER BY created_at DESC
        """, int(current_user))
        
        return {"predictions": [dict(p) for p in predictions]}
    finally:
        await release_db(conn)
