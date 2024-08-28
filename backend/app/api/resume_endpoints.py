from fastapi import APIRouter, UploadFile, File, HTTPException
import logging
from app.dao.dao import delete_resume_from_database

logger = logging.getLogger(__name__)

router = APIRouter()

# This will be set in the main file
resume_processor = None

@router.post("/documents")
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    content = await file.read()
    file_name = file.name
    if await resume_processor.chunk_and_embed_and_store_resume_to_db(content, file_name):
        return {"message": "Resume processed successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to process the resume")
    

@router.get("/documents")
async def get_all_resumes():
    resumes = await resume_processor.get_all_resumes()
    return resumes


@router.delete("/documents/{file_name}")
async def delete_resume(file_name: str):
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
