# src/app/modules/users/routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.app.modules.users.schemas import UserCreate, UserResponse, UserLogin, Token, TokenRefreshRequest
from src.app.modules.users.services import register_user, authenticate_user
from src.app.db.session import get_db
from src.app.modules.users.repository import validate_refresh_token, get_user_by_email
from src.app.core.security import create_access_token
from src.app.modules.users.repository import get_all_users

router = APIRouter()

@router.get("/list", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db)):
    users = get_all_users(db)
    return users


@router.post("/signup", response_model=UserResponse)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    user = register_user(db, user_data)
    return user

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    tokens = authenticate_user(db, user_data.email, user_data.password)
    return {"access_token": tokens["access_token"], "refresh_token": tokens["refresh_token"], "token_type": "bearer"}

@router.post("/refresh", response_model=Token)
def refresh_token(request: TokenRefreshRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, request.email)  # Fetch user using email
    print(f"# src/app/modules/users/routes.py user {user}")

    if not user or not validate_refresh_token(db, user.email, request.refresh_token):
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Generate new access token
    new_access_token = create_access_token({"sub": user.email})
    return {"access_token": new_access_token, "refresh_token": request.refresh_token, "token_type": "bearer"}

