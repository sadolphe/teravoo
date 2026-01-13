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
    # Priority to env var (Cloud), fallback to constructed (Local)
    DATABASE_URL: str | None = None

    def __init__(self, **values):
        super().__init__(**values)
        if not self.DATABASE_URL:
            # Fallback for local
            self.DATABASE_URL = f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
        
        # Determine if overwrite needed for Render (postgres:// -> postgresql://)
        if self.DATABASE_URL and self.DATABASE_URL.startswith("postgres://"):
            self.DATABASE_URL = self.DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)


    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"

settings = Settings()
