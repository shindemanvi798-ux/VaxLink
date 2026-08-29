from fastapi import APIRouter, Depends, HTTPException, status
import httpx
from app.schemas.chat import ChatRequest, ChatResponse
from app.core.config import settings
# from app.api.dependencies.auth import get_current_user # Optional: Uncomment if you want only logged-in users to use chat

router = APIRouter()

# System prompt defining the persona of the Saathi bot
SYSTEM_PROMPT = """
You are Saathi, a helpful, empathetic, and knowledgeable health companion for rural Indian parents.
Your goal is to answer questions about child vaccination, nutrition, and health camps.
Keep your answers brief, simple, and easy to understand.
Do not provide medical diagnoses. Always advise consulting an ASHA worker or doctor for serious concerns.
"""

@router.post("/", response_model=ChatResponse)
async def chat_with_saathi(
    request: ChatRequest, 
    # current_user: dict = Depends(get_current_user) # Uncomment to secure this endpoint
):
    """
    Proxies chat requests to the Anthropic (Claude) API securely on the server.
    This ensures the Anthropic API key is never exposed to the frontend browser.
    """
    if not settings.ANTHROPIC_API_KEY or settings.ANTHROPIC_API_KEY == "your-anthropic-api-key":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="AI Chatbot is not configured on the server."
        )

    # Format the messages for Anthropic's Messages API format
    formatted_messages = [
        {"role": msg.role, "content": msg.content}
        for msg in request.messages
    ]

    # Append a polite language instruction to the system prompt based on user preference
    lang_instruction = f"\nPlease reply in {request.language}."
    final_system_prompt = SYSTEM_PROMPT + lang_instruction

    try:
        # We use httpx.AsyncClient to make a non-blocking HTTP request to Anthropic
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": settings.ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                },
                json={
                    "model": "claude-3-haiku-20240307", # Fast and cheap model, perfect for this
                    "max_tokens": 500,
                    "system": final_system_prompt,
                    "messages": formatted_messages
                },
                timeout=30.0 # Don't hang forever if the API is slow
            )
            
        if response.status_code != 200:
            # Log the actual error internally, but give a generic message to the frontend
            error_data = response.json()
            print(f"Anthropic API Error: {error_data}")
            raise HTTPException(status_code=502, detail="Error communicating with the AI service.")

        response_data = response.json()
        
        # Extract the text reply from Claude's response format
        reply_text = response_data['content'][0]['text']
        
        return ChatResponse(reply=reply_text)

    except httpx.RequestError as e:
        print(f"HTTP Request Error: {e}")
        raise HTTPException(status_code=502, detail="Failed to connect to AI service.")
    except Exception as e:
        print(f"Unexpected Error: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred while processing the chat.")
