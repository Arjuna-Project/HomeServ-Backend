from sqlalchemy import Column, Integer, String, DECIMAL, Text
from app.core.database import Base

class Package(Base):
    __tablename__ = "packages"

    package_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String)
    price = Column(DECIMAL, nullable=False)
    duration = Column(String)
    features = Column(Text)
    description = Column(Text)
