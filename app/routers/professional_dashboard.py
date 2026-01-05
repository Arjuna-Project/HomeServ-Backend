from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.booking import Booking

router = APIRouter(prefix="/professionals/dashboard", tags=["Professional Dashboard"])


@router.get("/{professional_id}")
def get_dashboard(professional_id: int, db: Session = Depends(get_db)):

    pending_jobs = db.query(Booking).filter(
        Booking.professional_id == professional_id,
        Booking.status == "pending"
    ).count()

    completed_jobs = db.query(Booking).filter(
        Booking.professional_id == professional_id,
        Booking.status == "completed"
    ).count()

    earnings_rows = db.query(Booking.total_price).filter(
        Booking.professional_id == professional_id,
        Booking.status == "completed"
    ).all()

    total_earnings = sum(row[0] for row in earnings_rows if row[0])

    return {
        "pending_jobs": pending_jobs,
        "completed_jobs": completed_jobs,
        "total_earnings": total_earnings
    }
