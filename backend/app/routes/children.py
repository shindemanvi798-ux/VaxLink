from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models import Child, ChildCreate, ScheduleResponse, CalculatedDose
from app.database import (
    get_all_children, get_child_by_id, create_child, get_child_dose_records
)
from app.services.schedule_service import generate_child_schedule, calculate_age_months

router = APIRouter(prefix="/children", tags=["Children"])

@router.get("", response_model=List[Child])
def list_children():
    """Retrieve all children for the active family/demo profile."""
    return get_all_children()

@router.post("", response_model=Child, status_code=status.HTTP_201_CREATED)
def add_child(data: ChildCreate):
    """Add a new child profile."""
    if not data.name or len(data.name.strip()) == 0:
        raise HTTPException(status_code=400, detail="Child name cannot be empty.")
    
    return create_child(data)

@router.get("/{child_id}", response_model=Child)
def get_child(child_id: str):
    """Get details of a specific child."""
    child = get_child_by_id(child_id)
    if not child:
        raise HTTPException(status_code=404, detail="Child profile not found.")
    return child

@router.get("/{child_id}/schedule", response_model=ScheduleResponse)
def get_child_schedule(child_id: str):
    """
    Get calculated vaccination schedule for a child based on DOB and completed dose records.
    Returns calculated due dates, status (done|due|missed|upcoming), progress %, and next due vaccine.
    """
    child = get_child_by_id(child_id)
    if not child:
        raise HTTPException(status_code=404, detail="Child profile not found.")

    records = get_child_dose_records(child_id)
    doses, progress_pct, next_vaccine = generate_child_schedule(child.dob, records)
    age_m = calculate_age_months(child.dob)

    return ScheduleResponse(
        child_id=child.id,
        child_name=child.name,
        dob=child.dob,
        age_months=age_m,
        progress_percentage=progress_pct,
        next_vaccine=next_vaccine,
        doses=doses
    )
