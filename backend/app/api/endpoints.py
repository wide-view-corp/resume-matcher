from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.llm import llm
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str
    max_length: int = 100
    use_rag: bool = False

class LLMResponse(BaseModel):
    response: str



@router.post("/generate", response_model=LLMResponse)
async def generate_text(request: PromptRequest):
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    try:
        response = await llm.generate_response(request.prompt, request.max_length, request.use_rag)
        return LLMResponse(response=response)
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request")