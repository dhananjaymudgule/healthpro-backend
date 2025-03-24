# src/app/modules/users/services.py

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from email_validator import validate_email, EmailNotValidError

from src.app.modules.users.schemas import (VerifyEmailResponse, UserCreate,
                                           PasswordResetResponse)

from src.app.db.repositories.user_repository import (create_user, get_user_by_email, 
                                                     store_refresh_token)

from src.app.core.security import (verify_password, create_access_token, create_refresh_token,
                                   create_password_reset_token,
                                   create_email_verification_token)

from src.app.tasks.email import send_email  

async def request_email_verification(db: AsyncSession, email: str):
    """Send email verification request."""
    # Check if email is valid (format + domain)
    try:
        validation = validate_email(email, check_deliverability=True)
        email = validation.email  # Normalized email
    except EmailNotValidError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Check if user already exists
    existing_user = await get_user_by_email(db, email)  # ✅ Await async function
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Generate email verification token
    verification_token = create_email_verification_token(email)

    # Send verification email
    verification_link = f"https://yourfrontend.com/verify-email?token={verification_token}"
    await send_email(email_to=email, subject="Verify Your Email", body=f"Click here to verify: {verification_link}")

    return VerifyEmailResponse(message="Verification email sent. Please check your inbox.")

async def register_user(db: AsyncSession, user_data: UserCreate):
    """Register a new user."""
    existing_user = await get_user_by_email(db, user_data.email)  # ✅ Await async function
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return await create_user(db, user_data)  # ✅ Await async function

async def authenticate_user(db: AsyncSession, email: str, password: str):
    """Authenticate user and generate JWT tokens."""
    user = await get_user_by_email(db, email)  # ✅ Await async function
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate JWT access & refresh tokens
    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token()

    # Store refresh token
    await store_refresh_token(db, user.email, refresh_token)  # ✅ Await async function

    return {"access_token": access_token, "refresh_token": refresh_token}

async def request_password_reset(db: AsyncSession, email: str):
    """Send password reset email."""
    user = await get_user_by_email(db, email)  # ✅ Await async function
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    reset_token = create_password_reset_token(email)
    reset_link = f"https://yourfrontend.com/reset-password?token={reset_token}"

    await send_email(email_to=email, subject="Password Reset Request", body=f"Click here to reset your password: {reset_link}")

    return PasswordResetResponse(message="Password reset email sent")
