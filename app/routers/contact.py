from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactOut

router = APIRouter(
    prefix="/contact",   
    tags=["Contact"]
)

@router.post("/", response_model=ContactOut)   
def create_contact(data: ContactCreate, db: Session = Depends(get_db)):
    contact = Contact(**data.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact
