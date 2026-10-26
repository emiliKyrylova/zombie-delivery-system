# Zombie Night Delivery System 🧟‍♂️

Високонавантажена платформа динамічної маршрутизації для нічної доставки.

## ⚙️ Інструкція з запуску середовищ (Sandbox / Production)

Проєкт підтримує розділення конфігурацій для тестового та робочого середовищ за допомогою змінних оточення та `pydantic-settings`.

### 1. Запуск у тестовому середовищі (Sandbox)
За замовчуванням застосунок запускається в режимі Sandbox (`DEBUG = True`, ізольована тестова база даних).
```bash
uvicorn src.main:app --reload
```

### 2. Запуск у робочому середовищі (Production)
Для запуску в production-режимі (DEBUG = False, робоча БД) встановіть змінну середовища ENVIRONMENT:
У Windows PowerShell:
```bash
$env:ENVIRONMENT="production"; uvicorn src.main:app
```
У Linux / macOS:
```bash
ENVIRONMENT=production uvicorn src.main:app
```
