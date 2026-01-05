from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.area import AreaCreate, AreaUpdate, AreaOut
from app.models.area import Area
from app.core.database import get_db

router = APIRouter(prefix="/areas", tags=["Areas"])

@router.post("/", response_model=AreaOut)
def create_area(data: AreaCreate, db: Session = Depends(get_db)):
    area = Area(**data.dict())
    db.add(area)
    db.commit()
    db.refresh(area)
    return area

@router.get("/", response_model=list[AreaOut])
def get_areas(db: Session = Depends(get_db)):
    return db.query(Area).all()

@router.put("/{area_id}", response_model=AreaOut)
def update_area(area_id: int, data: AreaUpdate, db: Session = Depends(get_db)):
    area = db.query(Area).filter(Area.area_id == area_id).first()
    if not area:
        raise HTTPException(404, "Area not found")

    for k, v in data.dict(exclude_unset=True).items():
        setattr(area, k, v)

    db.commit()
    db.refresh(area)
    return area

@router.delete("/{area_id}")
def delete_area(area_id: int, db: Session = Depends(get_db)):
    area = db.query(Area).filter(Area.area_id == area_id).first()
    if not area:
        raise HTTPException(404, "Area not found")

    db.delete(area)
    db.commit()
    return {"message": "Area deleted"}
