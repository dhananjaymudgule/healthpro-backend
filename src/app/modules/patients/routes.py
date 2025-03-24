# src/app/modules/patients/routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.db.session import get_db
from src.app.modules.patients import services
from src.app.modules.patients.schemas import PatientCreate, PatientResponse
from src.app.modules.users.dependencies import get_current_user
from src.app.db.models.user import UserRole  


router = APIRouter()


@router.post("/patient", response_model=PatientResponse)
async def create_patient(
    patient: PatientCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)  # 🔐 Require Authentication
):
    """Create a patient record. Only patients can create their own info."""
    
    if current_user.role != UserRole.PATIENT:
        raise HTTPException(status_code=403, detail="Only patients can create patient info")

    return await services.create_patient_info(db, current_user.id, patient)



@router.get("/patient", response_model=PatientResponse)
async def get_patient(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)  # 🔐 Require Authentication
):
    return await services.get_patient_info(db, current_user.id)

@router.put("/patient", response_model=PatientResponse)
async def update_patient(
    update_data: PatientCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)  # 🔐 Require Authentication
):
    return await services.update_patient_info(db, current_user.id, update_data.model_dump())

@router.delete("/patient", response_model=dict)
async def delete_patient(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)  # 🔐 Require Authentication
):
    return await services.delete_patient_info(db, current_user.id)
