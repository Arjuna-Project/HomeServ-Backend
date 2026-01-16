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
                    "content": "You are HomeServ customer support assistant."
                },
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
