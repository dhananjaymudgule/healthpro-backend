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

    # basic
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # Token expiry

    # email config
    EMAIL_SENDER: str
    EMAIL_PASSWORD: str
    SMTP_SERVER: str   
    SMTP_PORT: int  


    # API Keys
    GEMINI_API_KEY: str
    GEMINI_LLM_MODEL_NAME: str

    # params
    

    class Config:
        env_file = ".env"

settings = Settings()
