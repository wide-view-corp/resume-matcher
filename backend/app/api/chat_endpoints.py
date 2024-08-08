# app/api/chat_endpoints.py
from fastapi import APIRouter, Depends
from app.services.chatbot import chatbot_service
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str
    suggested_resumes: list

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    result = await chatbot_service.process_query(request.query)
    return ChatResponse(**result)