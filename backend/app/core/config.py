import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "TeraVoo"
    
    # CORS Origins (No wildcard if allow_credentials=True)
    backend_cors_origins_str: str = "http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000,http://127.0.0.1:8000" 

    @property
    def BACKEND_CORS_ORIGINS(self) -> List[str]:
        return [x.strip() for x in self.backend_cors_origins_str.split(",")]

    # Database
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "teravoo")
    
    # Priority to env var (Cloud), fallback to constructed (Local)
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}")

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"

settings = Settings()
