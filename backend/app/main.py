from fastapi import FastAPI
from app.api.endpoints import router as main_router
from app.api.resume_endpoints import router as resume_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.dao.database import init_db
from app.services.resume_processor import resume_processor
from app.services.llm import llm 
import logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.APP_NAME)

app.include_router(main_router)
app.include_router(resume_router, prefix="/resume", tags=["resume"])

@app.on_event("startup")
async def startup_event():
    #asyncio.create_task(start_faiss_optimizer())
    await init_db()
    await resume_processor.load_or_create_index()

@app.on_event("shutdown")
async def shutdown_event():
    # Clean the conversation history
    llm.conversation_history = ""
    logger.info("Conversation history cleared on shutdown.")
    pass