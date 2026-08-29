from fastapi import APIRouter, HTTPException
from typing import List
from app.models import Camp, CampSlot
from app.database import get_all_camps, get_camp_by_id

router = APIRouter(prefix="/camps", tags=["Camps"])

@router.get("", response_model=List[Camp])
def list_camps():
    """Retrieve all upcoming vaccination camps with crowd status."""
    return get_all_camps()

@router.get("/{camp_id}", response_model=Camp)
def get_camp(camp_id: str):
    """Get camp details including time slots and crowd level."""
    camp = get_camp_by_id(camp_id)
    if not camp:
        raise HTTPException(status_code=404, detail="Vaccination camp not found.")
    return camp

@router.get("/{camp_id}/slots", response_model=List[CampSlot])
def get_camp_slots(camp_id: str):
    """Get available time slots for a specific camp."""
    camp = get_camp_by_id(camp_id)
    if not camp:
        raise HTTPException(status_code=404, detail="Vaccination camp not found.")
    return camp.slots
