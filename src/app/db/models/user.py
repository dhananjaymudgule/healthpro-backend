# src/app/db/models/user.py

from sqlalchemy import Column, Integer, String, Boolean, Enum
from enum import Enum as PyEnum
import uuid
from sqlalchemy.dialects.postgresql import UUID

from src.app.db.session import Base

# Define user roles
class UserRole(str, PyEnum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    PATIENT = "patient"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.PATIENT, nullable=False)
    refresh_token = Column(String, nullable=True)  # Store the refresh token




