from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_db, release_db
from app.core.security import get_current_user
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/disease")
async def predict_disease(
    health_data: dict,
    current_user: str = Depends(get_current_user)
):
    """Predict disease based on health data"""
    conn = await get_db()
    try:
        # Simple rule-based prediction
        age = health_data.get("age", 0)
        bmi = health_data.get("bmi", 0)
        glucose = health_data.get("glucose_level", 0)
        
        predicted_disease = "Low Risk"
        confidence = 0.85
        risk_factors = []
        recommendations = []
        
        if bmi > 30:
            predicted_disease = "Obesity"
            risk_factors.append("High BMI")
            recommendations.append("Consider weight management")
        
        if glucose > 126:
            predicted_disease = "Type 2 Diabetes"
            risk_factors.append("High glucose levels")
            recommendations.append("Monitor blood sugar regularly")
        
        if bmi > 25 and glucose > 100:
            predicted_disease = "Metabolic Syndrome"
            risk_factors.extend(["Elevated BMI", "High glucose"])
            recommendations.extend(["Diet modification", "Regular exercise"])
        
        # Save prediction
        prediction_id = await conn.fetchrow("""
            INSERT INTO predictions (user_id, health_data, predicted_disease, confidence, risk_factors, recommendations, all_probabilities)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING id
        """, int(current_user), health_data, predicted_disease, confidence, risk_factors, recommendations, {})
        
        return {
            "predicted_disease": predicted_disease,
            "confidence": confidence,
            "risk_factors": risk_factors,
            "recommendations": recommendations,
            "all_probabilities": {}
        }
    finally:
        await release_db(conn)

@router.get("/history")
async def get_prediction_history(
    current_user: str = Depends(get_current_user)
):
    """Get prediction history for user"""
    conn = await get_db()
    try:
        predictions = await conn.fetch("""
            SELECT * FROM predictions WHERE user_id = $1 ORDER BY created_at DESC
        """, int(current_user))
        
        return {"predictions": [dict(p) for p in predictions]}
    finally:
        await release_db(conn)
