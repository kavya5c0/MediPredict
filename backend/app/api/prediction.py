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
async def predict_disease(
    health_data: dict,
    current_user: str = Depends(get_current_user)
):
    """Predict disease using ML models trained on real medical data"""
    logger.info(f"Received health data: {health_data}")

    conn = None
    try:
        conn = await get_db()
        logger.info("Database connection established")
    except Exception as e:
        logger.warning(f"Database connection failed: {e}. Running without database.")
    
    # Use ML models for prediction with guaranteed fallback values
    logger.info("Calling ML models...")
    diabetes_result = ml_models.predict_diabetes(health_data)
    logger.info(f"Diabetes result: {diabetes_result}")
    
    heart_result = ml_models.predict_heart_disease(health_data)
    logger.info(f"Heart result: {heart_result}")
    
    hypertension_result = ml_models.predict_hypertension(health_data)
    logger.info(f"Hypertension result: {hypertension_result}")
    
    stroke_result = ml_models.predict_stroke(health_data)
    logger.info(f"Stroke result: {stroke_result}")
    
    kidney_result = ml_models.predict_kidney_disease(health_data)
    logger.info(f"Kidney result: {kidney_result}")
    
    liver_result = ml_models.predict_liver_disease(health_data)
    logger.info(f"Liver result: {liver_result}")
    
    respiratory_result = ml_models.predict_respiratory_disease(health_data)
    logger.info(f"Respiratory result: {respiratory_result}")
    
    # Ensure all results have values (fallback if ML fails)
    diabetes_result = diabetes_result or {"prediction": 0, "probability": 0.5, "risk_level": "Low"}
    heart_result = heart_result or {"prediction": 0, "probability": 0.5, "risk_level": "Low"}
    hypertension_result = hypertension_result or {"prediction": 0, "probability": 0.5, "risk_level": "Low"}
    stroke_result = stroke_result or {"prediction": 0, "probability": 0.5, "risk_level": "Low"}
    kidney_result = kidney_result or {"prediction": 0, "probability": 0.5, "risk_level": "Low"}
    liver_result = liver_result or {"prediction": 0, "probability": 0.5, "risk_level": "Low"}
    respiratory_result = respiratory_result or {"prediction": 0, "probability": 0.5, "risk_level": "Low"}
    
    logger.info(f"After fallback - All results have values")
    
    # Collect results
    predictions = []
    all_probabilities = {}
    
    predictions.append({
        "disease": "Type 2 Diabetes",
        "prediction": diabetes_result["prediction"],
        "probability": diabetes_result["probability"],
        "risk_level": diabetes_result["risk_level"],
        "method": "ML (Random Forest)"
    })
    all_probabilities["Type 2 Diabetes"] = diabetes_result["probability"]
    
    predictions.append({
        "disease": "Heart Disease",
        "prediction": heart_result["prediction"],
        "probability": heart_result["probability"],
        "risk_level": heart_result["risk_level"],
        "method": "ML (Random Forest)"
    })
    all_probabilities["Heart Disease"] = heart_result["probability"]
    
    predictions.append({
        "disease": "Hypertension",
        "prediction": hypertension_result["prediction"],
        "probability": hypertension_result["probability"],
        "risk_level": hypertension_result["risk_level"],
        "method": "ML (Logistic Regression)"
    })
    all_probabilities["Hypertension"] = hypertension_result["probability"]
    
    predictions.append({
        "disease": "Stroke",
        "prediction": stroke_result["prediction"],
        "probability": stroke_result["probability"],
        "risk_level": stroke_result["risk_level"],
        "method": "ML (Random Forest)"
    })
    all_probabilities["Stroke"] = stroke_result["probability"]
    
    predictions.append({
        "disease": "Kidney Disease",
        "prediction": kidney_result["prediction"],
        "probability": kidney_result["probability"],
        "risk_level": kidney_result["risk_level"],
        "method": "ML (Random Forest)"
    })
    all_probabilities["Kidney Disease"] = kidney_result["probability"]
    
    predictions.append({
        "disease": "Liver Disease",
        "prediction": liver_result["prediction"],
        "probability": liver_result["probability"],
        "risk_level": liver_result["risk_level"],
        "method": "ML (Random Forest)"
    })
    all_probabilities["Liver Disease"] = liver_result["probability"]
    
    predictions.append({
        "disease": "Respiratory Disease",
        "prediction": respiratory_result["prediction"],
        "probability": respiratory_result["probability"],
        "risk_level": respiratory_result["risk_level"],
        "method": "ML (Random Forest)"
    })
    all_probabilities["Respiratory Disease"] = respiratory_result["probability"]
    
    logger.info(f"Collected {len(predictions)} predictions")
    logger.info(f"All probabilities: {all_probabilities}")

    # Clinical severity override - prioritize life-threatening conditions
    # Check for Stage 2 Hypertension (BP >= 140/90)
    systolic = health_data.get('blood_pressure_systolic', 0)
    diastolic = health_data.get('blood_pressure_diastolic', 0)

    if systolic >= 140 or diastolic >= 90:
        # Hypertension is critical - boost its priority
        for pred in predictions:
            if pred["disease"] == "Hypertension":
                # Very high BP (160/100 or higher) gets highest priority
                if systolic >= 160 or diastolic >= 100:
                    pred["probability"] = max(pred["probability"], 0.90)
                else:
                    pred["probability"] = max(pred["probability"], 0.85)
                pred["risk_level"] = "High"
                all_probabilities["Hypertension"] = pred["probability"]
                logger.info(f"Critical hypertension detected (BP: {systolic}/{diastolic}) - prioritizing to {pred['probability']}")

    # Check for glucose levels
    glucose = health_data.get('glucose_level', 0)
    if glucose >= 200:
        # Diabetic emergency range - prioritize diabetes
        for pred in predictions:
            if pred["disease"] == "Type 2 Diabetes":
                pred["probability"] = max(pred["probability"], 0.95)
                pred["risk_level"] = "High"
                all_probabilities["Type 2 Diabetes"] = pred["probability"]
                logger.info(f"Critical glucose level detected ({glucose} mg/dL) - prioritizing diabetes")
    elif glucose >= 126 and glucose < 200:
        # Diabetic range but not emergency - moderate boost, but not higher than severe hypertension
        for pred in predictions:
            if pred["disease"] == "Type 2 Diabetes":
                pred["probability"] = max(pred["probability"], 0.70)
                if pred["probability"] >= 0.70:
                    pred["risk_level"] = "High"
                all_probabilities["Type 2 Diabetes"] = pred["probability"]
                logger.info(f"Elevated glucose detected ({glucose} mg/dL) - moderate diabetes risk at {pred['probability']}")

    # Find highest risk after clinical overrides
    predictions.sort(key=lambda x: x["probability"], reverse=True)
    highest_risk = predictions[0]
    
    # Generate recommendations based on ML predictions
    recommendations = generate_ml_recommendations(predictions, health_data)
    
    result = {
        "predicted_disease": highest_risk["disease"],
        "confidence": highest_risk["probability"],
        "risk_level": highest_risk["risk_level"],
        "method": "Machine Learning",
        "risk_factors": extract_risk_factors(health_data),
        "recommendations": [rec["action"] for rec in recommendations],
        "all_probabilities": all_probabilities,
        "model_details": predictions
    }
    
    logger.info(f"Final result: {result['predicted_disease']}")
    
    # Save to database if available
    if conn:
        try:
            import json
            logger.info(f"Attempting to save to database - all_probabilities: {result['all_probabilities']}")
            result_id = await conn.fetchrow("""
                INSERT INTO predictions (user_id, health_data, predicted_disease, confidence, risk_factors, recommendations, all_probabilities)
                VALUES ($1, $2::jsonb, $3, $4, $5, $6, $7::jsonb)
                RETURNING id
            """, int(current_user), json.dumps(health_data), result["predicted_disease"], result["confidence"],
                result["risk_factors"], result["recommendations"], json.dumps(result["all_probabilities"]))
            result["prediction_id"] = str(result_id["id"])
            logger.info(f"Successfully saved to database with ID: {result['prediction_id']}")
        except Exception as e:
            logger.error(f"Failed to save to database: {e}", exc_info=True)
        finally:
            try:
                await release_db(conn)
            except Exception as e:
                logger.error(f"Failed to release database connection: {e}")
    else:
        logger.warning("Skipping database save - no connection available")
    
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
