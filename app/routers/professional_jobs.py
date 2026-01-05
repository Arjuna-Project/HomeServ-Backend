from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.booking import Booking
from app.models.user import User
from app.models.service import Service

router = APIRouter(prefix="/professionals/jobs", tags=["Professional Jobs"])

@router.get("/my-jobs/{professional_id}")
def my_jobs(professional_id: int, db: Session = Depends(get_db)):

    rows = (
        db.query(
            Booking.booking_id,
            Booking.status,
            Booking.total_price,
            Booking.scheduled_at,
            User.name.label("username"),
            User.user_id,
            Service.name.label("service_name")
        )
        .join(User, Booking.user_id == User.user_id)
        .join(Service, Booking.service_id == Service.service_id)
        .filter(Booking.professional_id == professional_id)
        .all()
    )

    jobs = []
    for r in rows:
        jobs.append({
            "booking_id": r.booking_id,
            "user": r.username if r.username else r.user_id,
            "service": r.service_name,
            "booking_type": (
                f"Scheduled ({r.scheduled_at.strftime('%d %b %Y, %I:%M %p')})"
                if r.scheduled_at else
                "Emergency"
            ),
            "status": r.status,
            "price": float(r.total_price)
        })

    return jobs


