from fastapi import APIRouter

from api.src.v1.endpoints import healthcheck


api_router = APIRouter()

api_router.include_router(healthcheck.router, prefix="/healthcheck", tags=["Healthcheck"])
