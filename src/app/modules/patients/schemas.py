# src/app/module/patients/schemas.py

from pydantic import BaseModel, ConfigDict
from datetime import date
from enum import Enum
from uuid import UUID

class SmokingStatus(str, Enum):
    NEVER = "never"
    FORMER = "former"
    CURRENT = "current"

class DiabetesStatus(str, Enum):
    NO = "no"
    TYPE_1 = "type_1"
    TYPE_2 = "type_2"

class PatientCreate(BaseModel):
    gender: str
    date_of_birth: date
    height_cm: int
    weight_kg: int
    sbp: int
    smoking_status: SmokingStatus
    diabetes_status: DiabetesStatus
    total_cholesterol_level: int

    model_config = ConfigDict(from_attributes=True)  #  Pydantic ORM mode

class PatientResponse(PatientCreate):
    id: UUID
    user_id: UUID
