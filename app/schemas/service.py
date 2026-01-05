from pydantic import BaseModel

class ServiceBase(BaseModel):
    name: str
    description: str
    category: str
    base_price: float

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    category: str | None = None
    base_price: float | None = None

class ServiceOut(ServiceBase):
    service_id: int
    class Config:
        from_attributes = True

