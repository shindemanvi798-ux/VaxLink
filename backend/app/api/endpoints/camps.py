from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import date
from app.schemas.camps import CampResponse, BookingCreate, BookingResponse
from app.db.supabase import supabase
from app.api.dependencies.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[CampResponse])
async def list_camps(area: str = None, filter_date: date = None):
    """
    List vaccination camps. 
    Can be filtered by area and date. 
    This is generally public info, so it might not require auth, 
    but booking a slot WILL require auth.
    """
    try:
        query = supabase.table('camps').select('*, camp_slots(*)')
        
        if area:
            query = query.eq('area', area)
        if filter_date:
            query = query.eq('date', filter_date.isoformat())
            
        result = query.execute()
        
        # Format the nested Supabase response to match our Pydantic schema
        camps = []
        for camp_data in result.data:
            camps.append({
                "id": camp_data["id"],
                "area": camp_data["area"],
                "date": camp_data["date"],
                "slots": camp_data.get("camp_slots", [])
            })
            
        return camps
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/{camp_id}/slots/{slot_id}/book", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def book_slot(
    camp_id: str, 
    slot_id: str, 
    booking_data: BookingCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Book a specific slot at a camp for a child.
    Enforces capacity limits and ensures the user only books for their own family.
    """
    try:
        # 1. Get the family ID securely
        family_query = supabase.table('families').select('id').eq('primary_phone', current_user['phone']).execute()
        if not family_query.data:
            raise HTTPException(status_code=400, detail="Family record not found.")
        family_id = family_query.data[0]['id']
        
        # 2. Verify the child actually belongs to this family (security check)
        child_query = supabase.table('children').select('id').eq('id', booking_data.child_id).eq('family_id', family_id).execute()
        if not child_query.data:
             raise HTTPException(status_code=403, detail="Child does not belong to this family or does not exist.")

        # 3. Check capacity before booking
        # In a high-traffic production app, this requires a Postgres transaction or RPC to prevent race conditions.
        # For the pilot, a simple read-then-write is acceptable.
        slot_query = supabase.table('camp_slots').select('capacity, booked_count').eq('id', slot_id).execute()
        
        if not slot_query.data:
            raise HTTPException(status_code=404, detail="Slot not found.")
            
        slot = slot_query.data[0]
        if slot['booked_count'] >= slot['capacity']:
            raise HTTPException(status_code=409, detail="This slot is fully booked.")
            
        # 4. Create the booking
        supabase.postgrest.auth(current_user['token'])
        booking_insert = {
            "camp_slot_id": slot_id,
            "family_id": family_id,
            # If you added child_id to the bookings table in SQL, pass it here. 
            # We assume it exists based on the architecture requirement to track *who* is coming.
        }
        
        booking_result = supabase.table('bookings').insert(booking_insert).execute()
        
        # 5. Increment the booked_count on the slot
        new_count = slot['booked_count'] + 1
        supabase.table('camp_slots').update({"booked_count": new_count}).eq('id', slot_id).execute()
        
        # Return the created booking (we merge child_id back in for the response schema if it wasn't inserted)
        response_data = booking_result.data[0]
        response_data['child_id'] = booking_data.child_id 
        
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
