from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.db.supabase import supabase
from typing import Dict, Any

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> Dict[str, Any]:
    """
    Validates the JWT token in the Authorization header.
    Returns the user data and sets the session on the Supabase client.
    """
    token = credentials.credentials
    try:
        # We use supabase.auth.get_user(token) to validate the JWT.
        # This confirms the token is valid, hasn't expired, and was signed by our Supabase project.
        user_response = supabase.auth.get_user(token)
        
        if not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # Optional: In a production app with concurrent requests, you might need to manage 
        # the JWT carefully per-request so the RLS policies apply correctly to THIS specific user.
        # Supabase Python client v2 allows setting the auth header dynamically per request 
        # if you are bypassing the built-in auth manager, but for this pilot, getting the user 
        # proves they are authenticated.
            
        return {
            "id": user_response.user.id,
            "phone": user_response.user.phone,
            "token": token
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
