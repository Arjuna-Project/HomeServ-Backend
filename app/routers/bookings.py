from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.booking import BookingCreate, BookingOut, BookingUpdate
from app.services.bookings import create_booking_service, update_booking_status
from app.models.booking import Booking
from app.core.database import get_db

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)

# ======================================================
# CREATE BOOKING (FINAL, SINGLE SOURCE OF TRUTH)
# ======================================================
@router.post("/", response_model=BookingOut)
def create_booking(data: BookingCreate, db: Session = Depends(get_db)):

    # ✅ PACKAGE BOOKING
    if data.package_id:
        if data.service_id or data.professional_id:
            raise HTTPException(
                status_code=400,
                detail="Invalid package booking"
            )

    # ✅ NORMAL / EMERGENCY BOOKING
    else:
        if not data.service_id:
            raise HTTPException(
                status_code=400,
                detail="Service must be selected"
            )
        if not data.professional_id:
            raise HTTPException(
                status_code=400,
                detail="Professional must be selected"
            )

    return create_booking_service(data, db)

# ======================================================
# GET ALL BOOKINGS (ADMIN)
# ======================================================
@router.get("/", response_model=list[BookingOut])
def get_all_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).all()

# ======================================================
# GET BOOKINGS BY USER
# ======================================================
@router.get("/user/{user_id}", response_model=list[BookingOut])
def get_user_bookings(user_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Booking)
        .filter(Booking.user_id == user_id)
        .order_by(Booking.created_at.desc())
        .all()
    )

# ======================================================
# GET PACKAGE BOOKINGS
# ======================================================
@router.get("/user/{user_id}/packages", response_model=list[BookingOut])
def get_user_package_bookings(user_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Booking)
        .filter(
            Booking.user_id == user_id,
            Booking.package_id.isnot(None)
        )
        .order_by(Booking.created_at.desc())
        .all()
    )

# ======================================================
# GET NORMAL BOOKINGS
# ======================================================
@router.get("/user/{user_id}/normal", response_model=list[BookingOut])
def get_user_normal_bookings(user_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Booking)
        .filter(
            Booking.user_id == user_id,
            Booking.package_id.is_(None)
        )
        .order_by(Booking.created_at.desc())
        .all()
    )

# ======================================================
# GET BOOKING BY ID
# ======================================================
@router.get("/{booking_id}", response_model=BookingOut)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(404, "Booking not found")
    return booking

# ======================================================
# COMPLETE JOB
# ======================================================
@router.put("/{booking_id}/complete")
def complete_job(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(404, "Job not found")

    booking.status = "completed"
    db.commit()
    return {"message": "Job marked as completed"}

# ======================================================
# UPDATE BOOKING
# ======================================================
@router.put("/{booking_id}", response_model=BookingOut)
def update_booking(
    booking_id: int,
    data: BookingUpdate,
    db: Session = Depends(get_db)
):
    booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(404, "Booking not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(booking, key, value)

    db.commit()
    db.refresh(booking)
    return booking

# ======================================================
# CHANGE STATUS
# ======================================================
@router.patch("/{booking_id}/status", response_model=BookingOut)
def change_status(booking_id: int, status: str, db: Session = Depends(get_db)):

    if status not in ["pending", "cancelled", "completed"]:
        raise HTTPException(400, "Invalid status")

    return update_booking_status(booking_id, status, db)

# ======================================================
# DELETE BOOKING
# ======================================================
@router.delete("/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(404, "Booking not found")

    db.delete(booking)
    db.commit()
    return {"message": "Booking deleted successfully"}
