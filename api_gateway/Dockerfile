FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY app /app

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Запуск приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5008"]
