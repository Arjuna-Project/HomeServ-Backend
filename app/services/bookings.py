from sqlalchemy.orm import Session
from app.models.booking import Booking
from app.schemas.booking import BookingCreate

def create_booking_service(data: BookingCreate, db: Session):

    booking = Booking(
        user_id=data.user_id,
        area_id=data.area_id,

        package_id=data.package_id,
        service_id=data.service_id,
        professional_id=data.professional_id,

        scheduled_at=data.scheduled_at,
        total_price=data.total_price,
        details=data.details,
        status="pending"
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def update_booking_status(booking_id: int, status: str, db: Session):
    booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    booking.status = status
    db.commit()
    db.refresh(booking)
    return booking
