from fastapi import FastAPI
from app.api.chat_endpoint import router as chat_router
from app.api.resume_endpoints import router as resume_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.dao.database import init_db
from app.services.resume_processor import ResumeProcessor
from app.services.llm import llm 
import logging

setup_logging()
logger = logging.getLogger(__name__)


# Initialize ResumeProcessor instance
resume_processor = ResumeProcessor()

app = FastAPI(title=settings.APP_NAME)

app.include_router(chat_router)
app.include_router(resume_router, prefix="/resume", tags=["resume"])


# Pass the resume_processor instance to the router
resume_router.resume_processor = resume_processor

@app.on_event("startup")
async def startup_event():
    #asyncio.create_task(start_faiss_optimizer())
    await init_db()
    # Ensure that the index is correctly initialized by awaiting the index setup
    resume_processor.index = await resume_processor.index

@app.on_event("shutdown")
async def shutdown_event():
    # Clean the conversation history
    llm.conversation_history = ""
    logger.info("Conversation history cleared on shutdown.")
    pass