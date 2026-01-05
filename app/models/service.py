from sqlalchemy import Column, Integer, String, DECIMAL, Text
from app.core.database import Base

class Service(Base):
    __tablename__ = "services"

    service_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    category = Column(String)
    base_price = Column(DECIMAL)
