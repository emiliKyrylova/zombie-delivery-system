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

app.mount("/static", StaticFiles(directory="src/static"), name="static")
app.include_router(auth_router)


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("src/static/index.html", "r", encoding="utf-8") as f:
        return f.read()