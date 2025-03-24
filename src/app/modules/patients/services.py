# src/app/modules/patients/services.py

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.db.repositories.patient_repository import (
    create_patient, get_patient_by_user_id, update_patient, delete_patient
)
from src.app.modules.patients.schemas import PatientCreate, PatientResponse
import uuid


async def create_patient_info(db: AsyncSession, user_id: uuid.UUID, patient: PatientCreate) -> PatientResponse:
    """Create new patient record, ensuring no duplicate exists."""
    patient_record = await create_patient(db, user_id, patient)
    return PatientResponse.model_validate(patient_record)




async def get_patient_info(db: AsyncSession, user_id: uuid.UUID) -> PatientResponse:
    """Retrieve patient information."""
    patient = await get_patient_by_user_id(db, user_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient record not found")
    return PatientResponse.model_validate(patient)

async def update_patient_info(db: AsyncSession, user_id: uuid.UUID, update_data: dict) -> PatientResponse:
    """Update existing patient information."""
    patient = await update_patient(db, user_id, update_data)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient record not found")
    return PatientResponse.model_validate(patient)

async def delete_patient_info(db: AsyncSession, user_id: uuid.UUID) -> dict:
    """Delete a patient record."""
    success = await delete_patient(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Patient record not found")
    return {"message": "Patient record deleted successfully"}
