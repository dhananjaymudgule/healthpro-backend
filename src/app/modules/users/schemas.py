# src/app/modules/users/schemas.py

from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from src.app.db.models.user import UserRole  

# Pydantic v2 Fix: Use `ConfigDict(from_attributes=True)` instead of `Config.from_attributes`

# Email Verification Request
class VerifyEmailRequest(BaseModel):
    email: EmailStr

# Schema for email verification response
class VerifyEmailResponse(BaseModel):
    message: str

# User Signup After Email is Verified
class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr  # Email already verified before this step
    password: str = Field(..., min_length=8, max_length=100, description="Must be at least 8 characters")
    role: UserRole = UserRole.PATIENT  # Default role is PATIENT
    token: str  #  User must provide the verification token received via email

class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    is_active: bool
    role: UserRole  # Return role in response

    model_config = {"from_attributes": True}  # ✅ Pydantic v2 Fix

# Log in request schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Log in response schema
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

# Logout response schema
class LogoutResponse(BaseModel):
    message: str

# Refresh token schema
class TokenRefreshRequest(BaseModel):
    refresh_token: str

# Password reset request
class PasswordResetRequest(BaseModel):
    email: EmailStr

# Password reset response
class PasswordResetResponse(BaseModel):
    message: str

# Password reset confirm schema
class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
