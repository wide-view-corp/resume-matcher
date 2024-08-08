from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.resume_processor import resume_processor
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    content = await file.read()
    if await resume_processor.process_pdf(content):
        return {"message": "Resume processed successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to process the resume")