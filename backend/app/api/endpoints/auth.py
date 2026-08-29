from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import OTPRequest, OTPVerify, TokenResponse, UserProfile
from app.db.supabase import supabase

router = APIRouter()

@router.post("/otp/request", status_code=status.HTTP_200_OK)
async def request_otp(data: OTPRequest):
    """
    Sends an OTP to the provided phone number using Supabase Auth.
    """
    try:
        # Supabase sends the OTP via Twilio (configured in the Supabase dashboard)
        res = supabase.auth.signInWithOtp({"phone": data.phone})
        return {"message": "OTP sent successfully"}
    except Exception as e:
        # We catch generic exceptions here. Supabase raises its own errors for rate limits, etc.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/otp/verify", response_model=TokenResponse)
async def verify_otp(data: OTPVerify):
    """
    Verifies the OTP and returns the session tokens and basic user profile.
    """
    try:
        # Verify the OTP with Supabase
        res = supabase.auth.verify_otp({
            "phone": data.phone,
            "token": data.otp,
            "type": "sms"
        })
        
        session = res.session
        if not session:
            raise ValueError("Invalid OTP or session could not be established.")
            
        # Once authenticated, we fetch their custom profile from our `users` table.
        # We use the standard client, but because we just got the session, 
        # we need to pass the JWT to ensure RLS allows us to read our own profile.
        # (Supabase python client handles the current session token automatically 
        # after a successful login in the same instance, but in a real concurrent backend, 
        # we'd extract it differently. For now, this confirms they exist).
        
        user_id = session.user.id
        
        # Fetch the custom user profile
        user_query = supabase.table('users').select('*').eq('id', user_id).execute()
        
        # If the user doesn't exist in our custom table yet, they are a new user.
        # In a complete flow, we might auto-create a 'parent' record here or redirect them to an onboarding screen.
        # For now, we'll just check if they exist and default to 'parent' if we can't find the role.
        role = "parent" # Default fallback
        if len(user_query.data) > 0:
            role = user_query.data[0].get('role', 'parent')
            
        return TokenResponse(
            access_token=session.access_token,
            refresh_token=session.refresh_token,
            user_id=user_id,
            role=role
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )
