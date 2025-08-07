from fastapi import FastAPI, APIRouter
from src.settings import settings


def apply_routes(app: FastAPI) -> FastAPI:
    # Create main router
    router = APIRouter(prefix=settings.api.prefix)
    # Include API routers
    # Include main router
    app.include_router(router)
    return app
