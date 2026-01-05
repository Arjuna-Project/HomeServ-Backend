from pydantic import BaseModel

class PackageBase(BaseModel):
    name: str
    category: str
    price: float
    duration: str
    features: str
    description: str

class PackageCreate(PackageBase):
    pass

class PackageUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    price: float | None = None
    duration: str | None = None
    features: str | None = None
    description: str | None = None

class PackageOut(PackageBase):
    package_id: int
    class Config:
        from_attributes = True
