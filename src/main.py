from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from src.api.auth import router as auth_router
from src.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Zombie Night Delivery API",
    description="Високонавантажена платформа нічної доставки.",
    version="3.0.0",
)

# Підключаємо статичні файли (якщо потрібні картинки або стилі)
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# Підключаємо роути автентифікації
app.include_router(auth_router)


# Головна сторінка MVP (відкриває візуальний HTML-інтерфейс)
@app.get("/", response_class=HTMLResponse)
async def root():
    try:
        with open("src/static/index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return html_content
    except FileNotFoundError:
        return "<h3>Файл інтерфейсу не знайдено. Перевірте папку src/static/index.html</h3>"