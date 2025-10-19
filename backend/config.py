from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # 서버 설정
    APP_NAME: str = "Fire Drone Backend"
    VERSION: str = "1.0.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS 설정
    CORS_ORIGINS: list = [
        "http://localhost:5173",
        "http://localhost:8080",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080"
    ]
    
    # PostgreSQL 설정
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""  # 실행 시 입력받음
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "firedrone"
    
    # API 키 (보안)
    API_KEY: str = "your-secret-api-key-change-this"
    
    # WebSocket 설정
    WS_HEARTBEAT_INTERVAL: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def database_url(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()

