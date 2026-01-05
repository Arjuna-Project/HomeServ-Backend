from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# -----------------------
# CREATE
# -----------------------
class BookingCreate(BaseModel):
    user_id: int
    area_id: int

    package_id: Optional[int] = None
    service_id: Optional[int] = None
    professional_id: Optional[int] = None

    scheduled_at: datetime
    total_price: float
    details: str

# -----------------------
# UPDATE
# -----------------------
class BookingUpdate(BaseModel):
    scheduled_at: Optional[datetime] = None
    status: Optional[str] = None
    total_price: Optional[float] = None
    details: Optional[str] = None

# -----------------------
# RESPONSE (SINGLE SOURCE)
# -----------------------
class BookingOut(BaseModel):
    booking_id: int
    status: str
    scheduled_at: datetime
    total_price: float
    details: str
    created_at: datetime

    class Config:
        from_attributes = True
