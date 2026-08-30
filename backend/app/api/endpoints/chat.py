from fastapi import APIRouter, Depends, HTTPException, status
import httpx
from app.schemas.chat import ChatRequest, ChatResponse
from app.core.config import settings

router = APIRouter()

# System prompt defining the persona of the Saathi bot
SYSTEM_PROMPT = """
You are Saathi, a helpful, empathetic, and knowledgeable health companion for rural Indian parents.
Your goal is to answer questions about child vaccination, nutrition, and health camps.
Keep your answers brief, simple, and easy to understand.
Do not provide medical diagnoses. Always advise consulting an ASHA worker or doctor for serious concerns.
"""

def get_mock_chat_response(messages, language: str) -> str:
    """
    Robust local rule-based fallback when live Anthropic API is unavailable.
    Provides helpful answers in English, Hindi, and Marathi based on keywords.
    """
    lang = (language or "en").lower().strip()
    if lang not in ["en", "hi", "mr"]:
        lang = "en"
        
    # Get the last user message text
    user_text = ""
    for msg in reversed(messages):
        if msg.role == "user" or msg["role"] == "user":
            user_text = msg.content if hasattr(msg, "content") else msg.get("content", "")
            break
            
    user_text_lower = user_text.lower()
    
    # 1. BCG Vaccine
    if "bcg" in user_text_lower or any(k in user_text_lower for k in ["टीबी", "क्षयरोग"]):
        if lang == "hi":
            return "बीसीजी (BCG) टीका शिशुओं को तपेदिक (टीबी) से बचाता है। यह जन्म के समय (या 1 वर्ष से पहले जितनी जल्दी हो सके) बाईं ऊपरी बांह पर दिया जाता है। 2-3 सप्ताह के बाद वहां एक छोटा सा निशान बन जाता है, जो पूरी तरह से सामान्य है।"
        elif lang == "mr":
            return "बीसीजी (BCG) लस बाळांचे क्षयरोगापासून (टीबी) संरक्षण करते. ती जन्मानंतर लगेचच (किं त्यापूर्वी किंवा १ वर्षाच्या आत शक्य तितक्या लवकर) डाव्या हातावर दिली जाते. २-३ आठवड्यांनंतर तिथे लहान वण तयार होतो, जे अगदी सामान्य आहे।"
        else:
            return "BCG vaccine protects infants from Tuberculosis (TB). It is given at birth (or as soon as possible before 1 year of age) on the left upper arm. A small scar usually forms at the site after 2-3 weeks, which is completely normal."

    # 2. OPV Vaccine / Polio
    if "opv" in user_text_lower or any(k in user_text_lower for k in ["polio", "पोलियो", "पोलिओ"]):
        if lang == "hi":
            return "ओरल पोलियो वैक्सीन (OPV) बच्चों को पोलियो से बचाती है। यह जन्म के समय (शून्य खुराक), 6 सप्ताह, 10 सप्ताह और 14 सप्ताह पर मुंह में 2 बूंदों के रूप में दी जाती है।"
        elif lang == "mr":
            return "ओरल पोलिओ लस (OPV) बाळाचे पोलिओपासून संरक्षण करते. ती जन्मल्याबरोबर (शून्य डोस), ६ आठवड्यांनी, १० आठवड्यांनी आणि १४ आठवड्यांनी तोंडावाटे २ थेंब दिली जाते।"
        else:
            return "Oral Polio Vaccine (OPV) protects against Polio. It is given at Birth (Zero dose), 6 Weeks, 10 Weeks, and 14 Weeks as 2 drops by mouth."

    # 3. Pentavalent Vaccine
    if "penta" in user_text_lower or any(k in user_text_lower for k in ["पेंटा", "पेंटाव्हॅलेंट"]):
        if lang == "hi":
            return "पेंटावैलेंट वैक्सीन 5 जानलेवा बीमारियों से बचाती है: डिप्थीरिया, काली खांसी, टेटनस, हेपेटाइटिस बी और हिब। यह 6, 10 और 14 सप्ताह की उम्र में इंजेक्शन के रूप में दी जाती है।"
        elif lang == "mr":
            return "पेंटाव्हॅलेंट लस ५ घातक आजारांपासून संरक्षण करते: घटसर्प, डांग्या खोकला, धनुर्वात, हिपॅटायटीस बी आणि हिब. ती ६, १० आणि १४ व्या आठवड्यात इंजेक्शनद्वारे दिली जाते।"
        else:
            return "Pentavalent vaccine protects against 5 deadly diseases: Diphtheria, Pertussis (Whooping Cough), Tetanus, Hepatitis B, and Hib. It is given as an injection at 6, 10, and 14 weeks of age."

    # 4. Fever
    if any(k in user_text_lower for k in ["fever", "fiver", "बुखार", "ताप", "सूजन", "दुख"]):
        if lang == "hi":
            return "टीकाकरण के बाद हल्का बुखार, लालिमा या इंजेक्शन वाली जगह पर सूजन सामान्य लक्षण हैं, जो दर्शाते हैं कि टीका काम कर रहा है। आप ठंडे पानी की पट्टी रख सकते हैं। यदि बुखार 101°F से अधिक हो या 2 दिन से अधिक रहे, तो कृपया अपनी आशा कार्यकर्ता या डॉक्टर से संपर्क करें।"
        elif lang == "mr":
            return "लसीकरणानंतर सौम्य ताप, लालसरपणा किंवा सूज येणे सामान्य आहे, ज्याचा अर्थ असा की लस काम करत आहे. तुम्ही थंड पाण्याच्या पट्ट्या ठेवू शकता. ताप १०१°F पेक्षा जास्त असल्यास किंवा २ दिवसांपेक्षा जास्त राहिल्यास, कृपया आशा सेविका किंवा डॉक्टरांचा सल्ला घ्या।"
        else:
            return "Mild fever, redness, or swelling at the injection site are normal signs that the vaccine is working. You can apply a cold cloth to the site. If the fever exceeds 101°F or lasts more than 2 days, please consult your ASHA worker or doctor immediately."

    # 5. Camps / Booking
    if any(k in user_text_lower for k in ["camp", "book", "कैंप", "बुक", "शिबीर", "अपॉइंटमेंट"]):
        if lang == "hi":
            return "आप 'Find Camps' (कैंप खोजें) टैब के अंतर्गत पास के टीकाकरण शिविरों को देख सकते हैं और स्लॉट बुक कर सकते हैं। भीड़ से बचने के लिए हरे/LOW भीड़ की स्थिति वाले कैंप का चयन करें!"
        elif lang == "mr":
            return "तुम्ही 'शिबिरे शोधा' टॅब अंतर्गत जवळील लसीकरण शिबिरे पाहू शकता आणि वेळ बुक करू शकता. जास्त वेळ थांबावे लागू नये म्हणून हिरवे/LOW गर्दीचे शिबीर निवडा!"
        else:
            return "You can view nearby vaccination camps and book a slot under the 'Find Camps' tab. Choose a camp with green/LOW crowd status to avoid waiting!"

    # 6. Greetings
    if any(k in user_text_lower for k in ["hello", "hi", "hey", "namaste", "नमस्ते", "नमस्कार", "राम राम"]):
        if lang == "hi":
            return "नमस्ते! मैं साथी हूँ, आपका स्वास्थ्य साथी। मैं आपको बच्चों के टीकाकरण कार्यक्रम, पास के स्वास्थ्य शिविरों और सामान्य स्वास्थ्य जानकारी में मदद कर सकता हूँ। आपके बच्चे का नाम और उम्र क्या है?"
        elif lang == "mr":
            return "नमस्कार! मी साथी आहे, तुमचा आरोग्य मित्र. मी तुम्हाला बाल लसीकरण वेळापत्रक, जवळची शिबिरे आणि सामान्य आरोग्य माहितीबद्दल मदत करू शकतो. तुमच्या बाळाचे नाव आणि वय काय आहे?"
        else:
            return "Hello! I am Saathi, your health companion. I can help you with child vaccination schedules, nearby camps, and general health info. What is your child's name and age?"

    # 7. Default
    if lang == "hi":
        return "पूछने के लिए धन्यवाद! विशिष्ट चिकित्सा सलाह के लिए, हमेशा अपने स्थानीय आशा कार्यकर्ता या स्वास्थ्य केंद्र के डॉक्टर से परामर्श करें। आप 'Schedule' (होम) टैब में बच्चे के टीके की नियत तारीखें भी देख सकते हैं।"
    elif lang == "mr":
        return "विचारल्याबद्दल धन्यवाद! विशिष्ट वैद्यकीय सल्ल्यासाठी, नेहमी तुमच्या स्थानिक आशा सेविका किंवा आरोग्य केंद्राच्या डॉक्टरांचा सल्ला घ्या. तुम्ही ' वेळापत्रक' टॅबमध्ये बाळाच्या लसीकरणाची तारीख देखील पाहू शकता।"
    else:
        return "Thank you for asking! For specific medical advice, always consult your local ASHA worker or a health center doctor. You can also view your child's due dates in the 'Schedule' tab."


