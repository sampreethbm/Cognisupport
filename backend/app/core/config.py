import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "CogniSupport"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # Database
    # Default to SQLite for local development if not set
    DATABASE_URL: str = "sqlite:///./sql_app.db"

    # ML Model
    MODEL_PATH: str = "model.joblib"

    class Config:
        case_sensitive = True

settings = Settings()
