from fastapi import APIRouter, HTTPException, Depends
from app.schemas.ticket import TicketCreate, TicketResponse
from app.services.ml_service import ml_service

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.ticket import Ticket

router = APIRouter()

@router.post("/analyze", response_model=TicketResponse)
async def analyze_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    if not ml_service.model:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    result = ml_service.predict(ticket.title, ticket.description)
    if not result:
         raise HTTPException(status_code=500, detail="Prediction failed")

    # Persist to Database
    db_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        category=result["category"],
        priority=result["priority"],
        confidence=result["confidence"]
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)

    return TicketResponse(**result)
