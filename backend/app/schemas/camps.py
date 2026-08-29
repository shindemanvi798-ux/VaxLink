from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, time, datetime

class CampSlotResponse(BaseModel):
    id: str
    time_range: str = Field(..., description="e.g., '09:00-11:00'")
    capacity: int
    booked_count: int
    
class CampResponse(BaseModel):
    id: str
    area: str
    date: date
    slots: List[CampSlotResponse] = []
    
class BookingCreate(BaseModel):
    # The frontend only needs to send which slot they want and for which child.
    # The backend determines the family_id from the auth token.
    child_id: str
    
class BookingResponse(BaseModel):
    id: str
    camp_slot_id: str
    family_id: str
    child_id: str
    created_at: datetime
