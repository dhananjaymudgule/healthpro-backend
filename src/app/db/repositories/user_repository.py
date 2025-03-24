# src/app/db/repositories/user_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.app.db.models.user import User
from src.app.modules.users.schemas import UserCreate
from src.app.core.security import hash_password

async def create_user(db: AsyncSession, user_data: UserCreate):
    """Create a new user and hash their password."""
    hashed_password = hash_password(user_data.password)
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password,
        role=user_data.role
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user_by_email(db: AsyncSession, email: str):
    """Fetch a user by email."""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def get_user_by_refresh_token(db: AsyncSession, refresh_token: str):
    """Fetch a user by their refresh token."""
    result = await db.execute(select(User).where(User.refresh_token == refresh_token))
    return result.scalar_one_or_none()

async def store_refresh_token(db: AsyncSession, email: str, refresh_token: str):
    """Store a refresh token for a user."""
    user = await get_user_by_email(db, email)
    if user:
        print(f"Storing refresh token: {refresh_token} for user: {email}")
        user.refresh_token = refresh_token
        await db.commit()
        await db.refresh(user)

async def clear_refresh_token(db: AsyncSession, email: str):
    """Clears the stored refresh token for the given user."""
    user = await get_user_by_email(db, email)
    if user:
        user.refresh_token = None  # Remove token
        await db.commit()

async def validate_refresh_token(db: AsyncSession, email: str, refresh_token: str) -> bool:
    """Validate if a given refresh token matches the stored one."""
    user = await get_user_by_email(db, email)
    if user and user.refresh_token == refresh_token:
        return True
    return False

async def get_all_users(db: AsyncSession):
    """Retrieve all users."""
    result = await db.execute(select(User))
    return result.scalars().all()
