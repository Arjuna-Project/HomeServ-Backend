from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.package import PackageCreate, PackageUpdate, PackageOut
from app.models.package import Package
from app.core.database import get_db

router = APIRouter(prefix="/packages", tags=["Packages"])

@router.post("/", response_model=PackageOut)
def create_package(data: PackageCreate, db: Session = Depends(get_db)):
    pkg = Package(**data.dict())
    db.add(pkg)
    db.commit()
    db.refresh(pkg)
    return pkg

@router.get("/", response_model=list[PackageOut])
def get_packages(db: Session = Depends(get_db)):
    return db.query(Package).all()

@router.put("/{package_id}", response_model=PackageOut)
def update_package(package_id: int, data: PackageUpdate, db: Session = Depends(get_db)):
    pkg = db.query(Package).filter(Package.package_id == package_id).first()
    if not pkg:
        raise HTTPException(404, "Package not found")

    for k, v in data.dict(exclude_unset=True).items():
        setattr(pkg, k, v)

    db.commit()
    db.refresh(pkg)
    return pkg

@router.delete("/{package_id}")
def delete_package(package_id: int, db: Session = Depends(get_db)):
    pkg = db.query(Package).filter(Package.package_id == package_id).first()
    if not pkg:
        raise HTTPException(404, "Package not found")

    db.delete(pkg)
    db.commit()
    return {"message": "Package deleted"}
