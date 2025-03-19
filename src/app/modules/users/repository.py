# src/app/modules/users/repository.py

from sqlalchemy.orm import Session
from src.app.db.models.user import User
from src.app.modules.users.schemas import UserCreate
from src.app.core.security import hash_password

def create_user(db: Session, user_data: UserCreate):
    hashed_password = hash_password(user_data.password)
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password,
        role=user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_refresh_token(db: Session, refresh_token: str):
    return db.query(User).filter(User.refresh_token == refresh_token).first()

def store_refresh_token(db: Session, email: str, refresh_token: str):
    user = get_user_by_email(db, email)
    if user:
        print(f"Storing refresh token: {refresh_token} for user: {email}")
        user.refresh_token = refresh_token
        db.commit()
        db.refresh(user)  # Ensure the latest data is fetched

def clear_refresh_token(db: Session, email: str):
    """
    Clears the stored refresh token for the given user.
    """
    user = get_user_by_email(db, email)
    if user:
        user.refresh_token = None  # Remove token
        db.commit()

def validate_refresh_token(db: Session, email: str, refresh_token: str) -> bool:
    user = get_user_by_email(db, email)
    print(f"Stored Token: {user.refresh_token},\nProvided Token: {refresh_token}")
    if user and user.refresh_token == refresh_token:
        return True
    return False

def get_all_users(db: Session):
    return db.query(User).all()

