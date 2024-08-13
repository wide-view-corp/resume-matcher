from fastapi import FastAPI
from app.api.endpoints import router as main_router
from app.api.resume_endpoints import router as resume_router
from app.api.chat_endpoints import router as chat_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.dao.database import init_db
from app.services.resume_processor import resume_processor

setup_logging()

app = FastAPI(title=settings.APP_NAME)

app.include_router(main_router)
app.include_router(resume_router, prefix="/resume", tags=["resume"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_faiss_optimizer())
    await init_db()
    await resume_processor.load_index()

@app.on_event("shutdown")
async def shutdown_event():
    # You can add any cleanup logic here
    pass