# src/app/api/v1/users.py

from fastapi import APIRouter
from src.app.modules.users.routes import router as user_routes

# Create an APIRouter instance
router = APIRouter()

# Include all user-related routes from modules/users/routes.py
router.include_router(user_routes, tags=["Users"])


