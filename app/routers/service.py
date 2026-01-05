from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.service import ServiceCreate, ServiceUpdate, ServiceOut
from app.models.service import Service
from app.core.database import get_db

router = APIRouter(prefix="/services", tags=["Services"])

@router.post("/", response_model=ServiceOut)
def create_service(data: ServiceCreate, db: Session = Depends(get_db)):
    service = Service(**data.dict())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service

@router.get("/", response_model=list[ServiceOut])
def get_services(db: Session = Depends(get_db)):
    return db.query(Service).all()

@router.put("/{service_id}", response_model=ServiceOut)
def update_service(service_id: int, data: ServiceUpdate, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.service_id == service_id).first()
    if not service:
        raise HTTPException(404, "Service not found")

    for k, v in data.dict(exclude_unset=True).items():
        setattr(service, k, v)

    db.commit()
    db.refresh(service)
    return service

@router.delete("/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.service_id == service_id).first()
    if not service:
        raise HTTPException(404, "Service not found")

    db.delete(service)
    db.commit()
    return {"message": "Service deleted"}
