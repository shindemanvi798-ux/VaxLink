from datetime import date, timedelta
from typing import List, Dict, Tuple, Optional
from app.models import VaccineScheduleReference, DoseRecord, CalculatedDose, ScheduleResponse

# Central Universal Immunization Programme (UIP) reference schedule for India
VACCINE_REFERENCE_SCHEDULE: List[VaccineScheduleReference] = [
    VaccineScheduleReference(
        vaccine_code="BCG",
        name="BCG",
        description="Protects against Tuberculosis (TB). Administered at birth.",
        due_days_after_birth=0,
        due_timing_label="At Birth",
        dose_number=1
    ),
    VaccineScheduleReference(
        vaccine_code="OPV_0",
        name="OPV-0",
        description="Oral Polio Vaccine birth dose.",
        due_days_after_birth=0,
        due_timing_label="At Birth",
        dose_number=1
    ),
    VaccineScheduleReference(
        vaccine_code="HEP_B_0",
        name="Hepatitis B Birth Dose",
        description="Prevents Hepatitis B infection. Given within 24 hours of birth.",
        due_days_after_birth=0,
        due_timing_label="At Birth",
        dose_number=1
    ),
    VaccineScheduleReference(
        vaccine_code="OPV_1",
        name="OPV-1",
        description="Oral Polio Vaccine 1st dose.",
        due_days_after_birth=42, # 6 weeks
        due_timing_label="6 Weeks",
        dose_number=1
    ),
    VaccineScheduleReference(
        vaccine_code="PENTA_1",
        name="Pentavalent-1",
        description="Protects against Diphtheria, Pertussis, Tetanus, Hep B, and Hib.",
        due_days_after_birth=42,
        due_timing_label="6 Weeks",
        dose_number=1
    ),
    VaccineScheduleReference(
        vaccine_code="ROTA_1",
        name="Rotavirus-1",
        description="Protects against severe rotavirus diarrhea.",
        due_days_after_birth=42,
        due_timing_label="6 Weeks",
        dose_number=1
    ),
    VaccineScheduleReference(
        vaccine_code="OPV_2",
        name="OPV-2",
        description="Oral Polio Vaccine 2nd dose.",
        due_days_after_birth=70, # 10 weeks
        due_timing_label="10 Weeks",
        dose_number=2
    ),
    VaccineScheduleReference(
        vaccine_code="PENTA_2",
        name="Pentavalent-2",
        description="Pentavalent 2nd dose.",
        due_days_after_birth=70,
        due_timing_label="10 Weeks",
        dose_number=2
    ),
    VaccineScheduleReference(
        vaccine_code="ROTA_2",
        name="Rotavirus-2",
        description="Rotavirus 2nd dose.",
        due_days_after_birth=70,
        due_timing_label="10 Weeks",
        dose_number=2
    ),
    VaccineScheduleReference(
        vaccine_code="OPV_3",
        name="OPV-3",
        description="Oral Polio Vaccine 3rd dose.",
        due_days_after_birth=98, # 14 weeks
        due_timing_label="14 Weeks",
        dose_number=3
    ),
    VaccineScheduleReference(
        vaccine_code="PENTA_3",
        name="Pentavalent-3",
        description="Pentavalent 3rd dose.",
        due_days_after_birth=98,
        due_timing_label="14 Weeks",
        dose_number=3
    ),
    VaccineScheduleReference(
        vaccine_code="MR_1",
        name="Measles & Rubella-1 (MR-1)",
        description="Protects against Measles and Rubella.",
        due_days_after_birth=270, # 9 months
        due_timing_label="9 Months",
        dose_number=1
    ),
    VaccineScheduleReference(
        vaccine_code="JE_1",
        name="Japanese Encephalitis-1",
        description="Protects against Japanese Encephalitis in endemic districts.",
        due_days_after_birth=270,
        due_timing_label="9 Months",
        dose_number=1
    ),
    VaccineScheduleReference(
        vaccine_code="VIT_A_1",
        name="Vitamin A (Dose 1)",
        description="Prevents Vitamin A deficiency and blindness.",
        due_days_after_birth=270,
        due_timing_label="9 Months",
        dose_number=1
    ),
    VaccineScheduleReference(
        vaccine_code="MR_2",
        name="MR Booster / MR-2",
        description="Measles & Rubella 2nd dose.",
        due_days_after_birth=480, # 16-24 months (~16 months)
        due_timing_label="16-24 Months",
        dose_number=2
    ),
    VaccineScheduleReference(
        vaccine_code="DPT_BOOSTER_1",
        name="DPT Booster-1",
        description="Diphtheria, Pertussis, Tetanus 1st booster.",
        due_days_after_birth=480,
        due_timing_label="16-24 Months",
        dose_number=1
    )
]

def calculate_age_months(dob: date, today: Optional[date] = None) -> int:
    if not today:
        today = date.today()
    days = (today - dob).days
    return max(0, days // 30)

def generate_child_schedule(
    dob: date,
    dose_records: List[DoseRecord],
    today: Optional[date] = None
) -> Tuple[List[CalculatedDose], int, Optional[CalculatedDose]]:
    """
    Calculates due dates and status for all reference vaccines given child's DOB
    and existing dose completion records.
    Returns: (list_of_calculated_doses, progress_percentage, next_due_or_upcoming_vaccine)
    """
    if not today:
        today = date.today()

    record_map: Dict[str, DoseRecord] = {r.vaccine_code: r for r in dose_records}
    calculated_doses: List[CalculatedDose] = []
    
    done_count = 0
    next_vaccine: Optional[CalculatedDose] = None

    for ref in VACCINE_REFERENCE_SCHEDULE:
        due_date = dob + timedelta(days=ref.due_days_after_birth)
        
        # Determine status
        existing_record = record_map.get(ref.vaccine_code)
        
        if existing_record and existing_record.status == "done":
            status = "done"
            admin_date = existing_record.administered_date or due_date
            done_count += 1
        else:
            admin_date = None
            if due_date <= today:
                # If due date was in the past and overdue by > 30 days without completion
                if (today - due_date).days > 30:
                    status = "missed"
                else:
                    status = "due"
            else:
                status = "upcoming"

        calc_dose = CalculatedDose(
            vaccine_code=ref.vaccine_code,
            name=ref.name,
            description=ref.description,
            due_timing_label=ref.due_timing_label,
            due_date=due_date,
            status=status,
            administered_date=admin_date
        )
        calculated_doses.append(calc_dose)

    total_vaccines = len(VACCINE_REFERENCE_SCHEDULE)
    progress_pct = int((done_count / total_vaccines) * 100) if total_vaccines > 0 else 0

    # Pick next vaccine (first 'due', or first 'missed', or first 'upcoming')
    for d in calculated_doses:
        if d.status == "due":
            next_vaccine = d
            break
    if not next_vaccine:
        for d in calculated_doses:
            if d.status == "missed":
                next_vaccine = d
                break
    if not next_vaccine:
        for d in calculated_doses:
            if d.status == "upcoming":
                next_vaccine = d
                break

    return calculated_doses, progress_pct, next_vaccine
