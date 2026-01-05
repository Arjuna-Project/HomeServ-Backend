import random
import string
from sqlalchemy.orm import Session
from app.models.professionals import Professional


def generate_random_id(length: int = 10):
    """Generate random alphanumeric ID."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def assign_professional(area_id: int, service_id: int, db: Session):
    """Pick the first available professional matching area + service."""
    professional = (
        db.query(Professional)
        .filter(
            Professional.area_id == area_id,
            Professional.service_id == service_id,
            Professional.is_active == True
        )
        .first()
    )

    return professional 
