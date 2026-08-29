from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime

class ChildCreate(BaseModel):
    name: str = Field(..., description="Full name of the child")
    dob: date = Field(..., description="Date of birth in YYYY-MM-DD format")
    # Note: We do NOT pass family_id here. The backend will securely determine the 
    # family_id based on the authenticated user making the request.

class ChildResponse(BaseModel):
    id: str
    family_id: str
    name: str
    dob: date
    created_at: datetime

class DoseRecordUpdate(BaseModel):
    status: str = Field(..., description="Must be 'due', 'done', or 'missed'")
    administered_date: Optional[date] = None
    # We do NOT let the frontend say who administered it. 
    # The backend will automatically set 'administered_by' to the logged-in user's ID if they are an ASHA.

class DoseRecordResponse(BaseModel):
    id: str
    child_id: str
    vaccine_code: str
    status: str
    administered_date: Optional[date]
    administered_by: Optional[str]
    created_at: datetime

class ScheduleStatusResponse(BaseModel):
    child: ChildResponse
    doses: List[DoseRecordResponse]
    # In a full implementation, you'd also include the static vaccine info here (names in different languages)
