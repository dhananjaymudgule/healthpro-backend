# src/app/modules/users/file_handler.py

import aiofiles
from fastapi import UploadFile
from pathlib import Path
from src.app.core.config import settings

async def process_upload(file: UploadFile, user: dict):
    """
    Processes and saves uploaded PDF/image files for users.
    """
    if file.content_type not in ["application/pdf", "image/png", "image/jpeg"]:
        return {"error": "Invalid file type. Only PDFs and images are allowed."}

    file_path = settings.UPLOAD_DIR / f"{user.id}_{file.filename}"

    #  Use async file writing
    async with aiofiles.open(file_path, "wb") as buffer:
        while chunk := await file.read(1024):  # Read in chunks asynchronously
            await buffer.write(chunk)

    return {"message": "File uploaded successfully", "file_path": str(file_path)}
