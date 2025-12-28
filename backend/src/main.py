from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .api import auth, tasks
from .core.database import create_db_and_tables
from .core.config import settings
from .core.logging_config import setup_logging


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    # Set up logging
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Allow Next.js dev server
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_origin_regex=r"https?://localhost(:[0-9]+)?|https?://127\.0\.0\.1(:[0-9]+)?"
    )

    # Include API routes
    app.include_router(auth.router)
    app.include_router(tasks.router)

    # Create database tables on startup
    @app.on_event("startup")
    def on_startup():
        create_db_and_tables()

    # Health check endpoint
    @app.get("/health")
    def health_check():
        return {"status": "healthy", "version": settings.app_version}

    return app


# Create the main application instance
app = create_app()


# For running with uvicorn directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)