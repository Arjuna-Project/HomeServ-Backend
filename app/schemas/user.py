from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: str
    phone: str
    address: str


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    address: str | None = None


class UserOut(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
