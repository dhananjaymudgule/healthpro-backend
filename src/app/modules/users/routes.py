# src/app/modules/users/routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.app.modules.users.schemas import UserCreate, UserResponse, UserLogin, Token, TokenRefreshRequest
from src.app.modules.users.services import register_user, authenticate_user
from src.app.db.session import get_db
from src.app.modules.users.repository import get_user_by_email, get_all_users
from src.app.modules.users.repository import get_user_by_refresh_token  
from src.app.core.security import create_access_token, verify_refresh_token
from src.app.modules.users.dependencies import get_current_user, is_admin

router = APIRouter()


# User signup
@router.post("/signup", response_model=UserResponse)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    user = register_user(db, user_data)
    return user

# User login
@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    tokens = authenticate_user(db, user_data.email, user_data.password)
    return {"access_token": tokens["access_token"], "refresh_token": tokens["refresh_token"], "token_type": "bearer"}

# Refresh access token
@router.post("/refresh", response_model=Token)
def refresh_token(request: TokenRefreshRequest, db: Session = Depends(get_db)):
    user = get_user_by_refresh_token(db, request.refresh_token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Verify token
    user_email = verify_refresh_token(request.refresh_token, user)

    # Generate new access token
    new_access_token = create_access_token({"sub": user_email})
    return {"access_token": new_access_token, "refresh_token": request.refresh_token, "token_type": "bearer"}


# Get current user profile
@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active
    }


# Admin dashboard - Restricted to admins
@router.get("/admin", response_model=dict)
def get_admin_dashboard(admin=Depends(is_admin)):
    return {
        "message": "Welcome, Admin!",
        "user": {
            "id": admin.id,
            "name": admin.name,
            "email": admin.email,
            "role": admin.role
        }
    }


# List all users (Admin-Only)
@router.get("/list", response_model=List[UserResponse])
def list_users(admin=Depends(is_admin), db: Session = Depends(get_db)):
    users = get_all_users(db)
    return users


