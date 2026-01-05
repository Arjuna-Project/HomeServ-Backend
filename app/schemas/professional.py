from pydantic import BaseModel

class ProfessionalBase(BaseModel):
    name: str
    email: str
    phone: str
    area_id: int
    service_id: int
    rating: float | None = None
    is_active: bool = True


class ProfessionalCreate(ProfessionalBase):
    password: str


class ProfessionalUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    area_id: int | None = None
    service_id: int | None = None
    rating: float | None = None
    is_active: bool | None = None


class ProfessionalOut(ProfessionalBase):
    professional_id: int

    class Config:
        from_attributes = True
