# src/app/modules/users/services.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.app.modules.users.repository import create_user, get_user_by_email, store_refresh_token, validate_refresh_token
from src.app.modules.users.schemas import UserCreate
from src.app.core.security import verify_password, create_access_token, create_refresh_token

def register_user(db: Session, user_data: UserCreate):
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user_data)

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate JWT access & refresh tokens
    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token()

    # Store refresh token
    store_refresh_token(db, user.email, refresh_token)

    return {"access_token": access_token, "refresh_token": refresh_token}

