# src/app/modules/users/file_handler.py

import shutil
from fastapi import UploadFile
from pathlib import Path

from src.app.core.config import settings


# UPLOAD_DIR = Path("uploads")
# UPLOAD_DIR.mkdir(exist_ok=True)

async def process_upload(file: UploadFile, user: dict):
    """
    Processes and saves uploaded PDF/image files for users.
    """
    if file.content_type not in ["application/pdf", "image/png", "image/jpeg"]:
        return {"error": "Invalid file type. Only PDFs and images are allowed."}

    file_path = settings.UPLOAD_DIR / f"{user.id}_{file.filename}"
    
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"message": "File uploaded successfully", "file_path": str(file_path)}
