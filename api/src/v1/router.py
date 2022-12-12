from fastapi import APIRouter

from api.src.v1.endpoints import healthcheck
from api.src.v1.endpoints import predictions


api_router = APIRouter()

api_router.include_router(healthcheck.router, prefix="/healthcheck", tags=["Healthcheck"])
api_router.include_router(predictions.router, prefix="/predictions", tags=["Predictions"])
