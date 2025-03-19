# src/app/core/config.py

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    
    # General settings
    VERSION: str 
    HOST: str 
    PORT: int 
    PROJECT_NAME: str 
    PROJECT_DESCRIPTION: str 

    # db
    DATABASE_URL: str

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
