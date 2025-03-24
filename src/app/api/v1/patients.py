# src/app/api/v1/patients.py

from fastapi import APIRouter
from src.app.modules.patients.routes import router as patient_routes

router = APIRouter()
router.include_router(patient_routes, tags=["Patients"])
