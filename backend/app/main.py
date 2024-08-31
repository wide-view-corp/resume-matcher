from fastapi import FastAPI
from app.api.chat_endpoint import router as chat_router
from app.api.resume_endpoints import router as resume_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.dao.database import init_db
from dependency_injector.wiring import inject, Provide
from app.containers import Container

import logging

setup_logging()
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[
        "app.api.chat_endpoint",
        "app.api.resume_endpoints"
    ])

    app = FastAPI(title=settings.APP_NAME)
    app.container = container
    app.include_router(chat_router, prefix="/chatbot", tags=["chatbot"])
    app.include_router(resume_router, prefix="/resume", tags=["resume"])

    return app

app = create_app()

@app.on_event("startup")
async def startup_event():
    #asyncio.create_task(start_faiss_optimizer())
    await init_db()
    # Ensure that the index is correctly initialized by awaiting the index setup
    # resume_processor.index = await resume_processor.index

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Conversation history cleared on shutdown.")