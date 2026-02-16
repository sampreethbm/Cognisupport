FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Common Dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Backend Code
COPY backend/app /app/app
COPY backend/alembic /app/alembic
COPY backend/alembic.ini /app/alembic.ini
COPY backend/model.joblib /app/model.joblib

# Copy Frontend Build (Multistage build would be better, but sticking to simple copy as per earlier structure)
# Assuming frontend is built to a 'static' folder or similar if we want to serve it. 
# However, the requirement is likely to run frontend separately or via docker-compose.
# For this Dockerfile, we focus on the Backend API.

EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
