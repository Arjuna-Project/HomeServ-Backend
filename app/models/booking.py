from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Text, ForeignKey
from datetime import datetime
from app.core.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    booking_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    area_id = Column(Integer, ForeignKey("areas.area_id"), nullable=False, index=True)

    package_id = Column(Integer, ForeignKey("packages.package_id"), nullable=True)
    service_id = Column(Integer, ForeignKey("services.service_id"), nullable=True)
    professional_id = Column(Integer, ForeignKey("professionals.professional_id"), nullable=True)

    scheduled_at = Column(DateTime, nullable=False)
    status = Column(String, default="pending")
    total_price = Column(DECIMAL, nullable=False)
    details = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)
