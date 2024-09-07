import datetime
import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from dependency_injector.wiring import inject, Provide
import logging
from app.dao.dao import delete_resume_from_database
from app.containers import Container
from app.services.resume_processor import ResumeProcessor

logger = logging.getLogger(__name__)

router = APIRouter()
@router.post("/")
@inject
async def upload_resume(
    file: UploadFile = File(...),
    resume_processor: ResumeProcessor = Depends(Provide[Container.resume_processor])
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        await resume_processor.initialize()
        filename = file.filename

        content = await file.read()

        success = await resume_processor.chunk_and_embed_and_store_resume_to_db(content, filename)

        if success:
            return {
                "message": "Resume processed successfully",
                "original_filename": filename
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to process the resume")

    except Exception as e:
        logger.error(f"Error processing resume upload: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the resume")
    

@router.get("/")
@inject
async def get_all_resumes(resume_processor: ResumeProcessor = Depends(Provide[Container.resume_processor])):
    try:
        resumes = await resume_processor.get_all_resumes()
        return resumes
    except Exception as e:
        logger.error(f"Error retrieving resumes: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving resumes")


@router.delete("/{id}")
@inject
async def delete_resume(file_name: str,resume_processor: ResumeProcessor = Depends(Provide[Container.resume_processor])):
    try:
        # Delete resume from database and get list of FAISS indices to remove
        index_list = await delete_resume_from_database(file_name)

        # Check if any embeddings were returned
        if not index_list:
            raise HTTPException(status_code=404, detail="Resume not found in the database")

        # Delete the corresponding embeddings from the FAISS index
        await resume_processor.delete_elements_from_index(index_list)

        # Return a success message
        return {"message": f"Resume '{file_name}' and associated embeddings successfully deleted."}

    except Exception as e:
        # Log the error (you could use logger instead of print in production)
        logger.error(f"Error deleting resume '{file_name}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred while deleting the resume: {str(e)}")


# @router.delete("")
# async def delete_resume():
#     if file.content_type != "application/pdf":
#         raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
#     file_name = file.name 

#     try:
#         # Delete resume from database and get list of FAISS indices to remove
#         index_list = await delete_resume_from_database(file_name)

#         # Check if any embeddings were returned
#         if not index_list:
#             raise HTTPException(status_code=404, detail="Resume not found in the database")

#         # Delete the corresponding embeddings from the FAISS index
#         await resume_processor.delete_elements_from_index(index_list)

#         # Return a success message
#         return {"message": f"Resume '{file_name}' and associated embeddings successfully deleted."}

#     except Exception as e:
#         # Log the error (you could use logger instead of print in production)
#         logger.error(f"Error deleting resume '{file_name}': {str(e)}")
#         raise HTTPException(status_code=500, detail=f"An error occurred while deleting the resume: {str(e)}")
