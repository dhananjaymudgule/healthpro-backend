# src/app/db/repositories/patient_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from src.app.db.models.patient import Patient
import uuid
from datetime import datetime, timezone
from fastapi import HTTPException

async def create_patient(db: AsyncSession, user_id: uuid.UUID, patient_data) -> Patient:
    """
    Create or update a patient record.
    - If patient exists, update the record.
    - If no record exists, create a new one.
    """

    # Check if patient record already exists
    result = await db.execute(select(Patient).where(Patient.user_id == user_id))
    existing_patient = result.scalar_one_or_none()

    if existing_patient:
        # Update existing patient record
        for key, value in patient_data.items():
            setattr(existing_patient, key, value)

        existing_patient.last_updated = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(existing_patient)
        return existing_patient

    # Create a new patient record
    new_patient = Patient(
        user_id=user_id,
        created_at=datetime.now(timezone.utc),
        last_updated=datetime.now(timezone.utc),
        **patient_data
    )
    db.add(new_patient)
    await db.commit()
    await db.refresh(new_patient)
    return new_patient


async def get_patient_info(db: AsyncSession, user_id: uuid.UUID) -> Patient:
    """
    Retrieve patient record by user_id.
    Returns None if patient not found.
    """
    result = await db.execute(select(Patient).where(Patient.user_id == user_id))
    return result.scalar_one_or_none()


async def update_patient(db: AsyncSession, user_id: uuid.UUID, update_data: dict) -> Patient:
    """
    Update patient information, setting `last_updated` timestamp.
    Returns updated patient record.
    """
    patient = await get_patient_info(db, user_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient record not found")

    for key, value in update_data.items():
        setattr(patient, key, value)

    patient.last_updated = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(patient)
    return patient


async def delete_patient(db: AsyncSession, user_id: uuid.UUID) -> bool:
    """
    Delete patient record by user_id.
    Returns True if deleted, False if patient not found.
    """
    patient = await get_patient_info(db, user_id)
    if not patient:
        return False

    await db.delete(patient)
    await db.commit()
    return True
