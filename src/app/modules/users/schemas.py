# src/app/modules/users/schemas.py

from pydantic import BaseModel, EmailStr
from uuid import UUID

from pydantic import BaseModel, EmailStr
from typing import Optional
from src.app.db.models.user import UserRole  # Import UserRole Enum

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.PATIENT  # Default role is PATIENT


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    is_active: bool
    role: UserRole  # Return role in response

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenRefreshRequest(BaseModel):
    refresh_token: str


