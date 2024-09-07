import os
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
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

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Your API Title",
        version="1.0.0",
        description="Your API description",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[
        "app.api.chat_endpoint",
        "app.api.resume_endpoints"
    ])

    app = FastAPI(title=settings.APP_NAME, docs_url=None, redoc_url=None)

    app.container = container
    app.include_router(chat_router, prefix="/chatbot", tags=["chatbot"])
    app.include_router(resume_router, prefix="/resumes", tags=["resumes"])

    app.openapi = custom_openapi

    @app.get("/api", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url="/openapi.json",
            title=f"{settings.APP_NAME} - Swagger UI",
            swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
            swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
        )

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


