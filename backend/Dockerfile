# Dockerfile
FROM python:3.9-alpine3.13

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set PYTHONPATH environment variable
ENV PYTHONPATH=/app

# Ensure the .env file is copied
COPY .env .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

