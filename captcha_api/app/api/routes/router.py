from fastapi import APIRouter
from app.api.routes import heartbeat, prediction

api_router = APIRouter()
api_router.include_router(heartbeat.router, tags=["health"], prefix="/v1")
api_router.include_router(
    prediction.router,
    tags=["prediction"],
    prefix="/v1/model"
)
