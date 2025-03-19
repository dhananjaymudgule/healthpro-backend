# src/app/modules/users/routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.app.modules.users.schemas import (VerifyEmailRequest,VerifyEmailResponse,
                                           UserCreate, UserResponse, 
                                           UserLogin, Token, TokenRefreshRequest, 
                                           PasswordResetRequest,PasswordResetResponse,
                                           PasswordResetConfirm,
                                           )
from src.app.modules.users.services import (register_user, authenticate_user, request_password_reset,
                                            request_email_verification)
from src.app.db.session import get_db
from src.app.modules.users.repository import get_user_by_email, get_all_users
from src.app.modules.users.repository import get_user_by_refresh_token 
from src.app.modules.users.repository import clear_refresh_token
from src.app.core.security import create_access_token, verify_refresh_token
from src.app.modules.users.dependencies import get_current_user, is_admin

from src.app.core.security import (hash_password, verify_password_reset_token, 
                                   create_email_verification_token,
                                   verify_email_verification_token)
from src.app.tasks.email import send_email  


router = APIRouter()


# User signup
# @router.post("/signup", response_model=UserResponse)
# def signup(user_data: UserCreate, db: Session = Depends(get_db)):
#     user = register_user(db, user_data)
#     return user

@router.post("/verify-email", response_model=VerifyEmailResponse)
async def verify_email(request: VerifyEmailRequest, db: Session = Depends(get_db)):
    return await request_email_verification(db, request.email)


@router.post("/signup", response_model=UserResponse)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Verify email using the token and create a user in the database.
    """
    # register user
    user = register_user(db, user_data)

    return user


# User login
@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    tokens = authenticate_user(db, user_data.email, user_data.password)
    return {"access_token": tokens["access_token"], "refresh_token": tokens["refresh_token"], "token_type": "bearer"}


# user log out
@router.post("/logout")
def logout(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Logs out the user by clearing their refresh token from the database.
    """
    clear_refresh_token(db, current_user.email)  # Remove refresh token
    return {"message": "Successfully logged out"}


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


@router.post("/password-reset", response_model=PasswordResetResponse)
async def password_reset_request(request: PasswordResetRequest, db: Session = Depends(get_db)):
    return await request_password_reset(db, request.email)


@router.post("/password-reset/confirm", response_model=dict)
def password_reset_confirm(request: PasswordResetConfirm, db: Session = Depends(get_db)):
    email = verify_password_reset_token(request.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = hash_password(request.new_password)
    db.commit()
    return {"message": "Password has been reset successfully"}



