# src/app/modules/users/routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.app.modules.users.schemas import UserCreate, UserResponse
from src.app.modules.users.services import create_user
from src.app.db.session import get_db

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, user_data)
    return user
