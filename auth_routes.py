from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserRegister, UserLogin
from app.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
)

router = APIRouter()


@router.post("/register")
def register(
    user: UserRegister,
    db: Session = Depends(get_db),
):
    new_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    db.add(new_user)
    db.commit()

    return {"message": "User Registered Successfully"}


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        return {"error": "Invalid Credentials"}

    if not verify_password(user.password, db_user.password):
        return {"error": "Invalid Credentials"}

    token = create_access_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer",
    }
