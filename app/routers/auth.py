from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserOut, UserLogin
from app.models.user import User
from app.core.database import get_db
from app.core.security import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=UserOut)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(400, "Email already registered")

    user = User(
        name=user_data.name,
        email=user_data.email,
        phone=user_data.phone,
        address=user_data.address,
        password_hash=hash_password(user_data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(404, "User not found")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(400, "Invalid credentials")

    return {
        "message": "Login successful",
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email
    }
