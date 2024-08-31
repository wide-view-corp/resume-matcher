from fastapi import APIRouter, HTTPException, Depends
from dependency_injector.wiring import inject, Provide
from pydantic import BaseModel
from typing import List, Dict
import logging
from app.services.llm import LLM
from app.services.resume_processor import ResumeProcessor

logger = logging.getLogger(__name__)

router = APIRouter()

class ChatMessageRequest(BaseModel):
    message: str
    max_response_length: int = 200
    use_contextual_search: bool = False

class ChatMessageResponse(BaseModel):
    message: str

class ConversationHistoryResponse(BaseModel):
    history: List[Dict[str, str]]

@router.post("/chatbot/message", response_model=ChatMessageResponse)
@inject
async def generate_chat_response(
    request: ChatMessageRequest,
    llm: LLM = Depends(Provide[Container.llm]),
    resume_processor: ResumeProcessor = Depends(Provide[Container.resume_processor])
):
    if not request.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        context = await resume_processor.get_relevant_context(request.message)
        response = await llm.generate_response(
            prompt=request.message,
            use_rag=True,
            context=context
        )
        return ChatMessageResponse(message=response)
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request")

@router.get("/chatbot/history", response_model=ConversationHistoryResponse)
@inject
async def get_chat_history(llm: LLM = Depends(Provide[Container.llm])):
    history = llm.get_conversation_history()
    return ConversationHistoryResponse(history=history)