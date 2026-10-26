from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Використовуємо SQLite для простоти в лабораторній
SQLALCHEMY_DATABASE_URL = "sqlite:///./zombie_delivery.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()