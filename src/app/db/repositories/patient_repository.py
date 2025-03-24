# src/app/db/repositories/patient_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.app.db.models.patient import Patient
import uuid

from fastapi import HTTPException

async def create_patient(db: AsyncSession, user_id: uuid.UUID, patient_data) -> Patient:
    """Create new patient record, ensuring no duplicate exists."""

    # Check if patient record already exists
    result = await db.execute(select(Patient).where(Patient.user_id == user_id))
    existing_patient = result.scalar_one_or_none()

    if existing_patient:
        raise HTTPException(status_code=400, detail="Patient record already exists")

    # Create a new patient record
    new_patient = Patient(user_id=user_id, **patient_data.model_dump())
    db.add(new_patient)
    await db.commit()
    await db.refresh(new_patient)
    return new_patient


async def get_patient_by_user_id(db: AsyncSession, user_id: uuid.UUID) -> Patient:
    """Retrieve patient record by user_id."""
    result = await db.execute(select(Patient).where(Patient.user_id == user_id))
    return result.scalar_one_or_none()

async def update_patient(db: AsyncSession, user_id: uuid.UUID, update_data: dict) -> Patient:
    """Update patient information."""
    patient = await get_patient_by_user_id(db, user_id)
    if not patient:
        return None

    for key, value in update_data.items():
        setattr(patient, key, value)

    await db.commit()
    await db.refresh(patient)
    return patient

async def delete_patient(db: AsyncSession, user_id: uuid.UUID) -> bool:
    """Delete patient information."""
    patient = await get_patient_by_user_id(db, user_id)
    if not patient:
        return False

    await db.delete(patient)
    await db.commit()
    return True
