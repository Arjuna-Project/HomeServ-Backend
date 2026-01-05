from pydantic import BaseModel

class AreaBase(BaseModel):
    name: str
    city: str
    pincode: str
    image_url: str | None = None   

class AreaCreate(AreaBase):
    pass

class AreaUpdate(BaseModel):
    name: str | None = None
    city: str | None = None
    pincode: str | None = None
    image_url: str | None = None   

class AreaOut(AreaBase):
    area_id: int

    class Config:
        from_attributes = True
