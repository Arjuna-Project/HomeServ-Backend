from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.models.professionals import Professional
from app.schemas.professional import ProfessionalOut
from app.core.database import get_db

router = APIRouter(prefix="/professionals", tags=["Professionals"])


@router.get("/search", response_model=list[ProfessionalOut])
def search_professionals(
    area_id: int = Query(...),
    service_id: int = Query(...),
    db: Session = Depends(get_db)
):
    professionals = (
        db.query(Professional)
        .filter(
            Professional.area_id == area_id,
            Professional.service_id == service_id,
            Professional.is_active == True
        )
        .order_by(Professional.rating.desc())
        .all()
    )

    return professionals
