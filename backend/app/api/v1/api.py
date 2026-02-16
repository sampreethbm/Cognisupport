from fastapi import APIRouter
from app.api.v1.routers import ticketing, analytics

api_router = APIRouter()
api_router.include_router(ticketing.router, prefix="/tickets", tags=["tickets"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
