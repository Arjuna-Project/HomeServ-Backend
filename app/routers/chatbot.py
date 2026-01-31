import os
import json
import re
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
You are an experienced and safety-conscious home service professional.

Your task is to analyze the uploaded image of a home-related issue and decide
whether it can be safely fixed by a normal household user (DIY) or if it requires
a trained professional.

You MUST respond STRICTLY in valid JSON format only. Do not include explanations,
extra text, or markdown outside the JSON.

JSON format to follow:

{
  "issue": "<clear description of the problem seen in the image>",
  "service": "<one relevant HomeServ service category such as Plumbing, Electrical, Carpenter, Cleaning, Appliance Repair>",
  "diy_safe": true or false,
  "requirements": [
    "<specific tool or material 1>",
    "<specific tool or material 2>",
    "<protective item if needed>"
  ],
  "steps": [
    "<clear, beginner-friendly step 1 explaining what to do and why>",
    "<clear, beginner-friendly step 2 with proper action details>",
    "<clear, beginner-friendly step 3 including how to finish or verify the fix>"
  ]
}

Rules and safety guidelines:

- If diy_safe is TRUE:
  - Include BOTH "requirements" and "steps".
  - Requirements should list realistic household tools and materials such as:
    screwdrivers, adjustable wrench, pliers, replacement parts, cleaning cloth,
    gloves, bucket, tape, etc.
  - Steps must be detailed, easy to understand, and suitable for a non-technical user.
  - Steps should include preparation, fixing action, and final verification.

- If diy_safe is FALSE:
  - Set "diy_safe" to false.
  - DO NOT include "requirements" or "steps".
  - Only include "issue" and "service".
  - Consider issues involving electricity, gas, heavy appliances, structural damage,
    or high risk as NOT DIY safe.

- Prioritize user safety over convenience.
- Be realistic and practical, not overly technical.
- Do NOT assume professional-grade tools for DIY users.

Remember: Output ONLY valid JSON and nothing else.
"""


    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-4o-mini",
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

    # ✅ SAFE JSON EXTRACTION
    try:
        ai_data = extract_json(ai_reply)
    except Exception:
        print("AI RAW RESPONSE:", ai_reply)
        return {
            "type": "error",
            "reply": "I couldn't clearly analyze this image. Please upload a clearer image."
        }

    # 🟢 DIY SAFE → SHOW STEPS
    if ai_data.get("diy_safe") is True:
        requirements = "\n".join(
            [f"- {r}" for r in ai_data.get("requirements", [])]
        )

        steps = "\n".join(
            [f"{i+1}. {s}" for i, s in enumerate(ai_data.get("steps", []))]
        )

        return {
            "type": "diy",
            "reply": (
                f"Issue identified: {ai_data.get('issue')}\n\n"
                f"Requirements:\n{requirements}\n\n"
                f"Steps:\n{steps}"
            )
        }


    # 🔴 DIY RISKY → CREATE BOOKING
    booking_id = create_booking(
        user_id=req.user_id,
        service=ai_data.get("service"),
        issue=ai_data.get("issue")
    )

    # 🔴 DIY RISKY → JUST SHOW WARNING (NO BOOKING)
    return {
        "type": "risky",
        "reply": (
            f"⚠️ Issue identified: {ai_data.get('issue')}\n\n"
            "This issue is risky to handle on your own.\n\n"
            "🔧 Please book a professional through HomeServ to avoid safety hazards."
        )
    }



# -------- JSON EXTRACTION HELPER --------
def extract_json(text: str):
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON found")
    return json.loads(match.group())


# -------- BOOKING CREATION (MOCK) --------
def create_booking(user_id: Optional[int], service: str, issue: str):

    booking = {
        "user_id": user_id,
        "service": service,
        "issue": issue,
        "status": "confirmed",
        "source": "image"
    }

    print("BOOKING CREATED:", booking)

    return 1001
