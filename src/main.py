from fastapi import FastAPI

app = FastAPI(
    title="Zombie Night Delivery API",
    description=(
        "Високонавантажена платформа динамічної маршрутизації для нічної" " доставки."
    ),
    version="1.0.0",
)


@app.get("/")
async def root():
    return {
        "message": (
            "Мозки не знайдено, але сервер працює! Агрегатор нічної"
            " доставки зомбі активний."
        )
    }
