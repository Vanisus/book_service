FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY app /app
RUN mkdir -p /app/uploads
# Запуск приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5004"]
