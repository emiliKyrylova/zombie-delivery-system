import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Zombie Night Delivery"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./zombie_delivery.db"

    class Config:
        # Читаємо залежно від системної змінної ENVIRONMENT (sandbox або production)
        env_file = (
            ".env.production"
            if os.getenv("ENVIRONMENT") == "production"
            else ".env.sandbox"
        )
        env_file_encoding = "utf-8"


settings = Settings()