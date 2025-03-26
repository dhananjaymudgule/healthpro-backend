# src/app/core/config.py

from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path


class Settings(BaseSettings):

    # Base directory (Project root)
    BASE_DIR: Path = Path(__file__).resolve().parents[1]  # Go 4 levels up
    # print(f"BASE_DIR: {BASE_DIR}")
    
    # Upload directory
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # Ensure upload directory exists

    
    # General settings
    VERSION: str 
    HOST: str 
    PORT: int 
    PROJECT_NAME: str 
    PROJECT_DESCRIPTION: str 

    API_VERSION: str

    # db
    DATABASE_URL: str
    # db url parsed
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    MONGO_DB_URI: str

    # security
    ALGORITHM: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int 
    REFRESH_TOKEN_EXPIRE_DAYS: int
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int
    EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES: int

    # email config
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool
    USE_CREDENTIALS: bool


    # API Keys
    GEMINI_API_KEY: str
    GEMINI_LLM_MODEL_NAME: str

    # params
    

    class Config:
        env_file = ".env"

settings = Settings()
