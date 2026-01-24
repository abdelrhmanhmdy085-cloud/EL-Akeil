FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy project files first
COPY . .

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0
ENV SECRET_KEY=railway_production_secret_key
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Run the application
WORKDIR /app/src/backend
CMD ["python", "app.py"]
