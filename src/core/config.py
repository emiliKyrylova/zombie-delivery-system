from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Zombie Night Delivery Aggregator"
    DATABASE_URL: str = "postgresql+psycopg2://user:password@localhost:5432/zombie_db"

    class Config:
        env_file = ".env"


settings = Settings()
