from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from src.core.database import Base, get_db
from src.main import app
from src.models.user import UserModel  # Імпорт моделі обов'язковий

# Використовуємо файл для тестів або пам'ять з єдиним потоком
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


@pytest.fixture(autouse=True)
def setup_database():
    """Створює і повністю очищує базу даних перед кожним тестом."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_register_and_login():
    response = client.post(
        "/auth/register",
        json={
            "email": "survivor@zombie.com",
            "password": "securepassword123",
            "role": "client",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "survivor@zombie.com"
    assert data["role"] == "client"

    response = client.post(
        "/auth/login",
        data={
            "username": "survivor@zombie.com",
            "password": "securepassword123",
        },
    )
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"


def test_unauthorized_access():
    response = client.get("/auth/client/home")
    assert response.status_code == 401


def test_vertical_privilege_escalation():
    client.post(
        "/auth/register",
        json={
            "email": "client_test@zombie.com",
            "password": "password123",
            "role": "client",
        },
    )

    login_res = client.post(
        "/auth/login",
        data={
            "username": "client_test@zombie.com",
            "password": "password123",
        },
    )
    token = login_res.json()["access_token"]

    response = client.get(
        "/auth/admin/dashboard", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403


def test_admin_access():
    client.post(
        "/auth/register",
        json={
            "email": "admin_boss@zombie.com",
            "password": "adminpassword123",
            "role": "admin",
        },
    )

    login_res = client.post(
        "/auth/login",
        data={
            "username": "admin_boss@zombie.com",
            "password": "adminpassword123",
        },
    )
    token = login_res.json()["access_token"]

    response = client.get(
        "/auth/admin/dashboard", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "Ласкаво просимо в панель управління" in response.json()["message"]