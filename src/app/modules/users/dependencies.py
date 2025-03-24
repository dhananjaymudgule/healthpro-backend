# src/app/modules/users/dependencies.py

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.db.session import get_db
from src.app.core.security import verify_access_token
from src.app.db.repositories.user_repository import get_user_by_email
from src.app.db.models.user import UserRole

#  Async Dependency to get the current user from token
async def get_current_user(token: str, db: AsyncSession = Depends(get_db)):
    email = verify_access_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = await get_user_by_email(db, email)  # ✅ Await async DB query
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

#  Async Dependency to check if user is a doctor
async def is_doctor(user=Depends(get_current_user)):
    if user.role != UserRole.DOCTOR:
        raise HTTPException(status_code=403, detail="Only doctors can perform this action")
    return user

#  Async Dependency to check if user is a patient
async def is_patient(user=Depends(get_current_user)):
    if user.role != UserRole.PATIENT:
        raise HTTPException(status_code=403, detail="Only patients can perform this action")
    return user

#  Async Dependency to check if user is an admin
async def is_admin(user=Depends(get_current_user)):
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can perform this action")
    return user
