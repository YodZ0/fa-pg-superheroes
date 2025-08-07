from fastapi import FastAPI, APIRouter
from src.settings import settings

from src.apps.superheroes.router import router as superheroes_router


def apply_routes(app: FastAPI) -> FastAPI:
    # Create main router
    router = APIRouter(prefix=settings.api.prefix)
    # Include API routers
    router.include_router(superheroes_router)
    # Include main router
    app.include_router(router)
    return app
