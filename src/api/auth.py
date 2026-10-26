from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.security import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    get_password_hash,
    verify_password,
)
from src.models.user import UserModel, UserRole
from src.schemas.user import Token, UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication & Users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# --- Реєстрація ---
@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = (
        db.query(UserModel).filter(UserModel.email == user_data.email).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Користувач із таким email вже існує!"
        )

    hashed_password = get_password_hash(user_data.password)
    new_user = UserModel(
        email=user_data.email,
        hashed_password=hashed_password,
        role=user_data.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# --- Логін (отримання JWT токена) ---
@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невірний email або пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.email, "role": user.role.value}
    )
    return {"access_token": access_token, "token_type": "bearer"}


# --- Залежність для отримання поточного користувача за токеном ---
def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не вдалося перевірити облікові дані",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(UserModel).filter(UserModel.email == email).first()
    if user is None:
        raise credentials_exception
    return user


# --- Домашні сторінки-заглушки (Завдання №6) ---


@router.get("/client/home")
def client_home(current_user: UserModel = Depends(get_current_user)):
    if current_user.role not in [UserRole.CLIENT, UserRole.ADMIN]:
        raise HTTPException(
            status_code=403, detail="Доступ заборонено: потрібні права клієнта"
        )
    return {
        "message": f"Вітаю, виживший {current_user.email}! Це домашня сторінка клієнта."
    }


@router.get("/admin/dashboard")
def admin_dashboard(current_user: UserModel = Depends(get_current_user)):
    # Вертикальне розмежування ролей (Захист адмін-панелі)
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Доступ заборонено: потрібні права адміністратора!",
        )
    return {
        "message": f"Ласкаво просимо в панель управління апокаліпсисом, Адмін {current_user.email}."
    }