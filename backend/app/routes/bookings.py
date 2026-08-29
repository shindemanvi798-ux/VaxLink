from fastapi import APIRouter, HTTPException, status
from app.models import BookingRequest, BookingResponse
from app.database import book_camp_slot

router = APIRouter(tags=["Bookings"])

@router.post("/camps/{camp_id}/slots/{slot_id}/book", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(camp_id: str, slot_id: str, req: BookingRequest):
    """
    Book a vaccination slot for a child at a camp.
    Automatically validates slot capacity, updates booked count, updates crowd indicator, and returns confirmation.
    """
    try:
        booking_result = book_camp_slot(
            camp_id=camp_id,
            slot_id=slot_id,
            child_id=req.child_id,
            family_id=req.family_id or "fam_demo_001"
        )
        return booking_result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error while creating booking.")
