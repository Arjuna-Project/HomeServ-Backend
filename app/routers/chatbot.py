import os
import json
import base64
import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/chat", tags=["Chatbot"])

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# -------- REQUEST MODEL --------
class ChatRequest(BaseModel):
    message: Optional[str] = ""
    image: Optional[str] = None   # base64 encoded image
    user_id: Optional[int] = None


# -------- MAIN ENDPOINT --------
@router.post("/")
def chat_with_bot(req: ChatRequest):

    if not OPENROUTER_API_KEY:
        raise HTTPException(status_code=500, detail="AI key missing")

    # 🟢 IMAGE MODE (DIY / BOOKING)
    if req.image:
        return handle_image(req)

    # 🟢 TEXT MODE (NORMAL Q&A)
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    return handle_text(req.message)


# -------- TEXT Q&A HANDLER --------
def handle_text(user_message: str):

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openrouter/auto",
            "max_tokens": 512,
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
                        "Rules:\n"
                        "- ONLY answer questions related to HomeServ services.\n"
                        "- If unrelated, politely refuse.\n"
                        "- Keep responses short and helpful."
                    )
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        },
        timeout=30
    )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=response.text)

    return {
        "type": "text",
        "reply": response.json()["choices"][0]["message"]["content"]
    }


# -------- IMAGE HANDLER --------
def handle_image(req: ChatRequest):

    prompt = """
You are a home service expert.
Analyze the uploaded image and respond STRICTLY in JSON format like this:

{
  "issue": "<problem identified>",
  "service": "<service category>",
  "diy_safe": true or false,
  "steps": ["step 1", "step 2"]  // only if diy_safe is true
}

If DIY is unsafe, set diy_safe=false and do NOT include steps.
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openrouter/auto",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": f"data:image/jpeg;base64,{req.image}"
                        }
                    ]
                }
            ]
        },
        timeout=30
    )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=response.text)

    ai_reply = response.json()["choices"][0]["message"]["content"]

    try:
        ai_data = json.loads(ai_reply)
    except Exception:
        return {
            "type": "error",
            "reply": "Unable to analyze the image clearly. Please try another image."
        }

    # 🟢 DIY SAFE → SHOW STEPS
    if ai_data.get("diy_safe") is True:
        steps = "\n".join(
            [f"{i+1}. {s}" for i, s in enumerate(ai_data.get("steps", []))]
        )

        return {
            "type": "diy",
            "reply": (
                f"Issue identified: {ai_data.get('issue')}\n\n"
                f"DIY Steps:\n{steps}\n\n"
                "⚠️ If the issue continues, you can book a professional anytime."
            )
        }

    # 🔴 DIY RISKY → CREATE BOOKING
    booking_id = create_booking(
        user_id=req.user_id,
        service=ai_data.get("service"),
        issue=ai_data.get("issue")
    )

    return {
        "type": "booking",
        "reply": (
            f"⚠️ The issue appears risky for DIY.\n"
            f"A professional booking has been created.\n"
            f"Booking ID: {booking_id}"
        )
    }


# -------- BOOKING CREATION (MOCK) --------
def create_booking(user_id: Optional[int], service: str, issue: str):

    # 🔴 Replace this with DB insert later
    booking = {
        "user_id": user_id,
        "service": service,
        "issue": issue,
        "status": "confirmed",
        "source": "image"
    }

    print("BOOKING CREATED:", booking)

    return 1001
