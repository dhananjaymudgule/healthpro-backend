# src/app/modules/users/dependencies.py

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from src.app.db.session import get_db
from src.app.core.security import verify_access_token
from src.app.modules.users.repository import get_user_by_email
from src.app.db.models.user import UserRole

# Dependency to get the current user from token
def get_current_user(token: str, db: Session = Depends(get_db)):
    email = verify_access_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    # email = payload.get("sub")
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

# Dependency to check if user is a doctor
def is_doctor(user=Depends(get_current_user)):
    if user.role != UserRole.DOCTOR:
        raise HTTPException(status_code=403, detail="Only doctors can perform this action")
    return user

# Dependency to check if user is a patient
def is_patient(user=Depends(get_current_user)):
    if user.role != UserRole.PATIENT:
        raise HTTPException(status_code=403, detail="Only patients can perform this action")
    return user

# Dependency to check if user is an admin
def is_admin(user=Depends(get_current_user)):
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can perform this action")
    return user
