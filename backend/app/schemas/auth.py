from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class OTPRequest(BaseModel):
    phone: str = Field(..., description="Phone number with country code, e.g., +919876543210")

class OTPVerify(BaseModel):
    phone: str = Field(..., description="Phone number with country code")
    otp: str = Field(..., min_length=6, max_length=6, description="6-digit OTP code")

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    user_id: str
    role: str

class UserProfile(BaseModel):
    id: str
    role: str
    phone: str
    full_name: str
    preferred_lang: str
    area: Optional[str] = None
    created_at: datetime
