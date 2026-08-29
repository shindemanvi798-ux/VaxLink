from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime

class User(BaseModel):
    id: str
    role: str = "parent"  # parent | health_worker | admin
    phone: str
    full_name: str
    preferred_lang: str = "en"
    area: str

class Family(BaseModel):
    id: str
    primary_phone: str
    consent_given_at: Optional[datetime] = None
    consent_version: str = "1.0"

class ChildCreate(BaseModel):
    name: str = Field(..., min_length=1, example="Aarav")
    dob: date = Field(..., example="2025-12-15")
    gender: Optional[str] = "unspecified"
    family_id: Optional[str] = "fam_demo_001"

class Child(BaseModel):
    id: str
    family_id: str
    name: str
    dob: date
    created_at: datetime

class VaccineScheduleReference(BaseModel):
    vaccine_code: str
    name: str
    description: str
    due_days_after_birth: int
    due_timing_label: str # e.g. "At Birth", "6 Weeks", "10 Weeks", "14 Weeks", "9 Months"
    dose_number: int
    category: str = "essential"

class DoseRecord(BaseModel):
    id: str
    child_id: str
    vaccine_code: str
    status: str  # due | done | missed
    administered_date: Optional[date] = None
    administered_by: Optional[str] = None
    created_at: datetime

class CalculatedDose(BaseModel):
    vaccine_code: str
    name: str
    description: str
    due_timing_label: str
    due_date: date
    status: str # done | due | missed | upcoming
    administered_date: Optional[date] = None

class ScheduleResponse(BaseModel):
    child_id: str
    child_name: str
    dob: date
    age_months: int
    progress_percentage: int
    next_vaccine: Optional[CalculatedDose] = None
    doses: List[CalculatedDose]

class CampSlot(BaseModel):
    id: str
    camp_id: str
    time_range: str # e.g. "09:00 - 10:00"
    capacity: int
    booked_count: int
    available_slots: int

class Camp(BaseModel):
    id: str
    name: str
    location: str
    area: str
    date: date
    created_by: str = "health_dept"
    crowd_status: str # LOW | MEDIUM | HIGH
    total_capacity: int
    total_booked: int
    slots: List[CampSlot] = []

class Booking(BaseModel):
    id: str
    camp_slot_id: str
    family_id: str
    created_at: datetime

class BookingRequest(BaseModel):
    child_id: str
    family_id: Optional[str] = "fam_demo_001"

class BookingResponse(BaseModel):
    booking_id: str
    reference_code: str
    child_id: str
    child_name: str
    camp_id: str
    camp_name: str
    camp_location: str
    date: date
    time_slot: str
    created_at: datetime
    status: str = "CONFIRMED"
