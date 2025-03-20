# src/app/modules/users/services.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from email_validator import validate_email, EmailNotValidError

from src.app.modules.users.schemas import (VerifyEmailResponse, UserCreate,
                                           PasswordResetResponse)

from src.app.modules.users.repository import create_user, get_user_by_email, store_refresh_token, validate_refresh_token
from src.app.core.security import (verify_password, create_access_token, create_refresh_token,
                                   create_password_reset_token,
                                   create_email_verification_token)
from src.app.tasks.email import send_email  


async def request_email_verification(db: Session, email: str):
    # Check if email is valid (format + domain)
    try:
        validation = validate_email(email, check_deliverability=True)
        email = validation.email  # Normalized email
    except EmailNotValidError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Check if user already exists
    existing_user = get_user_by_email(db, email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Generate email verification token
    verification_token = create_email_verification_token(email)

    # Send verification email
    verification_link = f"https://yourfrontend.com/verify-email?token={verification_token}"
    await send_email(email_to=email, subject="Verify Your Email", body=f"Click here to verify: {verification_link}")

    return VerifyEmailResponse(message="Verification email sent. Please check your inbox.")


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



async def request_password_reset(db: Session, email: str):
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    reset_token = create_password_reset_token(email)
    print(f"Password Reset Token: {reset_token}")
    reset_link = f"https://yourfrontend.com/reset-password?token={reset_token}"

    await send_email(email_to=email, subject="Password Reset Request", body=f"Click here to reset your password: {reset_link}")
    # return {"message": "Password reset email sent"}
    return PasswordResetResponse(message="Password reset email sent")
