from fastapi import APIRouter
import random

router = APIRouter()

@router.get("/stats")
async def get_stats():
    # Mock data for dashboard
    # TODO: Connect to real database stats
    return {
        "tickets_resolved_today": random.randint(10, 50),
        "active_tickets": random.randint(5, 20),
        "avg_response_time": f"{random.randint(5, 15)} mins"
    }
