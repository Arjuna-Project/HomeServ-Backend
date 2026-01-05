from pydantic import BaseModel

class ProfessionalLogin(BaseModel):
    email: str
    password: str
