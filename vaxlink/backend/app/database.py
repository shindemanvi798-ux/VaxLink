from datetime import date, datetime, timedelta
from typing import Dict, List, Optional
import uuid

from app.models import (
    User, Family, Child, DoseRecord, Camp, CampSlot, Booking, BookingResponse, ChildCreate
)
from app.services.crowd_service import calculate_crowd_status

# Deterministic Seed Data
DEMO_USER = User(
    id="usr_demo_001",
    role="parent",
    phone="+91 98765 43210",
    full_name="Priya Sharma",
    preferred_lang="hi",
    area="Shivaji Nagar, Pune"
)

DEMO_FAMILY = Family(
    id="fam_demo_001",
    primary_phone="+91 98765 43210",
    consent_given_at=datetime.now(),
    consent_version="1.0"
)

# Seed Children
# Child 1: Aarav (Infant, 8 months old - DOB ~8 months ago)
# Has completed birth & 6-wk/10-wk doses, Penta-3 & OPV-3 currently DUE today!
today = date.today()

child_1_dob = today - timedelta(days=240) # ~8 months ago
CHILD_1 = Child(
    id="child_001",
    family_id="fam_demo_001",
    name="Aarav Sharma",
    dob=child_1_dob,
    created_at=datetime.now() - timedelta(days=240)
)

# Child 2: Ananya (Newborn, 10 days old)
# Needs BCG, OPV-0, Hep B
child_2_dob = today - timedelta(days=10)
CHILD_2 = Child(
    id="child_002",
    family_id="fam_demo_001",
    name="Ananya Sharma",
    dob=child_2_dob,
    created_at=datetime.now() - timedelta(days=10)
)

# In-Memory Database Stores
children_db: Dict[str, Child] = {
    CHILD_1.id: CHILD_1,
    CHILD_2.id: CHILD_2,
}

# Dose records for Child 1 (Aarav)
dose_records_db: Dict[str, List[DoseRecord]] = {
    CHILD_1.id: [
        DoseRecord(id="dr_1", child_id=CHILD_1.id, vaccine_code="BCG", status="done", administered_date=child_1_dob, created_at=datetime.now()),
        DoseRecord(id="dr_2", child_id=CHILD_1.id, vaccine_code="OPV_0", status="done", administered_date=child_1_dob, created_at=datetime.now()),
        DoseRecord(id="dr_3", child_id=CHILD_1.id, vaccine_code="HEP_B_0", status="done", administered_date=child_1_dob, created_at=datetime.now()),
        DoseRecord(id="dr_4", child_id=CHILD_1.id, vaccine_code="OPV_1", status="done", administered_date=child_1_dob + timedelta(days=42), created_at=datetime.now()),
        DoseRecord(id="dr_5", child_id=CHILD_1.id, vaccine_code="PENTA_1", status="done", administered_date=child_1_dob + timedelta(days=42), created_at=datetime.now()),
        DoseRecord(id="dr_6", child_id=CHILD_1.id, vaccine_code="ROTA_1", status="done", administered_date=child_1_dob + timedelta(days=42), created_at=datetime.now()),
        DoseRecord(id="dr_7", child_id=CHILD_1.id, vaccine_code="OPV_2", status="done", administered_date=child_1_dob + timedelta(days=70), created_at=datetime.now()),
        DoseRecord(id="dr_8", child_id=CHILD_1.id, vaccine_code="PENTA_2", status="done", administered_date=child_1_dob + timedelta(days=70), created_at=datetime.now()),
        DoseRecord(id="dr_9", child_id=CHILD_1.id, vaccine_code="ROTA_2", status="done", administered_date=child_1_dob + timedelta(days=70), created_at=datetime.now()),
    ],
    CHILD_2.id: [] # Newborn - birth doses due
}

# Camps Data
# Camp 1: Shivaji Nagar PHC (LOW Crowd - 10/40 booked = 25%)
# Camp 2: Aundh Urban Health Center (MEDIUM Crowd - 26/40 booked = 65%)
# Camp 3: Hadapsar Community Health Camp (HIGH Crowd - 38/40 booked = 95%)

camp_1_slots = [
    CampSlot(id="slot_c1_1", camp_id="camp_001", time_range="09:00 - 10:30 AM", capacity=15, booked_count=4, available_slots=11),
    CampSlot(id="slot_c1_2", camp_id="camp_001", time_range="10:30 - 12:00 PM", capacity=15, booked_count=4, available_slots=11),
    CampSlot(id="slot_c1_3", camp_id="camp_001", time_range="12:00 - 01:30 PM", capacity=10, booked_count=2, available_slots=8),
]

