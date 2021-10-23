from fastapi import APIRouter

from app.api.endpoints import home, recommendation


api_router = APIRouter()
api_router.include_router(home.router, tags=['home'])
api_router.include_router(recommendation.router, tags=['recommendation'])
