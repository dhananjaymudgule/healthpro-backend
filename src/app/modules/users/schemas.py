# src/app/modules/users/schemas.py

from pydantic import BaseModel, EmailStr
from uuid import UUID
from src.app.db.models.user import UserRole  


from pydantic import BaseModel, EmailStr, Field
from src.app.db.models.user import UserRole

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

    class Config:
        from_attributes = True

# log in request schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str

#log in response schema
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

# logout  Response schema
class LogoutResponse(BaseModel):
    message: str

# refresh token schema
class TokenRefreshRequest(BaseModel):
    refresh_token: str


# password reset request
class PasswordResetRequest(BaseModel):
    email: EmailStr

# password reset response
class PasswordResetResponse(BaseModel):
    message: str

# password reset confirm schema
class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str



