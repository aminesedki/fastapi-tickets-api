from fastapi import APIRouter

from api.v1.tickets import router as tickets_router
from core.settings import settings

api_router = APIRouter(prefix=settings.API_BASE_PREFIX)
api_router.include_router(router=tickets_router, prefix="/tickets")
