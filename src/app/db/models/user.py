# src/app/db/models/user.py

from sqlalchemy import Column, String, Boolean, Enum, DateTime
from enum import Enum as PyEnum
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from src.app.db.session import Base

# Define user roles
class UserRole(str, PyEnum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    PATIENT = "patient"


def utc_now():
    return datetime.now(timezone.utc)  # Keep timezone-aware timestamps


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.PATIENT, nullable=False)
    refresh_token = Column(String, nullable=True)  # Store the refresh token

    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    last_updated = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    # One-to-One Relationship with Patient
    patient = relationship("Patient", uselist=False, back_populates="user")
