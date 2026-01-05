from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class Area(Base):
    __tablename__ = "areas"

    area_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    pincode = Column(String, nullable=False)
    image_url = Column(Text, nullable=True)
