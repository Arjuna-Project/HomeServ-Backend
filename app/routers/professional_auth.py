from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.professionals import Professional
from app.schemas.professional_auth import ProfessionalLogin

router = APIRouter(prefix="/professionals", tags=["Professional Auth"])


@router.post("/login")
def professional_login(
    data: ProfessionalLogin,
    db: Session = Depends(get_db)
):
    professional = db.query(Professional).filter(
        Professional.email == data.email,
        Professional.is_active == True
    ).first()

    if not professional:
        raise HTTPException(status_code=404, detail="Professional not found")

    if professional.password != data.password:
        raise HTTPException(status_code=401, detail="Invalid password")

    return {
        "professional_id": professional.professional_id,
        "name": professional.name,
        "email": professional.email
    }
