import os
import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["Chatbot"])

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

class ChatRequest(BaseModel):
    message: str

@router.post("/")
def chat_with_bot(req: ChatRequest):

    if not OPENROUTER_API_KEY:
        raise HTTPException(status_code=500, detail="AI key missing")

    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openrouter/auto",
            "max_tokens":512,
            "messages": [
                {
  "role": "system",
  "content": (
    "You are the official HomeServ customer support assistant.\n\n"
    "HomeServ is a home services platform similar to UrbanClap.\n"
    "HomeServ offers the following services:\n"
    "- Home cleaning (deep cleaning, bathroom, kitchen)\n"
    "- Plumbing services (leak repair, pipe installation, fittings)\n"
    "- Electrical services (wiring, switch installation, repairs)\n"
    "- Appliance repair (AC, washing machine, refrigerator)\n"
    "- Carpenter services (furniture repair, custom wood work)\n"
    "- Gardening and landscaping\n"
    "- Renovation and interior services\n"
    "- Technology services (CCTV, WiFi, smart home setup)\n\n"
    "HomeServ also provides:\n"
    "- Area selection (Adyar, Guindy, OMR, Velachery, Anna Nagar, etc.)\n"
    "- Viewing professionals for each service\n"
    "- Service packages (monthly, half-yearly, yearly plans)\n"
    "- Booking, rescheduling, and cancellation of services\n"
    "- Pricing, plans, and subscriptions\n"
    "- User account and profile assistance\n\n"
    "Rules:\n"
    "- ONLY answer questions related to HomeServ services.\n"
    "- If a question is unrelated (politics, coding, movies, general knowledge), politely refuse.\n"
    "- Always respond as HomeServ customer support.\n"
    "- Keep responses short, clear, and helpful.\n\n"
    "If the question is unrelated, reply:\n"
    "\"I can help only with HomeServ home services. Please ask a HomeServ-related question.\""
  )
}
,
                {
                    "role": "user",
                    "content": req.message
                }
            ]
        },
        timeout=30
    )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=response.text)

    return {
        "reply": response.json()["choices"][0]["message"]["content"]
    }
