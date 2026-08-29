from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.children import ChildCreate, ChildResponse, DoseRecordUpdate, DoseRecordResponse, ScheduleStatusResponse
from app.db.supabase import supabase
from app.api.dependencies.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ChildResponse])
async def list_children(current_user: dict = Depends(get_current_user)):
    """
    List all children for the logged-in family.
    Because RLS is enabled in the database, this query will automatically 
    only return rows where the family_id matches the user's family.
    """
    try:
        # First, we need to find this user's family_id
        # In a real app, this mapping might be cached, but we'll look it up for now.
        family_query = supabase.table('families').select('id').eq('primary_phone', current_user['phone']).execute()
        
        if not family_query.data:
            return [] # No family record yet
            
        family_id = family_query.data[0]['id']
        
        # Now get the children. We set the JWT so RLS works.
        supabase.postgrest.auth(current_user['token'])
        children_query = supabase.table('children').select('*').eq('family_id', family_id).execute()
        
        return children_query.data
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/", response_model=ChildResponse, status_code=status.HTTP_201_CREATED)
async def add_child(child: ChildCreate, current_user: dict = Depends(get_current_user)):
    """
    Add a new child to the logged-in user's family.
    """
    try:
        # Get family ID securely on the backend
        family_query = supabase.table('families').select('id, consent_given_at').eq('primary_phone', current_user['phone']).execute()
        
        if not family_query.data:
            raise HTTPException(status_code=400, detail="Family record not found. Cannot add child.")
            
        family_record = family_query.data[0]
        
        # Enforce consent check as per architecture
        if not family_record.get('consent_given_at'):
            raise HTTPException(
                status_code=403, 
                detail="Consent has not been recorded for this family. Please record consent first."
            )
            
        # Insert the child
        supabase.postgrest.auth(current_user['token'])
        insert_data = {
            "family_id": family_record['id'],
            "name": child.name,
            "dob": child.dob.isoformat()
        }
        
        result = supabase.table('children').insert(insert_data).execute()
        
        # (Track 2 feature) Here you would ideally also trigger a background task or database trigger 
        # to auto-generate the `dose_records` rows for this child based on their DOB and the `vaccine_schedule_reference` table.
        
        return result.data[0]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
