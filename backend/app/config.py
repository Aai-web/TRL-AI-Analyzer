"""Application Configuration Settings."""

import os
from typing import List

class Settings:
    APP_NAME: str = "TRL Intelligence"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]
    UPLOAD_MAX_SIZE_MB: int = int(os.getenv("UPLOAD_MAX_SIZE_MB", "25"))
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".txt"]

settings = Settings()
