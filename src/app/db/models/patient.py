# src/app/db/models/patient.py

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum as PyEnum
import uuid
from datetime import datetime, timezone
from src.app.db.session import Base

# Enum for Smoking Status
class SmokingStatus(str, PyEnum):
    NEVER = "never"
    FORMER = "former"
    CURRENT = "current"

# Enum for Diabetes Status
class DiabetesStatus(str, PyEnum):
    NO = "no"
    TYPE_1 = "type_1"
    TYPE_2 = "type_2"


def utc_now():
    return datetime.now(timezone.utc)  # Keep timezone-aware timestamps

class Patient(Base):
    __tablename__ = "patients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    gender = Column(String, nullable=False)  # Example: "Male", "Female", "Other"
    date_of_birth = Column(Date, nullable=False)
    height_cm = Column(Integer, nullable=False)
    weight_kg = Column(Integer, nullable=False)
    sbp = Column(Integer, nullable=False)  # Systolic Blood Pressure
    smoking_status = Column(Enum(SmokingStatus), nullable=False)
    diabetes_status = Column(Enum(DiabetesStatus), nullable=False)
    total_cholesterol_level = Column(Integer, nullable=False)  # mg/dL

    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    last_updated = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)
    
    # Relationship with User model
    user = relationship("User", back_populates="patient")