camp_2_slots = [
    CampSlot(id="slot_c2_1", camp_id="camp_002", time_range="09:00 - 10:30 AM", capacity=15, booked_count=12, available_slots=3),
    CampSlot(id="slot_c2_2", camp_id="camp_002", time_range="10:30 - 12:00 PM", capacity=15, booked_count=10, available_slots=5),
    CampSlot(id="slot_c2_3", camp_id="camp_002", time_range="01:00 - 02:30 PM", capacity=10, booked_count=4, available_slots=6),
]

camp_3_slots = [
    CampSlot(id="slot_c3_1", camp_id="camp_003", time_range="09:00 - 10:30 AM", capacity=15, booked_count=15, available_slots=0),
    CampSlot(id="slot_c3_2", camp_id="camp_003", time_range="10:30 - 12:00 PM", capacity=15, booked_count=14, available_slots=1),
    CampSlot(id="slot_c3_3", camp_id="camp_003", time_range="01:00 - 02:30 PM", capacity=10, booked_count=9, available_slots=1),
]

camps_db: Dict[str, Camp] = {
    "camp_001": Camp(
        id="camp_001",
        name="Shivaji Nagar Primary Health Center (PHC)",
        location="Near Bus Depot, Shivaji Nagar, Pune",
        area="Shivaji Nagar",
        date=today + timedelta(days=1),
        created_by="District Health Office",
        crowd_status="LOW",
        total_capacity=40,
        total_booked=10,
        slots=camp_1_slots
    ),
    "camp_002": Camp(
        id="camp_002",
        name="Aundh Urban Health Center",
        location="Sector 4, Parihar Chowk, Aundh, Pune",
        area="Aundh",
        date=today + timedelta(days=1),
        created_by="Municipal Health Corp",
        crowd_status="MEDIUM",
        total_capacity=40,
        total_booked=26,
        slots=camp_2_slots
    ),
    "camp_003": Camp(
        id="camp_003",
        name="Hadapsar Community Health Camp",
        location="Gram Panchayat Hall, Main Road, Hadapsar, Pune",
        area="Hadapsar",
        date=today + timedelta(days=2),
        created_by="District Health Office",
        crowd_status="HIGH",
        total_capacity=40,
        total_booked=38,
        slots=camp_3_slots
    )
}

bookings_db: Dict[str, Booking] = {}

# Repository Functions
def get_all_children() -> List[Child]:
    return list(children_db.values())

def get_child_by_id(child_id: str) -> Optional[Child]:
    return children_db.get(child_id)

def create_child(data: ChildCreate) -> Child:
    child_id = f"child_{uuid.uuid4().hex[:6]}"
    new_child = Child(
        id=child_id,
        family_id=data.family_id or "fam_demo_001",
        name=data.name,
        dob=data.dob,
        created_at=datetime.now()
    )
    children_db[child_id] = new_child
    dose_records_db[child_id] = []
    return new_child

def get_child_dose_records(child_id: str) -> List[DoseRecord]:
    return dose_records_db.get(child_id, [])

def get_all_camps() -> List[Camp]:
    # Update crowd status dynamically
    for camp in camps_db.values():
        camp.crowd_status = calculate_crowd_status(camp.total_booked, camp.total_capacity)
    return list(camps_db.values())

def get_camp_by_id(camp_id: str) -> Optional[Camp]:
    camp = camps_db.get(camp_id)
    if camp:
        camp.crowd_status = calculate_crowd_status(camp.total_booked, camp.total_capacity)
    return camp

def book_camp_slot(camp_id: str, slot_id: str, child_id: str, family_id: str = "fam_demo_001") -> BookingResponse:
    camp = camps_db.get(camp_id)
    if not camp:
        raise ValueError("Vaccination camp not found.")

    target_slot: Optional[CampSlot] = None
    for s in camp.slots:
        if s.id == slot_id:
            target_slot = s
            break

    if not target_slot:
        raise ValueError("Selected time slot not found.")

    if target_slot.available_slots <= 0:
        raise ValueError("Selected slot is fully booked. Please select another slot.")

    child = children_db.get(child_id)
    if not child:
        raise ValueError("Child profile not found.")

    # Perform booking mutation safely
    booking_id = f"bk_{uuid.uuid4().hex[:8]}"
    ref_code = f"VX-{uuid.uuid4().hex[:6].upper()}"

    target_slot.booked_count += 1
    target_slot.available_slots -= 1
    camp.total_booked += 1
    camp.crowd_status = calculate_crowd_status(camp.total_booked, camp.total_capacity)

    booking_obj = Booking(
        id=booking_id,
        camp_slot_id=slot_id,
        family_id=family_id,
        created_at=datetime.now()
    )
    bookings_db[booking_id] = booking_obj

    return BookingResponse(
        booking_id=booking_id,
        reference_code=ref_code,
        child_id=child.id,
        child_name=child.name,
        camp_id=camp.id,
        camp_name=camp.name,
        camp_location=camp.location,
        date=camp.date,
        time_slot=target_slot.time_range,
        created_at=datetime.now(),
        status="CONFIRMED"
    )
