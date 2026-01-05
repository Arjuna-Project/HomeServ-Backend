from pydantic import BaseModel
from datetime import datetime

class ContactCreate(BaseModel):
    name: str
    email: str
    phone: str
    subject: str
    message: str

class ContactOut(ContactCreate):
    contact_id: int
    created_at: datetime

    class Config:
        from_attributes = True
