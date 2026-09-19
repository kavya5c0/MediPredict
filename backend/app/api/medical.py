from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from typing import Optional
from app.core.database import medical_reports_collection
from app.core.security import get_current_user
from bson import ObjectId
from datetime import datetime
import aiofiles
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Try to initialize the medical analyzer (optional dependency)
analyzer = None
try:
    from app.services.medical_report_analyzer import MedicalReportAnalyzer
    analyzer = MedicalReportAnalyzer()
    logger.info("Medical analyzer initialized successfully")
except ImportError as e:
    logger.warning(f"Medical analyzer dependencies not available: {e}")
    logger.warning("Medical analysis will use basic text processing")
except Exception as e:
    logger.warning(f"Medical analyzer initialization failed: {e}")
    logger.warning("Medical analysis will use basic text processing")

@router.post("/upload")
async def upload_medical_report(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user)
):
    """Upload and analyze medical report"""
    if medical_reports_collection is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available. Please ensure MongoDB is running."
        )
    
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
    
    # Use timestamp to avoid filename conflicts
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{current_user}_{timestamp}_{file.filename}"
    file_path = os.path.join(upload_dir, safe_filename)
    
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
    except Exception as e:
        logger.error(f"Failed to save file: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Analyze report
    try:
        if analyzer:
            analysis = analyzer.analyze_report(image_path=file_path)
        else:
            analysis = {
                "note": "Medical analyzer not available due to missing dependencies",
                "summary": "File uploaded successfully but analysis unavailable",
                "recommendations": ["Install OCR dependencies for full analysis"],
                "medical_entities": {"diseases": [], "medications": [], "symptoms": [], "lab_values": [], "vitals": []}
            }
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        analysis = {
            "error": f"Analysis failed: {str(e)}",
            "summary": "File uploaded but analysis encountered an error",
            "recommendations": [],
            "medical_entities": {"diseases": [], "medications": [], "symptoms": [], "lab_values": [], "vitals": []}
        }
    
    # Save to database
    report_data = {
        "user_id": current_user,
        "filename": file.filename,
        "file_path": file_path,
        "analysis": analysis,
        "uploaded_at": datetime.utcnow()
    }
    
    try:
        result = await medical_reports_collection.insert_one(report_data)
        return {
            "report_id": str(result.inserted_id),
            "filename": file.filename,
            "analysis": analysis
        }
    except Exception as e:
        logger.error(f"Failed to save report to database: {e}")
        # File is saved, just DB insert failed
        return {
            "report_id": "local_only",
            "filename": file.filename,
            "analysis": analysis,
            "warning": "Report analysis complete but not saved to database"
        }

@router.post("/analyze/text")
async def analyze_medical_text(
    text_data: dict,
    current_user: str = Depends(get_current_user)
):
    """Analyze medical text directly"""
    if medical_reports_collection is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available. Please ensure MongoDB is running."
        )
    
    text = text_data.get("text", "")
    
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")
    
    if analyzer:
        analysis = analyzer.analyze_report(text=text)
    else:
        analysis = {"note": "Medical analyzer not available due to missing dependencies"}
    
    # Save to database
    report_data = {
        "user_id": current_user,
        "text_input": text,
        "analysis": analysis,
        "analyzed_at": datetime.utcnow()
    }
    
    result = await medical_reports_collection.insert_one(report_data)
    
    return {
        "report_id": str(result.inserted_id),
        "analysis": analysis
    }

@router.get("/reports")
async def get_medical_reports(
    current_user: str = Depends(get_current_user)
):
    """Get all medical reports for user"""
    if medical_reports_collection is None:
        return {"reports": []}
    
    reports = await medical_reports_collection.find(
        {"user_id": current_user}
    ).to_list(length=100)
    
    for report in reports:
        report["_id"] = str(report["_id"])
    
    return {"reports": reports}

@router.get("/reports/{report_id}")
async def get_medical_report(
    report_id: str,
    current_user: str = Depends(get_current_user)
):
    """Get specific medical report"""
    if medical_reports_collection is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available. Please ensure MongoDB is running."
        )
    
    report = await medical_reports_collection.find_one({
        "_id": ObjectId(report_id),
        "user_id": current_user
    })
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    report["_id"] = str(report["_id"])
    
    return report
