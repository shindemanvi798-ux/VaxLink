from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.consent import ConsentUpdate, ConsentResponse, DataDeletionRequest
from app.db.supabase import supabase, supabase_admin
from app.api.dependencies.auth import get_current_user
from datetime import datetime

router = APIRouter()

@router.post("/update", response_model=ConsentResponse)
async def update_consent(
    data: ConsentUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Records a DPDP-compliant consent event.
    Logs the action in the immutable consent_log and updates the family record.
    """
    if data.action not in ["given", "withdrawn"]:
        raise HTTPException(status_code=400, detail="Action must be 'given' or 'withdrawn'")
        
    try:
        # 1. Get the family ID
        family_query = supabase.table('families').select('id').eq('primary_phone', current_user['phone']).execute()
        if not family_query.data:
            raise HTTPException(status_code=404, detail="Family record not found.")
        family_id = family_query.data[0]['id']
        
        # 2. Update the family record
        timestamp = datetime.utcnow().isoformat()
        update_payload = {
            "consent_given_at": timestamp if data.action == "given" else None,
            "consent_version": data.consent_text_version if data.action == "given" else None
        }
        
        supabase.postgrest.auth(current_user['token'])
        supabase.table('families').update(update_payload).eq('id', family_id).execute()
        
        # 3. Write to the immutable consent log (audit trail)
        log_payload = {
            "family_id": family_id,
            "action": data.action,
            "consent_text_version": data.consent_text_version
        }
        supabase.table('consent_log').insert(log_payload).execute()
        
        return ConsentResponse(
            message=f"Consent successfully {data.action}",
            consent_given_at=timestamp
        )
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/account", status_code=status.HTTP_200_OK)
async def request_data_deletion(
    request: DataDeletionRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    DPDP Right to Erasure implementation.
    Wipes the family record, children, dose records, and the Supabase Auth user.
    """
    if not request.confirmation:
        raise HTTPException(status_code=400, detail="Confirmation required for data deletion.")
        
    try:
        # Note on cascading deletes:
        # Because we defined `ON DELETE CASCADE` in our initial SQL schema for 
        # children, dose_records, and consent_log, deleting the `families` record 
        # or the `users` record will automatically wipe all associated data in Postgres.
        
        # 1. Delete custom user profile (which will cascade to other things if linked)
        supabase.postgrest.auth(current_user['token'])
        supabase.table('users').delete().eq('id', current_user['id']).execute()
        
        # 2. Delete the actual Auth user in Supabase
        # RLS prevents a user from deleting themselves from the `auth.users` table. 
        # Therefore, we MUST use the `supabase_admin` (service role) client here.
        admin_delete_result = supabase_admin.auth.admin.delete_user(current_user['id'])
        
        return {"message": "All personal data has been permanently deleted in compliance with data protection laws."}
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to process deletion: {str(e)}")
