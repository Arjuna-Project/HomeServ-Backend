from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from app.core.database import Base

class Professional(Base):
    __tablename__ = "professionals"

    professional_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)   # ✅ ADD THIS
    phone = Column(String, nullable=False)

    area_id = Column(Integer, ForeignKey("areas.area_id"), index=True)
    service_id = Column(Integer, ForeignKey("services.service_id"), index=True)

    rating = Column(Float)
    is_active = Column(Boolean, default=True)
