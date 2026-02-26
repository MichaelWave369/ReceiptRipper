from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from receiptrip.auth import create_access_token, get_current_user, hash_password, verify_password
from receiptrip.db import get_db
from receiptrip.models import User
from receiptrip.schemas import LoginIn, Token, UserCreate, UserOut

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    user = User(email=payload.email, password_hash=hash_password(payload.password), default_currency=payload.default_currency)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return Token(access_token=create_access_token(user.email))


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
