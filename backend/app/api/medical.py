from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from typing import Optional
from app.core.database import get_db, release_db
from app.core.security import get_current_user
from datetime import datetime
import aiofiles
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/upload")
async def upload_medical_report(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user)
):
    """Upload and analyze medical report"""
    conn = await get_db()
    try:
        # Validate file type
        allowed_extensions = {'.pdf', '.jpg', '.jpeg', '.png', '.gif', '.bmp'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type {file_ext} not allowed. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Save uploaded file
        upload_dir = "uploads/medical_reports"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, f"{current_user}_{file.filename}")
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Save to database
        report_id = await conn.fetchrow("""
            INSERT INTO medical_reports (user_id, filename, file_path, uploaded_at)
            VALUES ($1, $2, $3, $4)
            RETURNING id
        """, int(current_user), file.filename, file_path, datetime.utcnow())
        
        return {
            "message": "File uploaded successfully",
            "report_id": str(report_id["id"])
        }
    finally:
        await release_db(conn)

@router.post("/analyze/text")
async def analyze_medical_text(
    text_data: dict,
    current_user: str = Depends(get_current_user)
):
    """Analyze medical text directly"""
    conn = await get_db()
    try:
        text = text_data.get("text", "")
        
        if not text:
            raise HTTPException(status_code=400, detail="No text provided")
        
        # Simple analysis
        analysis = {
            "summary": "Medical report analysis based on provided text",
            "key_findings": ["Analysis completed"],
            "recommendations": ["Consult healthcare provider"]
        }
        
        # Save to database
        report_id = await conn.fetchrow("""
            INSERT INTO medical_reports (user_id, text_input, analysis, analyzed_at)
            VALUES ($1, $2, $3, $4)
            RETURNING id
        """, int(current_user), text, analysis, datetime.utcnow())
        
        return {
            "report_id": str(report_id["id"]),
            "analysis": analysis
        }
    finally:
        await release_db(conn)

@router.get("/reports")
async def get_medical_reports(
    current_user: str = Depends(get_current_user)
):
    """Get all medical reports for user"""
    conn = await get_db()
    try:
        reports = await conn.fetch("""
            SELECT * FROM medical_reports WHERE user_id = $1 ORDER BY uploaded_at DESC
        """, int(current_user))
        
        return {"reports": [dict(report) for report in reports]}
    finally:
        await release_db(conn)

@router.delete("/reports/{report_id}")
async def delete_medical_report(
    report_id: int,
    current_user: str = Depends(get_current_user)
):
    """Delete medical report"""
    conn = await get_db()
    try:
        await conn.execute(
            "DELETE FROM medical_reports WHERE id = $1 AND user_id = $2",
            report_id, int(current_user)
        )
        
        return {"message": "Report deleted successfully"}
    finally:
        await release_db(conn)
