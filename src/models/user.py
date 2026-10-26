import enum
from sqlalchemy import Boolean, Column, Enum, Integer, String
from src.core.database import Base  # Створимо базовий клас бд нижче


class UserRole(str, enum.Enum):
    CLIENT = "client"
    COURIER = "courier"
    ADMIN = "admin"


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(
        Enum(UserRole), default=UserRole.CLIENT, nullable=False
    )
    is_active = Column(Boolean, default=True)