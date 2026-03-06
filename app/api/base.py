from fastapi import APIRouter

from app.api.v1.tickets import router as tickets_router
from app.core.settings import settings

api_router = APIRouter(prefix=settings.API_BASE_PREFIX)
api_router.include_router(router=tickets_router, prefix="/tickets")
