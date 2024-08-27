from fastapi import APIRouter, UploadFile, File, HTTPException
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# This will be set in the main file
resume_processor = None

@router.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    content = await file.read()
    file_name = file.name
    if await resume_processor.chunk_and_embed_and_store_resume_to_db(content, file_name):
        return {"message": "Resume processed successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to process the resume")
    
# Delete resume function to be added