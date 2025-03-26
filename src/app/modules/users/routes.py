# src/app/modules/users/routes.py

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi.security import OAuth2PasswordRequestForm


from src.app.modules.users.schemas import (
    VerifyEmailRequest, VerifyEmailResponse,
    UserCreate, UserResponse, 
    UserLogin, Token, TokenRefreshRequest, 
    PasswordResetRequest, PasswordResetResponse,
    PasswordResetConfirm
)

from src.app.modules.users.services import (
    register_user, 
    authenticate_user, 
    request_password_reset,
    request_email_verification
)

from src.app.db.repositories.user_repository import (
    get_user_by_email, 
    get_all_users,
    get_user_by_refresh_token,
    clear_refresh_token
)

from src.app.modules.users.dependencies import (
    get_current_user, is_admin
)

from src.app.core.security import (
    create_access_token, verify_refresh_token,
    hash_password, verify_password_reset_token
)

from src.app.db.session import get_db
from src.app.modules.users import file_handler

from src.app.core.logging_config import user_logger  


router = APIRouter()

@router.post("/verify-email", response_model=VerifyEmailResponse)
async def verify_email(request: VerifyEmailRequest, db: AsyncSession = Depends(get_db)):
    return await request_email_verification(db, request.email)


@router.post("/signup", response_model=UserResponse)
async def signup(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Verify email using the token and create a user in the database.
    """
    return await register_user(db, user_data)

# User login
@router.post("/login", response_model=Token)
async def login(user_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # OAuth2PasswordRequestForm uses username instead of email
    # user_data.username is used instead of user_data.email  
    tokens = await authenticate_user(db, user_data.username , user_data.password)
    return {"access_token": tokens["access_token"], "refresh_token": tokens["refresh_token"], "token_type": "bearer"}



# User logout
@router.post("/logout")
async def logout(current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """
    Logs out the user by clearing their refresh token from the database.
    """
    await clear_refresh_token(db, current_user.email)  # Remove refresh token
    return {"message": "Successfully logged out"}

# Refresh access token
@router.post("/refresh", response_model=Token)
async def refresh_token(request: TokenRefreshRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_refresh_token(db, request.refresh_token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Verify token
    user_email = verify_refresh_token(request.refresh_token, user)

    # Generate new access token
    new_access_token = create_access_token({"sub": user_email})
    return {"access_token": new_access_token, "refresh_token": request.refresh_token, "token_type": "bearer"}

# Get current user profile
@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active
    }

# Admin dashboard - Restricted to admins
@router.get("/admin", response_model=dict)
async def get_admin_dashboard(admin=Depends(is_admin)):
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
async def list_users(admin=Depends(is_admin), db: AsyncSession = Depends(get_db)):
    return await get_all_users(db)

@router.post("/password-reset", response_model=PasswordResetResponse)
async def password_reset_request(request: PasswordResetRequest, db: AsyncSession = Depends(get_db)):
    return await request_password_reset(db, request.email)

@router.post("/password-reset/confirm", response_model=dict)
async def password_reset_confirm(request: PasswordResetConfirm, db: AsyncSession = Depends(get_db)):
    email = verify_password_reset_token(request.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = await get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = hash_password(request.new_password)
    await db.commit()
    return {"message": "Password has been reset successfully"}

@router.post("/upload-file/", tags=["Users"])
async def upload_file(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)  # Ensuring only logged-in users
):
    """
    Upload a file (PDF/Image) for a logged-in user.
    """
    return await file_handler.process_upload(file, current_user)
