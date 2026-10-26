# --- Етап 1: Збирання залежностей (Builder) ---
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Встановлюємо залежності у спеціальну директорію
RUN pip install --no-cache-dir --user -r requirements.txt

# --- Етап 2: Фінальний легкий образ ---
FROM python:3.11-slim

WORKDIR /app

# Копіюємо тільки встановлені пакети з першого етапу (виключаємо компілятори)
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]