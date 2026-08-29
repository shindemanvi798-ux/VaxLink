from pydantic import BaseModel, Field
from datetime import datetime

class ConsentUpdate(BaseModel):
    action: str = Field(..., description="Must be 'given' or 'withdrawn'")
    consent_text_version: str = Field(..., description="The specific version/hash of the text the user agreed to")

class ConsentResponse(BaseModel):
    message: str
    consent_given_at: datetime
    
class DataDeletionRequest(BaseModel):
    confirmation: bool = Field(..., description="Must be true to proceed with deletion")
