# src/app/db/models/user.py

from sqlalchemy import Column, Integer, String, Boolean, Enum
from enum import Enum as PyEnum
from src.app.db.session import Base

# Define user roles
class UserRole(str, PyEnum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    PATIENT = "patient"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.PATIENT, nullable=False)
    refresh_token = Column(String, nullable=True)  # Store the refresh token
