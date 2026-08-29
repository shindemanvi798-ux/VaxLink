from pydantic import BaseModel, Field
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str = Field(..., description="Must be 'user' or 'assistant'")
    content: str = Field(..., description="The message content")

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    language: Optional[str] = Field(default="hi", description="Preferred language code (e.g., 'hi', 'en', 'mr')")

class ChatResponse(BaseModel):
    reply: str