@router.post("/", response_model=ChatResponse)
async def chat_with_saathi(request: ChatRequest):
    """
    Proxies chat requests to the Anthropic (Claude) API securely on the server.
    If the API is unavailable or credit balance is too low, it falls back
    gracefully to a local, high-quality, multilingual mock dialog manager.
    """
    # 1. Check if Anthropic configuration is complete
    if not settings.ANTHROPIC_API_KEY or settings.ANTHROPIC_API_KEY == "your-anthropic-api-key":
        print("[Saathi Chat] Anthropic API Key not configured. Using high-quality multilingual local fallback.")
        reply_text = get_mock_chat_response(request.messages, request.language)
        return ChatResponse(reply=reply_text)

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
                timeout=10.0 # Fast response, fail quick to trigger mock fallback
            )
            
        if response.status_code != 200:
            error_data = response.json()
            print(f"[Saathi Chat] Anthropic API Error ({response.status_code}): {error_data}. Falling back to multilingual local engine.")
            reply_text = get_mock_chat_response(request.messages, request.language)
            return ChatResponse(reply=reply_text)

        response_data = response.json()
        
        # Extract the text reply from Claude's response format
        reply_text = response_data['content'][0]['text']
        return ChatResponse(reply=reply_text)

    except Exception as e:
        print(f"[Saathi Chat] Exception: {e}. Falling back to multilingual local engine.")
        reply_text = get_mock_chat_response(request.messages, request.language)
        return ChatResponse(reply=reply_text)
