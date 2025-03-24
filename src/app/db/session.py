# src/app/db/session.py

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.app.core.config import settings

# # Ensure database URL uses asyncpg (not psycopg2)
# DATABASE_URL = settings.DATABASE_URL.replace("postgresql+psycopg2", "postgresql+asyncpg")

# Create async engine
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

# Create async session
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Keep using Base for SQLAlchemy models
Base = declarative_base()

# Dependency for async database session
async def get_db():
    async with SessionLocal() as session:
        yield session



