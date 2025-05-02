# Используем легкий образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код бэкенда и фронтенда
COPY backend /app/backend
COPY frontend /app/frontend

# Устанавливаем рабочую директорию для запуска
WORKDIR /app/backend

# Запускаем FastAPI с помощью Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]