# src/app/modules/users/services.py

from sqlalchemy.orm import Session
from src.app.modules.users.models import User
from src.app.modules.users.schemas import UserCreate
from src.app.core.security import hash_password

def create_user(db: Session, user_data: UserCreate):
    hashed_password = hash_password(user_data.password)
    new_user = User(name=user_data.name, email=user_data.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
