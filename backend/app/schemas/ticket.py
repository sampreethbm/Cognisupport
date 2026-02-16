from pydantic import BaseModel

class TicketBase(BaseModel):
    title: str
    description: str

class TicketCreate(TicketBase):
    pass

class TicketResponse(BaseModel):
    category: str
    priority: str
    confidence: str
    
    class Config:
        from_attributes = True
