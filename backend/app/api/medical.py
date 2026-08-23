from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from typing import Optional
from app.core.database import medical_reports_collection
from app.core.security import get_current_user
from bson import ObjectId
from datetime import datetime
import aiofiles
import os

router = APIRouter()

# Try to initialize the medical analyzer (optional dependency)
analyzer = None
try:
    from app.services.medical_report_analyzer import MedicalReportAnalyzer
    analyzer = MedicalReportAnalyzer()
    print("Medical analyzer initialized successfully")
except ImportError as e:
    print(f"Medical analyzer dependencies not available: {e}")
    print("Medical analysis will use basic text processing")
except Exception as e:
    print(f"Medical analyzer initialization failed: {e}")
    print("Medical analysis will use basic text processing")

@router.post("/upload")
async def upload_medical_report(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user)
):
    """Upload and analyze medical report"""
    # Save uploaded file
    upload_dir = "uploads/medical_reports"
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = f"{upload_dir}/{current_user}_{file.filename}"
    
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    # Analyze report
    try:
        if analyzer:
            analysis = analyzer.analyze_report(image_path=file_path)
        else:
            analysis = {"note": "Medical analyzer not available due to missing dependencies"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    
    # Save to database
    report_data = {
        "user_id": current_user,
        "filename": file.filename,
        "file_path": file_path,
        "analysis": analysis,
        "uploaded_at": datetime.utcnow()
    }
    
    result = await medical_reports_collection.insert_one(report_data)
    
    return {
        "report_id": str(result.inserted_id),
        "analysis": analysis
    }

@router.post("/analyze/text")
async def analyze_medical_text(
    text_data: dict,
    current_user: str = Depends(get_current_user)
):
    """Analyze medical text directly"""
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
    report = await medical_reports_collection.find_one({
        "_id": ObjectId(report_id),
        "user_id": current_user
    })
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    report["_id"] = str(report["_id"])
    
    return report
